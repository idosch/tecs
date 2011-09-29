import sys

class Parser:
    """Encapsulates access to the input code."""

    def __init__(self, temp_file_name):
        """Opens the input stream and gets ready to parse it."""
        self._input_file = open(temp_file_name, 'r')
        self._lines = self._input_file.readlines()
        self._input_file.close()

        self._counter = 0
        self._commands_num = len(self._lines)
        self._command = None

    def has_more_commands(self):
        """Retruns True if current command isn't last, otherwise False."""
        if self._counter < self._commands_num:
            return True
        else:
            return False

    def advance(self):
        """Reads next command from input and makes it current command."""
        self._command = self._lines[self._counter][:-1]
        self._counter += 1

    def command_type(self):
        """Returns the type of the current command."""
        if self._command[0] == '@':
            return 'A_COMMAND'
        elif self._command[0] == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        """Returns symbol or decimal Xxx of current @Xxx or (Xxx) command."""
        if self._command[0] == '@':
            return self._command[1:]
        else:
            return self._command[1:-1]

    def dest(self):
        """Returns the 'dest' mnemonic in the current C-command"""
        if '=' in self._command:
            pos = self._command.find('=')
            return self._command[:pos]
        else:
            return ''

    def comp(self):
        """Returns the 'comp' mnemonic in the current C-command"""
        if '=' in self._command:
            start_pos = self._command.find('=') + 1
        else:
            start_pos = 0

        if ';' in self._command:
            end_pos = self._command.find(';')
        else:
            end_pos = len(self._command)

        return self._command[start_pos:end_pos]

    def jump(self):
        """Returns the 'jump' mnemonic in the current C-command"""
        if ';' in self._command:
            pos = self._command.find(';') + 1
            return self._command[pos:]
        else:
            return 'null'

    def get_file_name(self):
        """Returns the file name without the '.asm' suffix"""
        return sys.argv[1][0:-4]

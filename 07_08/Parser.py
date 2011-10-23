class Parser:
    """Handles the parsing of a single .vm file."""

    def __init__(self, fname):
        input_file = open(fname, 'r')
        code = input_file.readlines()
        input_file.close()
        
        self._code = []
        for line in code:
            line = ' '.join(line.rsplit())

            if '//' in line:
                pos = line.find('//')
                line = line[:pos - 1]

            if line != '':
                self._code.append(line)

        self._number_of_commands = len(self._code)
        self._counter = 0
        self._command = None
        self._file_name = fname

    def has_more_commands(self):
        """Returns 'True' if not at the end, otherwise 'False'."""
        return (self._counter < self._number_of_commands)

    def advance(self):
        """Reads next command from input and makes it current command."""
        self._command = self._code[self._counter]
        self._counter += 1

    def command_type(self):
        """Returns the type of the current VM command."""
        arithmetic_commands = ["add", "sub", "neg", "eq", "gt", "lt", "and",
                               "or", "not"]
        logic_commands = ["and", "or", "not"]


        split = self._command.rsplit()
        if split[0] in arithmetic_commands:
            return 'C_ARITHMETIC'
        elif split[0] in logic_commands:
            return 'C_IF'
        elif split[0] == 'push':
            return 'C_PUSH'
        elif split[0] == 'pop':
            return 'C_POP'
        elif split[0] == 'label':
            return 'C_LABEL'
        elif split[0] == 'goto':
            return 'C_GOTO'
        elif split[0] == 'if-goto':
            return 'C_IF'
        elif split[0] == 'function':
            return 'C_FUNCTION'
        elif split[0] == 'call':
            return 'C_CALL'
        elif split[0] == 'return':
            return 'C_RETURN'

    def arg1(self):
        """Returns the first argument of the current command."""
        split = self._command.rsplit()
        command_type = self.command_type()

        if command_type == 'C_ARITHMETIC':
            return split[0]
        else:
            return split[1]

    def arg2(self):
        """Returns the second argument of the current command."""
        split = self._command.rsplit()

        return int(split[2])

    def get_file_name(self):
        """Returns the file name of the current input file."""
        return self._file_name

    def get_command(self):
        """Returns the current command."""
        return self._command 

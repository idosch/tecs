#!/usr/bin/python

import sys
import os

class Preprocessor:
    """Creates a temporary file without whitespaces and comments."""

    def __init__(self):
        """Opens the input stream and gets ready to process it."""
        self._input_file = open(sys.argv[1], 'r')
        self._code = self._input_file.readlines()
        self._input_file.close()
        self._temp_file = None

    def __del__(self):
        """Removes the temporary file."""
        os.remove(sys.argv[1] + '.tmp')

    def remove_white_spaces_comments(self):
        """Removes white spaces and comments."""
        new_code = []
        for line in self._code:
            line = ''.join(line.rsplit())

            if '//' in line:
                pos = line.find('//')
                line = line[:pos]

            if line != '':
                new_code.append(line)

        self._code = new_code

    def write_temp_file(self):
        """Write the processed text to a temp file."""
        self._temp_file = open(sys.argv[1] + '.tmp', 'w')

        for line in self._code:
            self._temp_file.write(line + str('\n'))

        self._temp_file.close()


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

class Code:
    """Translates Hack assembly language mnemonics into binary codes"""

    def __init__(self):
        """Initializes the symbol tables needed"""
        self._jump_st = dict()
        self._jump_st['null'] = '000'
        self._jump_st['JGT'] = '001'
        self._jump_st['JEQ'] = '010'
        self._jump_st['JGE'] = '011'
        self._jump_st['JLT'] = '100'
        self._jump_st['JNE'] = '101'
        self._jump_st['JLE'] = '110'
        self._jump_st['JMP'] = '111'

        self._comp_st = dict()
        self._comp_st['0'] = '0101010'
        self._comp_st['1'] = '0111111'
        self._comp_st['-1'] = '0111010'
        self._comp_st['D'] = '0001100'
        self._comp_st['A'] = '0110000'
        self._comp_st['M'] = '1110000'
        self._comp_st['!D'] = '0001101'
        self._comp_st['!A'] = '0110001'
        self._comp_st['!M'] = '1110001'
        self._comp_st['-D'] = '0001111'
        self._comp_st['-A'] = '0110011'
        self._comp_st['-M'] = '1110011'
        self._comp_st['D+1'] = '0011111'
        self._comp_st['A+1'] = '0110111'
        self._comp_st['M+1'] = '1110111'
        self._comp_st['D-1'] = '0001110'
        self._comp_st['A-1'] = '0110010'
        self._comp_st['M-1'] = '1110010'
        self._comp_st['D+A'] = '0000010'
        self._comp_st['D+M'] = '1000010'
        self._comp_st['D-A'] = '0010011'
        self._comp_st['D-M'] = '1010011'
        self._comp_st['A-D'] = '0000111'
        self._comp_st['M-D'] = '1000111'
        self._comp_st['D&A'] = '0000000'
        self._comp_st['D&M'] = '1000000'
        self._comp_st['D|A'] = '0010101'
        self._comp_st['D|M'] = '1010101'

    def dest(self, dest_str):
        """Returns the binary code of the 'dest' mnemonic"""
        if 'M' in dest_str:
            d3 = 1
        else:
            d3 = 0
        if 'D' in dest_str:
            d2 = 1
        else:
            d2 = 0
        if 'A' in dest_str:
            d1 = 1
        else:
            d1 = 0

        return str(d1) + str(d2) + str(d3)

    def comp(self, comp_str):
        """Returns the binary code of the 'comp' mnemonic"""
        return self._comp_st[comp_str]

    def jump(self, jump_str):
        """Returns the binary code of the 'jump' mnemonic"""
        return self._jump_st[jump_str]

    def convert_to_binary(self, dec_str):
        """Returns the binary representation of 'dec_str'"""
        bin_str = bin(int(dec_str))
        return bin_str[2:].zfill(15)

class SymbolTable:
    """Keeps a correspondence between symboilic labels and numeric addresses"""

    def __init__(self):
        """Creates a new symbol table"""
        self._st = dict()
        self._st['SP'] = 0
        self._st['LCL'] = 1
        self._st['ARG'] = 2
        self._st['THIS'] = 3
        self._st['THAT'] = 4
        self._st['SCREEN'] = 16384
        self._st['KBD'] = 24576
        for i in range(16):
            self._st['R' + str(i)] = i

    def addEntry(self, symbol, address):
        """Adds the pair (symbol, address) to the table"""
        self._st[symbol] = address

    def contains(self, symbol):
        """Checks whether symbol is in the symbol table"""
        return symbol in self._st.keys()

    def GetAddress(self, symbol):
        """Returns the address associated with the symbol"""
        return self._st[symbol]

def main():
    """Drives the entire translation process."""

    """Preprocess the file"""
    pp = Preprocessor()
    pp.remove_white_spaces_comments()
    pp.write_temp_file()

    """First pass - adds labels to the symbol table."""
    parser = Parser(sys.argv[1] + '.tmp')
    symbol_table = SymbolTable()
    pc = -1
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == 'A_COMMAND' or command_type == 'C_COMMAND':
            pc += 1
        elif command_type == 'L_COMMAND':
            label = parser.symbol()
            symbol_table.addEntry(label, pc + 1)

    """Second pass - handles variables names and writes the *.hack file."""
    ram_address = 16
    parser = Parser(sys.argv[1] + '.tmp')
    code = Code()
    file_name = parser.get_file_name()
    hack_file = open(file_name + '.hack', 'w')

    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == 'A_COMMAND':
            a_symbol = parser.symbol()
            if a_symbol[0] in '0123456789':
                a_symbol_binary = code.convert_to_binary(a_symbol)
                hack_file.write('0' + a_symbol_binary + '\n')
            else:
                if symbol_table.contains(a_symbol) is False:
                    symbol_table.addEntry(a_symbol, ram_address)
                    ram_address += 1
                address = symbol_table.GetAddress(a_symbol)
                address_binary = code.convert_to_binary(address)
                hack_file.write('0' + address_binary + '\n')

        elif command_type == 'C_COMMAND':
            comp = code.comp(parser.comp())
            dest = code.dest(parser.dest())
            jump = code.jump(parser.jump())
            hack_file.write('111' + comp + dest + jump + '\n')

    hack_file.close()

if __name__ == '__main__':
    main()

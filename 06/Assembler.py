#!/usr/bin/python

import sys
from Preprocessor import *
from Parser import *
from Code import *
from SymbolTable import *

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

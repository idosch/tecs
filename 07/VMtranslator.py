#!/usr/bin/python

import sys
import os
from Parser import *
from CodeWriter import *

def main():
    """Drives the VM-to-Hack translation procces"""
    file_name = sys.argv[1]
    parsers = []
    abs_path = os.path.abspath(file_name)
    if '.vm' in file_name and file_name[-3:] == '.vm':
        parser = Parser(abs_path)
        parsers.append(parser)
        output_path = os.path.splitext(abs_path)[0] + '.asm'
    else:
        path_split = abs_path.rsplit('/')
        output_path = '/'.join(path_split[:-1]) + '/' + path_split[-1] + '.asm'
        for walk_obj in os.walk(abs_path):
            for vm_file in walk_obj[2]:
                parser = Parser(abs_path + '/' + vm_file)
                parsers.append(parser)
    
    cw = CodeWriter(output_path)
    for parser in parsers:
        #cw.set_file_name(parser.get_file_name())
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            if command_type == 'C_ARITHMETIC':
                cw.write_arithmetic(parser.get_command())
            elif command_type == 'C_PUSH' or command_type == 'C_POP':
                #command = parser.get_command()
                command = command_type
                segment = parser.arg1()
                index = parser.arg2()
                cw.write_push_pop(command, segment, index)

    """
    TESTING
    TODO: delete
    for p in parsers:
        arg2_type = ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]
        while p.has_more_commands():
            p.advance()
            com_type = p.command_type()
            print('command type: ' + com_type)
            if com_type != 'C_RETURN':
                print('Arg1: ' + p.arg1())
            if com_type in arg2_type:
                print('Arg2: ' + str(p.arg2()))
            print('-----')
    """

    #print(output_path)


if __name__ == '__main__':
    main()

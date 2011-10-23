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
        output_path = abs_path + '/' + path_split[-1] + '.asm'
        for walk_obj in os.walk(abs_path):
            for vm_file in walk_obj[2]:
                if '.vm' in vm_file and vm_file[-3:] == '.vm':
                    parser = Parser(abs_path + '/' + vm_file)
                    parsers.append(parser)

    cw = CodeWriter(output_path)
    cw.write_init()
    for parser in parsers:
        a_path = parser.get_file_name()
        fname = os.path.split(a_path)[1][:-3]
        cw.set_file_name(fname)
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            if command_type == 'C_ARITHMETIC':
                cw.write_arithmetic(parser.get_command())
            elif command_type == 'C_PUSH' or command_type == 'C_POP':
                command = command_type
                segment = parser.arg1()
                index = parser.arg2()
                cw.write_push_pop(command, segment, index)
            elif command_type == 'C_LABEL':
                label = parser.arg1()
                cw.write_label(label)
            elif command_type == 'C_GOTO':
                label = parser.arg1()
                cw.write_goto(label)
            elif command_type == 'C_IF':
                label = parser.arg1()
                cw.write_if(label)
            elif command_type == 'C_CALL':
                function_name = parser.arg1()
                num_args = parser.arg2()
                cw.write_call(function_name, num_args)
            elif command_type == 'C_RETURN':
                cw.write_return()
            elif command_type == 'C_FUNCTION':
                function_name = parser.arg1()
                num_locals = parser.arg2()
                cw.write_function(function_name, num_locals)

if __name__ == '__main__':
    main()

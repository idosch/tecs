#!/usr/bin/python

import sys
import os
from JackTokenizer import *

def main():
    """Drives the Jack-to-VM translation process"""
    file_name = sys.argv[1]
    tokenizers = []
    output_files = []

    abs_path = os.path.abspath(file_name)

    if '.jack' in file_name and file_name[-5:] == '.jack':
        tokenizer = JackTokenizer(abs_path)
        tokenizers.append(tokenizer)
        output_path = os.path.splitext(abs_path)[0] + '.xml'
        output_files.append(output_path)
    else:
        for walk_obj in os.walk(abs_path):
            for jack_file in walk_obj[2]:
                if '.jack' in jack_file and jack_file[-5:] == '.jack':
                    tokenizer = JackTokenizer(abs_path + '/' + jack_file)
                    tokenizers.append(tokenizer)
                    output_path = abs_path + '/' + jack_file[:-5] + '.xml'
                    output_files.append(output_path)
    
    for tokenizer in tokenizers:
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            token_type = tokenizer.token_type()

            if token_type == 'KEYWORD':
                keyword = tokenizer.keyword()
            elif token_type == 'SYMBOL':
                symbol = tokenizer.symbol()
            elif token_type == 'IDENTIFIER':
                identifier = tokenizer.identifier()
            elif token_type == 'INT_CONST':
                int_val = tokenizer.int_val()
            elif token_type == 'STRING_CONST':
                string_val = tokenizer.string_val()

if __name__ == '__main__':
    main()

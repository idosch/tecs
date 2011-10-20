class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_path):
        """Opens the output file and gets ready to write into it."""
        self._output_file = open(output_path, 'w')

    def __del__(self):
        """Closes the output file."""
        self._output_file.write('(END)\n')
        self._output_file.write('@END\n')
        self._output_file.write('0;JMP\n')
        self._output_file.close()

    def set_file_name(self, file_name):
        """Informs the coder writer that the translation of a new VM file
           started"""
        pass

    def write_arithmetic(self, command):
        """Writes the assembly code that is the translation of the the given
           arithmetic command."""
        if command == 'add':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nM=D+M\nD=A+1\n')
            self._output_file.write('@SP\nM=D\n')
        elif command == 'sub':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nM=M-D\nD=A+1\n')
            self._output_file.write('@SP\nM=D\n')
        elif command == 'neg':
            self._output_file.write('@SP\nA=M-1\nM=-M\n')
        elif command == 'and':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nM=D&M\n@SP\n\
                    M=M-1\n')
        elif command == 'or':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nM=D|M\n@SP\n\
                    M=M-1\n')
        elif command == 'not':
            self._output_file.write('@SP\nA=M-1\nM=!M\n')
        elif command == 'eq':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@SP\n\
                    M=M-1\n@EQUAL\nD;JEQ\n@NOT_EQUAL\nD;JNE\n(EQUAL)\n\
                    @SP\nA=M-1\nM=-1\n@END_EQ\n0;JMP\n\
                    (NOT_EQUAL)\n@SP\nA=M-1\nM=0\n@END_EQ\n0;JMP\n\
                    (END_EQ)\n')
        elif command == 'gt':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\n\
                    M=M-1\n@GREATER\nD;JGT\n@LESS_EQUAL\nD;JLE\n(GREATER)\n\
                    @SP\nA=M-1\nM=-1\n@END_GT\n0;JMP\n\
                    (LESS_EQUAL)\n@SP\nA=M-1\nM=0\n@END_GT\n0;JMP\n\
                    (END_GT)\n')
        elif command == 'lt':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\n\
                    M=M-1\n@LESS\nD;JLT\n@GE\nD;JGE\n(LESS)\n\
                    @SP\nA=M-1\nM=-1\n@END_LT\n0;JMP\n(GE)\n@SP\n\
                    A=M-1\nM=0\n@END_LT\n0;JMP\n(END_LT)\n')

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given
           command where command is either C_PUSH or C_POP."""
        if command == 'C_PUSH':
            if segment == 'constant':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@SP\nA=M\n')
                self._output_file.write('M=D\n@SP\nM=M+1\n')

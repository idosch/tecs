class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_path):
        """Opens the output file and gets ready to write into it."""
        self._output_file = open(output_path, 'w')
        self._file_name = None
        self._current_function = 'none'
        self._counter = 0
        self._a_counter = 0

    def __del__(self):
        """Closes the output file."""
        self._output_file.write('(END)\n')
        self._output_file.write('@END\n')
        self._output_file.write('0;JMP\n')
        self._output_file.close()

    def set_file_name(self, file_name):
        """Informs the coder writer that the translation of a new VM file
           started"""
        self._file_name = file_name

    def write_arithmetic(self, command):
        """Writes the assembly code for the corresponding math command."""
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
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@SP\n')
            self._output_file.write('M=M-1\n')
            self._output_file.write('@EQUAL_' + str(self._a_counter) + '\n')
            self._output_file.write('D;JEQ\n')
            self._output_file.write('@NOT_EQUAL_' + str(self._a_counter) + '\n')
            self._output_file.write('D;JNE\n')
            self._output_file.write('(EQUAL_' + str(self._a_counter) + ')\n')
            self._output_file.write('@SP\nA=M-1\nM=-1\n')
            self._output_file.write('@END_EQ_' + str(self._a_counter) + '\n')
            self._output_file.write('0;JMP\n')
            self._output_file.write('(NOT_EQUAL_' + str(self._a_counter) + ')\n')
            self._output_file.write('@SP\nA=M-1\nM=0\n')
            self._output_file.write('@END_EQ_' + str(self._a_counter) + '\n')
            self._output_file.write('0;JMP\n')
            self._output_file.write('(END_EQ_' + str(self._a_counter) + ')\n')
        elif command == 'gt':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\n')
            self._output_file.write('M=M-1\n')
            self._output_file.write('@GREATER_' + str(self._a_counter) + '\n')
            self._output_file.write('D;JGT\n')
            self._output_file.write('@LESS_EQUAL_' + str(self._a_counter) + '\n')
            self._output_file.write('D;JLE\n')
            self._output_file.write('(GREATER_' + str(self._a_counter) + ')\n')
            self._output_file.write('@SP\nA=M-1\nM=-1\n')
            self._output_file.write('@END_GT_' + str(self._a_counter) + '\n')
            self._output_file.write('0;JMP\n')
            self._output_file.write('(LESS_EQUAL_' + str(self._a_counter) + ')\n')
            self._output_file.write('@SP\nA=M-1\nM=0\n')
            self._output_file.write('@END_GT_' + str(self._a_counter) + '\n')
            self._output_file.write('0;JMP\n')
            self._output_file.write('(END_GT_' + str(self._a_counter) + ')\n')
        elif command == 'lt':
            self._output_file.write('@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\n')
            self._output_file.write('M=M-1\n')
            self._output_file.write('@LESS_' + str(self._a_counter) + '\n')
            self._output_file.write('D;JLT\n')
            self._output_file.write('@GE_' + str(self._a_counter) + '\n')
            self._output_file.write('D;JGE\n')
            self._output_file.write('(LESS_' + str(self._a_counter) + ')\n')
            self._output_file.write('@SP\nA=M-1\nM=-1\n')
            self._output_file.write('@END_LT_' + str(self._a_counter) + '\n')
            self._output_file.write('0;JMP\n')
            self._output_file.write('(GE_' + str(self._a_counter) + ')\n')
            self._output_file.write('@SP\nA=M-1\nM=0\n')
            self._output_file.write('@END_LT_' + str(self._a_counter) + '\n')
            self._output_file.write('0;JMP\n')
            self._output_file.write('(END_LT_' + str(self._a_counter) + ')\n')

        self._a_counter += 1

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given
           command where command is either C_PUSH or C_POP."""
        if command == 'C_PUSH':
            if segment == 'constant':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@SP\nA=M\n')
                self._output_file.write('M=D\n@SP\nM=M+1\n')
            if segment == 'local':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@LCL\nA=D+M\nD=M\n@SP\nA=M\n\
                        M=D\n@SP\nM=M+1\n')
            if segment == 'argument':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@ARG\nA=D+M\nD=M\n@SP\nA=M\n\
                        M=D\n@SP\nM=M+1\n')
            if segment == 'this':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@THIS\nA=D+M\nD=M\n@SP\nA=M\n\
                        M=D\n@SP\nM=M+1\n')
            if segment == 'that':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@THAT\nA=D+M\nD=M\n@SP\nA=M\n\
                        M=D\n@SP\nM=M+1\n')
            if segment == 'pointer':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@3\nA=D+A\nD=M\n@SP\nA=M\nM=D\n\
                        @SP\nM=M+1\n')
            if segment == 'temp':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n\
                        @SP\nM=M+1\n')
            if segment == 'static':
                self._output_file.write('@' + self._file_name + '.' +\
                        str(index) + '\n')
                self._output_file.write('D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')

        if command == 'C_POP':
            if segment == 'local':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\n\
                        A=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\n\
                        A=M\nM=D\n')
            if segment == 'argument':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\n\
                        A=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\n\
                        A=M\nM=D\n')
            if segment == 'this':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\n\
                        A=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\n\
                        A=M\nM=D\n')
            if segment == 'that':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\n\
                        A=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\n\
                        A=M\nM=D\n')
            if segment == 'pointer':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@3\nD=D+A\n@R13\nM=D\n@SP\n\
                        A=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\n\
                        A=M\nM=D\n')
            if segment == 'temp':
                self._output_file.write('@' + str(index) + '\n')
                self._output_file.write('D=A\n@5\nD=D+A\n@R13\nM=D\n@SP\n\
                        A=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\n\
                        A=M\nM=D\n')
            if segment == 'static':
                self._output_file.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n')
                self._output_file.write('@' + self._file_name + '.' +\
                        str(index) + '\n')
                self._output_file.write('M=D\n')

    def write_label(self, label):
        """Writes assembly code that effects the label command."""
        self._output_file.write('(' + self._current_function + '$' + label\
                + ')\n')

    def write_goto(self, label):
        """Writes assembly code that effects the goto command."""
        self._output_file.write('@' + self._current_function + '$' + label\
                + '\n')
        self._output_file.write('0;JMP\n')

    def write_if(self, label):
        """Writes assembly code that effects the if-goto command."""
        self._output_file.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n')
        self._output_file.write('@' + self._current_function + '$' + label\
                + '\n')
        self._output_file.write('D;JNE\n')

    def write_call(self, func_name, num_args):
        """Writes assembly code that effects the call command."""
        self._output_file.write('@RET_' + func_name + '_')
        self._output_file.write(str(self._counter) + '\n')
        self._output_file.write('D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@' + str(num_args) + '\n')
        self._output_file.write('D=A\n@SP\nD=M-D\n@5\nD=D-A\n@ARG\nM=D\n')
        self._output_file.write('@SP\nD=M\n@LCL\nM=D\n')
        self._output_file.write('@' + func_name + '\n')
        self._output_file.write('0;JMP\n')
        self._output_file.write('(RET_' + func_name + '_')
        self._output_file.write(str(self._counter) + ')\n')
        self._counter += 1

    def write_return(self):
        """Writes the assembly code that effects the return command."""
        self._output_file.write('@LCL\nD=M\n@FRAME\nM=D\n')
        self._output_file.write('@5\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@RET\nM=D')
        self._output_file.write('\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n')
        self._output_file.write('@ARG\nD=M\n@SP\nM=D+1\n')
        self._output_file.write('@1\nD=A\n@FRAME\nA=M-D\nD=M\n@THAT\nM=D\n')
        self._output_file.write('@2\nD=A\n@FRAME\nA=M-D\nD=M\n@THIS\nM=D\n')
        self._output_file.write('@3\nD=A\n@FRAME\nA=M-D\nD=M\n@ARG\nM=D\n')
        self._output_file.write('@4\nD=A\n@FRAME\nA=M-D\nD=M\n@LCL\nM=D\n')
        self._output_file.write('@RET\nA=M\n0;JMP\n')

    def write_function(self, func_name, num_locals):
        """Writes assembly code that effects the function command."""
        self._output_file.write('(' + func_name + ')\n')
        self._output_file.write('@' + str(num_locals) + '\n')
        self._output_file.write('D=A\n@END_LOOP_' + func_name + '\n')
        self._output_file.write('D;JLE\n(LOOP_' + func_name + ')\n')
        self._output_file.write('@SP\nA=M\nM=0\n@SP\nM=M+1\nD=D-1\n')
        self._output_file.write('@LOOP_' + func_name + '\nD;JGT\n')
        self._output_file.write('(END_LOOP_' + func_name + ')\n')

        self._current_function = func_name

    def write_init(self):
        """Writes the bootstrap code."""
        self._output_file.write('@256\nD=A\n@SP\nM=D\n')
        self._output_file.write('@RET_Sys.init\n')
        self._output_file.write('D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self._output_file.write('D=0\n@SP\nD=M-D\n@5\nD=D-A\n@ARG\nM=D\n')
        self._output_file.write('@SP\nD=M\n@LCL\nM=D\n')
        self._output_file.write('@Sys.init\n')
        self._output_file.write('0;JMP\n')
        self._output_file.write('(RET_Sys.init)\n')

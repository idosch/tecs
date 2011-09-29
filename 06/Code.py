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

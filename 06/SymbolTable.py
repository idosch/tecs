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

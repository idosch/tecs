class JackTokenizer:
    """Removes all comments and white space from the input stream and breaks\
    it into Jack-language tokens, as specified by the Jack grammar."""

    def __init__(self, fname):
        self._keyword = ['class', 'constructor', 'function', 'method',
                         'field', 'static', 'var', 'int', 'char',
                         'boolean', 'void', 'true', 'false', 'null',
                         'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self._symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-',
                        '*', '/', '&', '|', '<', '>', '=', '~']

        input_file = open(fname, 'r')
        code = input_file.readlines()
        input_file.close()
        
        lines = []
        self._tokens = []
        for line in code:
            line = ' '.join(line.rsplit())

            if '//' in line:
                pos = line.find('//')
                line = line[:pos]
            if '/*' in line:
                continue
            if line != '' and line[0] == '*':
                continue
            if '"' in line:
                pos = line.find('"')
                end = line.find('"', pos + 1)
                lines.append(line[:pos])
                lines.append(line[pos: end + 1])
                lines.append(line[end + 1:])
                continue
            if line != '':
                lines.append(line)

        for line in lines:
            if line[0] == '"':
                self._tokens.append(line)
            else:
                line = line.rsplit()
                for word in line:
                    appended = False
                    if word in self._keyword or word in self._symbol:
                        self._tokens.append(word)
                        appended = True
                    else:
                        cur_word = ''
                        for char in word:
                            cur_word = cur_word + char
                            if char in self._symbol:
                                if len(cur_word) == 1:
                                    self._tokens.append(char)
                                    appended = True
                                elif cur_word != '':
                                    self._tokens.append(cur_word[:-1])
                                    self._tokens.append(char)
                                    appended = True
                                cur_word = ''
                            else:
                                appended = False
                    if appended == False:
                        self._tokens.append(cur_word)

        self._number_of_tokens = len(self._tokens)
        self._counter = 0
        self._token = None

    def has_more_tokens(self):
        """Returns 'True' if not at the end, otherwise 'False'."""
        return (self._counter < self._number_of_tokens)

    def advance(self):
        """Reads next token from input and makes it current token."""
        self._token = self._tokens[self._counter]
        self._counter += 1

    def token_type(self):
        """Returns the type of the current token."""
        if self._token in self._keyword:
            return 'KEYWORD'
        elif self._token in self._symbol:
            return 'SYMBOL'
        elif self._token.isnumeric():
            return 'INT_CONST'
        elif self._token[0] == '"':
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'

    def keyword(self):
        """Returns the keyword which is the current token."""
        return self._token.upper()

    def symbol(self):
        """Returns the character which is the current token."""
        return self._token

    def identifier(self):
        """Returns the identifier which is the current token."""
        return self._token

    def int_val(self):
        """Returns the integer value of the current token."""
        return int(self._token)

    def string_val(self):
        """Returns the string value of the current token w/o double quotes."""
        return self._token[1:-1]

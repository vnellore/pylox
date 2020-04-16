class Token:
    def __init__(self, tokentype, lexeme, literal, line):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f'{self.__class__.__name__}({self.tokentype}, {self.lexeme}, {self.literal}, {self.line})'

    def __str__(self):
        return f'{self.tokentype} {self.lexeme} {self.literal}'

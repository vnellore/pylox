import token
import token_type
import lox

class Scanner:
    def __init__(self, source):
        self.tokens = []
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while self.isAtEnd() == False:
            self.start = self.current
            self.scanToken()

        self.tokens.append(token.Token(token_type.TokenType.EOF, "", None, self.line))

        return self.tokens    
    
    def scanToken(self):

        c = self.advance()

        if (c == '('):
            self.addToken(token_type.TokenType.LEFT_PAREN)
        elif (c == ')'):
            self.addToken(token_type.TokenType.RIGHT_PAREN)
        elif (c == '{'):
            self.addToken(token_type.TokenType.LEFT_BRACE)
        elif (c == '}'):
            self.addToken(token_type.TokenType.RIGHT_BRACE)
        elif (c == ','):
            self.addToken(token_type.TokenType.COMMA)
        elif (c == '.'):
            self.addToken(token_type.TokenType.DOT)
        elif (c == '-'):
            self.addToken(token_type.TokenType.MINUS)
        elif (c == '+'):
            self.addToken(token_type.TokenType.PLUS)
        elif (c == ';'):
            self.addToken(token_type.TokenType.SEMICOLON)
        elif (c == '*'):
            self.addToken(token_type.TokenType.STAR)
        else:
            lox.error(self.line, "Unexpected character.")
                
    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(token.Token(token_type, text, literal, self.line))    
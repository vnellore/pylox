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
        self.keywords = {"and":token_type.TokenType.AND,
        "class":token_type.TokenType.CLASS,
        "else":token_type.TokenType.ELSE,
        "false":token_type.TokenType.FALSE,
        "for":token_type.TokenType.FOR,
        "fun":token_type.TokenType.FUN,
        "if":token_type.TokenType.IF,
        "nil":token_type.TokenType.NIL,
        "or":token_type.TokenType.OR,
        "print":token_type.TokenType.PRINT,
        "return":token_type.TokenType.RETURN,
        "super":token_type.TokenType.SUPER,
        "this":token_type.TokenType.THIS,
        "true":token_type.TokenType.TRUE,
        "var":token_type.TokenType.VAR,
        "while":token_type.TokenType.WHILE
        }

    def scanTokens(self):
        """
        Function to scan all token in given source
        """
        while self.isAtEnd() == False:
            self.start = self.current
            self.scanToken()

        self.tokens.append(token.Token(token_type.TokenType.EOF, "", None, self.line))

        return self.tokens    
    
    def scanToken(self):
        """
        Determines and adds token type and value to token list
        """
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
        elif (c == '!'):
            self.addToken(token_type.TokenType.BANG_EQUAL if self.match('=') else token_type.TokenType.BANG)
        elif (c == '='):
            self.addToken(token_type.TokenType.EQUAL_EQUAL if self.match('=') else token_type.TokenType.EQUAL)
        elif (c == '<'):
            self.addToken(token_type.TokenType.LESS_EQUAL if self.match('=') else token_type.TokenType.LESS)
        elif (c == '>'):
            self.addToken(token_type.TokenType.GREATER_EQUAL if self.match('=') else token_type.TokenType.GREATER)
        elif (c == '/'):
            if (self.match('/')):
                while (self.peek() != '\n' and self.isAtEnd() == False ):
                    self.advance()
            else:
                self.addToken(token_type.TokenType.SLASH)
        elif (c == ' '): 
            pass
        elif (c == '\r'):
            pass
        elif (c == '\t'):
            pass
        elif (c == '\n'):
            self.line += 1
        elif (c == '"'):
            self.string()
        else:
            if (self.isDigit(c)):
                self.number()
            elif (self.isAlpha(c)) :
                self.identifier()

            else:
                lox.error(self.line, f"Unexpected character {c}")

    def identifier(self):
        while (self.isAlphaNumeric(self.peek())):
            self.advance()
        
        # See if the identifier is a reserved word
        text = self.source[self.start:self.current]
        type = self.keywords[text]

        if(type):
            self.addToken(type)
        else:    
            type = token_type.TokenType.IDENTIFIER


    def isAlpha(self, c):
        return (c >= 'a' and c <='z') or (c >= 'A' and c <='Z') or (c =='_') 

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def string(self):
        """
        Determines and adds a string token to list
        """
        while(self.peek() != '"' and self.isAtEnd()==False):
            if (self.peek() == '\n'):
                self.line += 1
            self.advance()
        
        # unterminated string
        if (self.isAtEnd()):
            lox.error(self.line,"Unterminated string.")
            return
        
        # the closing "
        self.advance()

        # trim the surrounding quotes
        value = self.source[self.start + 1 : self.current - 1]
        self.addToken(token_type.TokenType.STRING, value)


    def number(self):
        while (self.isDigit(self.peek())):
            self.advance() 
        # Look for fractional part
        if (self.peek() == '.') and self.isDigit(self.peekNext()):
            # consume the "."
            self.advance()

            while(self.isDigit(self.peek())):
                self.advance()

        self.addToken(token_type.TokenType.NUMBER, float(self.source[self.start:self.current]))

    def peek(self):
        """
        Function which returns next character without advancing the character. Return '\0' if EOF
        """
        if (self.isAtEnd()):
            return '\0'

        return self.source[self.current]    
    
    def peekNext(self):
        if (self.current + 1 >= len(self.source)):
            return '\0'
        
        return self.source[self.current + 1]

    def isDigit(self, c):
        """
        Determine if character is a numeric digit
        """
        return c > '0' and c <= '9'


    def match(self, expected):
        """
        Function to determine if current character matches the argument passed in
        """
        if(self.isAtEnd()): 
            return False
        if (self.source[self.current] != expected):
            return False

        self.current += 1

        return True


    def isAtEnd(self):
        """
        Function to determine if current position is end of file
        """
        return self.current >= len(self.source)

    def advance(self):
        """
        Function to advance and return next character
        """
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, token_type, literal=None):
        """
        Add token to list of tokens
        """
        text = self.source[self.start:self.current]
        self.tokens.append(token.Token(token_type, text, literal, self.line))    
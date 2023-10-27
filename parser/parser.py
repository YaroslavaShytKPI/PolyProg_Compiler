from PolyProg_Compiler.analyzer.lexical_analyzer import lex, table_of_sym


class Parser:
    num_row = 1

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
        return cls.instance

    # Program =  main ‘()‘ ‘{’ DeclarList DoSection ‘}’
    def parse_program(self):
        try:
            self.parse_token("main", "keyword", "")
            print("Parser: Синтаксичний аналiз завершився успiшно")
            return True
        except SystemExit as e:
            print(f"Parses: Аварійне завершення програми з кодом {0}".format(e))

    def parse_token(self, lexeme, token, ident):
        if self.num_row > len(table_of_sym):
            self.fail_parse("Неочікуваний кінець програми", (lexeme, token, self.num_row))
        num_line, lex, tok = self.get_sym()
        self.num_row += 1
        if (lex, tok) == (lexeme, token):
            print(ident + "parseToken: В рядку {0} токен {1}".format(num_line, (lexeme, token)))
            return True
        else:
            self.fail_parse("Невідповідність токенів", (num_line, lex, tok, lexeme, token))
            return False

    def get_sym(self):
        num_line, lexeme, token, _ = table_of_sym[self.num_row]
        return num_line, lexeme, token

    def fail_parse(self, str, tuple):
        if str == "Неочікуваний кінець програми":
            (lexeme, token, self.num_row) = tuple
            print(
                "Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}.\n\t Очікувалось - {0}".format(
                    (lexeme, token), self.num_row))
            exit(1001)
        elif str == "Невідповідність токенів":
            (num_line, lexeme, token, lex, tok) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент({1},{2}). \n\tОчікувався - ({3},{4})".format(
                num_line, lexeme, token, lex, tok))
            exit(1)

    # StatementList = Statement {; Statement}
    def parse_statement_list(self):
        print("\t parse statement list")
        while self.parse_statement():
            pass
        return True

    # Statement = Assign | Inp | Out | ForStatement |DoWhileStatement| IfStatement
    def parse_statement(self):
        print("\t\t parse statement (): ")
        num_line, lex, tok = self.get_sym()

        if tok == "id": #????????? ident
            self.parse_assign()
            return True
        elif (lex, tok) == ("if", "keyword"):
            self.parse_if()
            return True
        elif (lex, tok) == ("print", "keyword"):
            self.parse_print()
            return True
        elif (lex, tok) == ("readline", "keyword"):
            self.parse_readline()
            return True
        elif (lex, tok) == ("for", "keyword"):
            self.parse_for()
            return True
        elif (lex, tok) == ("do", "keyword"):
            self.parse_do()
            return True
        else:
            self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, 'ident або if'))
            return False

    def parse_assign(self):
        print("\t"*4 + "parse assign()")
        num_line, lex, tok = self.get_sym()
        self.num_row += 1
        print("\t"*5 +"в рядку {0} - {1}".format(numLine, (lex, tok)))
        # якщо ця поточна лексема - ’:=’
        if self.parse_token("=", "assign_op", "\t\t\t\t\t"):
            self.parse_expression()
            return True
        else:
            return False





lex()
print('-'*30)
print('tableOfSymb:{0}'.format(table_of_sym))
print('-'*30)
parser = Parser().parse_program()
from lexical_analyzer import lex, table_of_sym

class Parser:
    num_row = 1

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
        
        return cls.instance

    # Program =  main ‘()‘ ‘{’ DeclarList DoSection ‘}’
    def parse_main(self):
        try:
            self.parse_token("main", "keyword", "")
            self.parse_token("{", "breacket_op", "")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op", "")
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
        if self.num_row > len(table_of_sym):
            self.fail_parse("get_sym(): Неочікуваний кінець програми", (self.num_row))

        num_line, lexeme, token, _ = table_of_sym[self.num_row]

        return num_line, lexeme, token

    def fail_parse(self, str, tuple):
        if str == "Неочікуваний кінець програми":
            (lexeme, token, self.num_row) = tuple
            print("Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}.\n\t Очікувалось - {0}".format(
                  (lexeme, token), self.num_row))
            exit(1001)

        if str == "get_sym(): Неочікуваний кінець програми":
            self.num_row = tuple
            print("Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}".format(
                  self.num_row, table_of_sym[self.num_row-1]))
            exit(1002)
        elif str == "Невідповідність токенів":
            (num_line, lexeme, token, lex, tok) = tuple
            print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - ({3}, {4}).'.format(
                  num_line, lexeme, token, lex, tok))
            exit(1)
        elif str == "Невідповідність інструкцій" or str == "Невiдповiднiсть у Expression.Factor":
            (num_line, lex, tok, expected) = tuple
            print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.'.format(
                num_line, lex, tok, expected))
            exit(2)

    # StatementList = Statement {; Statement}
    def parse_statement_list(self):
        print("\t parse statement list")
        while self.parse_statement():
            self.parse_token(";", "punct", "\t")
        
        return True

    # Statement = Assign | Inp | Out | ForStatement |DoWhileStatement| IfStatement
    def parse_statement(self):
        print("\t\t parse statement (): ")
        num_line, lex, tok = self.get_sym()
        #print(f"DATA {self.get_sym()}")

        if tok == "id":
            self.parse_assign()
            return True

        elif (lex, tok) == ("print", "keyword"):
            self.parse_print()
            return True

        elif (lex, tok) == ("readline", "keyword"):
            self.parse_readline()
            return True

        elif (lex, tok) == ('}', 'breacket_op'):
            return False
        else:
            self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, 'id або if'))

            return False

    # ID - done, CONST, EXPRESSION??????????, не виводить цифри
    def parse_print(self):
        print("\t" * 4 + "parse_print():")
        _, lex, tok = self.get_sym()

        if lex == "print" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op", "\t")
            self.parse_id_list()
            self.parse_token(")", "breacket_op", "\t")
            return True
        else:
            return False

    def parse_id_list(self):
        print("\t" * 5 + "parse_ident_list():")
        while self.parse_id():
            self.parse_token(",", "punct", "\t")
        return True

    def parse_id(self):
        print("\t" * 6 + "parse_id():")
        while True:
            num_line, lex, tok = self.get_sym()
            if tok in "id":
                self.num_row += 1
                print('\t' * 7 + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
            else:
                break
        return False

    def parse_readline(self):
        print("\t" * 4 + "parse_readline():")
        _, lex, tok = self.get_sym()
        if lex == "readline" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op", "\t")
            self.parse_id_list()
            self.parse_token(")", "breacket_op", "\t")
            return True
        else:
            return False

    # Assign = Ident ‘=’ Expression ‘;’
    def parse_assign(self):
        print("\t" * 4 + "parse_assign():")
        num_line, lex, tok = self.get_sym()
        self.num_row += 1
        print("\t" * 5 + "в рядку {0} - {1}".format(num_line, (lex, tok)))

        if self.parse_token("=", "assign_op", "\t\t\t\t\t"):
            self.parse_ind_expression()
            return True
        else:
            return False

    # IndExpr = Ident ‘=’ MathExpression1 ‘;’ BoolExpression ‘;’ Ident ‘=’ MathExpression2
    def parse_ind_expression(self):
        print("\t" * 5 + "parse_ind_expression():")
        num_line, lex, tok = self.get_sym()
        self.parse_term()
        F = True

        while F:
            num_line, lex, tok = self.get_sym()
            if tok in "add_op":
                self.num_row += 1
                print("\t" * 6 + "в рядку {0} - {1}".format(num_line, (lex, tok)))
                self.parse_term()
            else:
                F = False
        
        return True

    def parse_term(self):
        print("\t" * 6 + "parse_term():")
        self.parse_factor()
        F = True

        while F:
            num_line, lex, tok = self.get_sym()
            if tok in "mult_op":
                self.num_row += 1
                print("\t" * 6 + "в рядку {0} - {1}".format(num_line, (lex, tok)))
                self.parse_factor()
            else:
                F = False
        return True

    def parse_factor(self):
        print("\t" * 7 + "parse_factor():")
        num_line, lex, tok = self.get_sym()

        print("\t" * 7 + "parseFactor(): рядок: {0}\t (lex, tok): {1}".format(num_line, (lex, tok)))
        if tok in ("intnum", "doublenum", "id"):
            self.num_row += 1
            print("\t" * 7 + "в рядку {0} - {1}".format(num_line, (lex, tok)))
        elif lex == "(":
            self.num_row += 1
            self.parse_ind_expression()
            self.parse_token(")", "breacket_op", "\t"*7)
            print("\t"*7 + "в рядку {0} - {1}".format(num_line, (lex, tok)))
        else:
            self.fail_parse("Невiдповiднiсть у Expression.Factor", (num_line, lex, tok,"rel_op, int, double, id або \’(\’ Expression \’)\’"))

        return True


lex()
print('-' * 30)
print('tableOfSymb:{0}'.format(table_of_sym))
print('-' * 30)
parser = Parser().parse_main()


"""
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
"""
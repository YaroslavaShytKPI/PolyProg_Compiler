from lexical_analyzer import lex, table_of_sym

class Parser:
    num_row = 1
    column = 1

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
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - ({3}, {4}).".format(
                  num_line, lexeme, token, lex, tok))
            exit(1)
        elif str == "Невідповідність інструкцій" or str == "Невiдповiднiсть у Expression.Factor":
            (num_line, lex, tok, expected) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.".format(
                num_line, lex, tok, expected))
            exit(2)
        elif str == "Mismatch in BoolExpr" or str == "Невiдповiднiсть у Power":
            (num_line, lex, tok, expected) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.".format(
                num_line, lex, tok, expected))
        # elif str == "Тіло оператору не має бути порожнім":
        #     (num_line, lex, tok) = tuple
        #     print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\tТіло оператору не має бути порожнім.".format(
        #         num_line, lex, tok))

    # StatementList = Statement {; Statement}
    def parse_statement_list(self):
        print("\t" * self.column + "parse_statement_list():")
        while self.parse_statement():
            pass
        
        return True

    # Statement = Assign | Inp | Out | ForStatement |DoWhileStatement| IfStatement
    def parse_statement(self):
        self.column = 2
        print("\t" * self.column + "parse_statement():")
        num_line, lex, tok = self.get_sym()

        if tok == "id":
            self.parse_assign()
            self.parse_token(";", "punct", "\t")
            return True

        elif (lex, tok) == ("print", "keyword"):
            self.parse_print()
            self.parse_token(";", "punct", "\t")
            return True

        elif (lex, tok) == ("readline", "keyword"):
            self.parse_readline()
            self.parse_token(";", "punct", "\t")
            return True
        
        elif (lex, tok) == ("if", "keyword"):
            self.parse_if()
            return True
        
        elif (lex, tok) == ("while", "keyword"):
            self.parse_while()
            return True
        
        elif (lex, tok) == ("do", "keyword"):
            self.parse_do_while()
            return True

        elif (lex, tok) == ("for", "keyword"):
            self.parse_for()
            return True
        
        elif (lex, tok) == ("int", "keyword"):
            self.parse_declaration()
            return True
        
        elif (lex, tok) == ("double", "keyword"):
            self.parse_declaration()
            return True
        
        elif (lex, tok) == ("bool", "keyword"):
            self.parse_declaration()
            return True

        elif (lex, tok) == ('}', 'breacket_op'):
            return False
        else:
            self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, "keyword"))

            return False
        
    def parse_declaration(self):
        self.column += 1
        print("\t" * self.column + "parse_declaration():")
        _, lex, tok = self.get_sym()

        if tok == "keyword" and lex in ("int", "double", "bool"):
            print('\t' * self.column + 'в рядку {0} - {1}'.format(lex, tok))
            self.num_row += 1

            if not self.parse_id_declaration_list():
                self.fail_parse("Невідповідність токенів", (self.num_row, lex, tok, 'id', "ident"))
            
            self.parse_token(";", "punct", "\t")

            return True
        else:
            return False
        
    def parse_id_declaration_list(self):
        self.column += 1
        print("\t" * self.column + "parse_id_declaration_list():")

        if not self.parse_id():
            return False

        while True:
            num_line, lex, tok = self.get_sym()

            if lex == ",":
                print('\t' * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
                self.parse_token(",", "punct", "\t")
                num_line, lex, tok = self.get_sym()

                if not self.parse_id():
                    self.fail_parse("Невідповідність токенів", (self.num_row, lex, tok, 'id', 'ident'))
            elif lex == ";":
                break
            else:
                self.fail_parse("Невідповідність токенів", (num_line, lex, tok, ';', 'punct'))
                return False
            
        return True

    def parse_for(self):
        self.column += 1
        print("\t" * self.column + "parse_for():")
        _, lex, tok = self.get_sym()
        if lex == "for" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op", "\t")
            self.parse_assign()
            self.parse_token(";", "punct", "\t")
            self.parse_bool_expr()
            self.parse_token(";", "punct", "\t")
            self.parse_assign()
            self.parse_token(")", "breacket_op", "\t")
            self.parse_token("{", "breacket_op", "\t")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op", "\t")
            return True
        else:
            return False

    def parse_do_while(self):
        self.column += 1
        print("\t" * self.column+ "parse_do_while():")
        _, lex, tok = self.get_sym()

        if lex == "do" and tok == "keyword":
            self.num_row += 1
            self.parse_token("{", "breacket_op", "\t")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op", "\t")
            self.parse_token("while", "keyword", "\t")
            self.parse_token("(", "breacket_op", '\t')
            self.parse_bool_expr()
            self.parse_token(")", "breacket_op", "\t")

            return True
        else: 
            return False
        
    def parse_while(self):
        self.column += 1
        print("\t" * self.column + "parse_while():")
        _, lex, tok = self.get_sym()

        if lex == "while" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op", '\t')
            self.parse_bool_expr()
            self.parse_token(")", "breacket_op", "\t")
            self.parse_token("{", "breacket_op", "\t")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op", "\t")

            return True
        else: 
            return False
        
    def parse_if(self):
        self.column += 1
        print("\t" * self.column + "parse_if():")
        num_line, lex, tok = self.get_sym()

        if lex == "if" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op", '\t')
            self.parse_bool_expr()
            self.parse_token(")", "breacket_op", "\t")
            self.parse_token("{", "breacket_op", "\t")
            self.parse_statement_list()
            
            # _, next_lex, next_tok = self.get_sym()

            # if next_lex == "}" and next_tok == "breacket_op":
            #     self.fail_parse("Тіло оператору не має бути порожнім", (num_line, lex, tok))
            # else:
            #     self.parse_statement_list()
            
            self.parse_token("}", "breacket_op", "\t")

            _, lex, tok = self.get_sym()

            if lex == "else" and tok == "keyword":
                self.parse_token("else", "keyword", "\t")
                self.parse_token("{", "breacket_op", "\t")
                self.parse_statement_list()
                self.parse_token("}", "breacket_op", "\t")

            return True
        else: 
            return False

    def parse_bool_expr(self):
        self.parse_expression()
        num_line, lex, tok = self.get_sym()

        if tok in ('rel_op'):
            self.num_row += 1
            print('\t' * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
        elif tok in ("boolval"):
            self.num_row += 1
            print('\t' * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
        else:
            self.fail_parse("Mismatch in BoolExpr", (num_line, lex, tok, 'rel_op'))
        
        self.parse_expression()

        return True

    def parse_print(self):
        self.column += 1
        print("\t" * self.column + "parse_print():")
        _, lex, tok = self.get_sym()

        if lex == "print" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op", "\t")
            self.parse_expression()
       #     if not self.parse_id():
       #         self.fail_parse("Невідповідність токенів", (self.num_row, lex, tok, 'id'))
            self.parse_token(")", "breacket_op", "\t")
            return True
        else:
            return False



    def parse_id_list(self):
        self.column += 1
        print("\t" * self.column + "parse_id_list():")

        if not self.parse_id():
            return False

        #while self.parse_id():
        while True:
            num_line, lex, tok = self.get_sym()
         #   print(num_line, lex, tok)
         #   self.num_row += 1
            if lex == ",":
                print('\t' * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
                self.parse_token(",", "punct", "\t")
                num_line, lex, tok = self.get_sym()
                if lex == ")":
                    self.fail_parse("Невідповідність токенів", (num_line, lex, tok, 'id', 'ident'))
                #self.num_row += 1
                #self.parse_token(",", "punct", "\t")
                if not self.parse_id():
                    self.fail_parse("Невідповідність токенів", (num_line, lex, tok, 'id', 'ident'))
              #  self.parse_id()
            elif lex == ")":
                break
            else:
                self.fail_parse("Невідповідність токенів", (num_line, lex, tok, ', or )', 'punct or breacket_op'))
                return False

              #  break
        return True

    def parse_id(self):
        self.column += 1
        print("\t" * self.column + "parse_id():")
        num_line, lex, tok = self.get_sym()

        if tok in "id":
            self.num_row += 1
            print('\t' * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
            return True
        else:
            return False

    def parse_readline(self):
        self.column += 1
        print("\t" * self.column + "parse_readline():")
        num_line, lex, tok = self.get_sym()
        if lex == "readline" and tok == "keyword":
            print('\t' * self.column + 'в рядку {0} - {1}'.format(lex, tok))
            self.num_row += 1
            self.parse_token("(", "breacket_op", "\t")
            # self.parse_id_list()
            if not self.parse_id_list():
                _, lex, tok = self.get_sym()
                self.fail_parse("Невідповідність токенів", (num_line, lex, tok, 'id', 'ident'))
            self.parse_token(")", "breacket_op", "\t")
            return True
        else:
            return False

    # Assign = Ident ‘=’ Expression ‘;’
    def parse_assign(self):
        self.column += 1
        print("\t" * self.column + "parse_assign():")
        num_line, lex, tok = self.get_sym()
        self.num_row += 1
        print("\t" * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))

        if self.parse_token("=", "assign_op", "\t\t\t\t\t"):
           # self.num_row += 1
            self.parse_expression()

            return True
        else:
            return False

    def parse_expression(self):
        self.column += 1
        print("\t" * self.column + "parse_expression():")
        self.parse_term()
        F = True

        while F:
            num_line, lex, tok = self.get_sym()
            if tok in ("add_op", "power_op"):
                self.num_row += 1
                print("\t" * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
                self.parse_term()
            else:
                F = False

        return True

    def parse_term(self):
        self.column += 1
        print("\t" * self.column + "parse_term():")
        self.parse_factor()
        F = True

        while F:
            num_line, lex, tok = self.get_sym()
            if tok in "mult_op":
                self.num_row += 1
                print("\t" * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
                self.parse_factor()
            else:
                F = False
        return True

    def parse_factor(self):
        self.column += 1
        print("\t" * self.column + "parse_factor():")
        num_line, lex, tok = self.get_sym()

        print("\t" * self.column + "parseFactor(): рядок: {0} (lex, tok): {1}".format(num_line, (lex, tok)))
        if tok in ("intnum", "doublenum", "id"):
            self.num_row += 1
            print("\t" * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
        elif lex == "(":
            self.num_row += 1
            self.parse_expression()
            self.parse_token(")", "breacket_op", "\t"*7)
            print("\t" * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
        elif lex == "-" and tok == "add_op":
            self.num_row += 1
            self.parse_factor()
        elif lex == "^" and tok == "power_op":
            self.num_row += 1
            self.parse_power()

        elif lex == "true" or lex == "false":
            self.num_row += 1
            return True

        else:
            self.fail_parse("Невiдповiднiсть у Expression.Factor", (num_line, lex, tok, "int, double, bool, id або (Expression)"))

        return True
    
    def parse_power(self):
        self.column += 1
        print("\t" * self.column + "parse_power():")
        self.parse_factor()
        num_line, lex, tok = self.get_sym()

        if tok == "power_op" and lex == "^":
            self.num_row += 1
            print("\t" * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
            self.parse_factor()
        else:
            self.fail_parse("Невiдповiднiсть у Power", (num_line, lex, tok, "^ Factor"))


lex()
print('-' * 30)
print('tableOfSymb:{0}'.format(table_of_sym))
print('-' * 30)
parser = Parser().parse_main()
"""
    def parse_id(self):
        print("\t" * 6 + "parse_id():")
        while True:
            num_line, lex, tok = self.get_sym()
            if tok in "id":
                self.num_row += 1
                print('\t' * 7 + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
            else:
                break
        return True
        
            def parse_readline(self):
        print("\t" * 4 + "parse_readline():")
        _, lex, tok = self.get_sym()
        if lex == "readline" and tok == "keyword":
            print('\t' * 7 + 'в рядку {0} - {1}'.format(lex, tok))
            self.num_row += 1
            self.parse_token("(", "breacket_op", "\t")
            # self.parse_id_list()
            if not self.parse_id_list():
                self.fail_parse("Невідповідність токенів", (self.num_row, lex, tok, 'id'))
            self.parse_token(")", "breacket_op", "\t")
            return True
        else:
            return False
"""
"""
    def parse_ind_expression(self):
        print("\t" * 4 + "parse_ind_expression():")
        _, lex, tok = self.get_sym()
        if lex == "int" or lex == "double":
            self.num_row += 1
            print('\t' * 5 + 'в рядку {0} - {1}'.format(lex, tok))
            self.parse_id()

            self.parse_assign()

        #    self.parse_expression()

            self.parse_token(";", "punct", "\t")
            self.parse_bool_expr()
            self.parse_token(";", "punct", "\t")
            self.parse_id()
            self.parse_assign()

       #     self.parse_expression()

            return True
        else:
            return False
"""
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
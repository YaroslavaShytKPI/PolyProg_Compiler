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
            self.parse_token("main", "keyword")
            self.parse_token("{", "breacket_op")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op")
            print("Parser: Синтаксичний аналiз завершився успiшно")

            return True
        
        except SystemExit as e:
            print(f"Parses: Аварійне завершення програми з кодом {0}".format(e))

    def parse_token(self, lexeme, token):
        if self.num_row > len(table_of_sym):
            self.fail_parse("Неочікуваний кінець програми", (lexeme, token, self.num_row))

        num_line, lex, tok = self.get_sym()
        self.num_row += 1

        if (lex, tok) == (lexeme, token):
            print(" " * self.column + "parseToken: В рядку {0} токен {1}".format(num_line, (lexeme, token)))
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
            print("Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з "
                  "номером {1}.\n\t Очікувалось - {0}".format((lexeme, token), self.num_row))
            exit(1001)

        if str == "get_sym(): Неочікуваний кінець програми":
            self.num_row = tuple
            print("Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з "
                  "номером {0}. \n\t Останній запис - {1}".format(
                  self.num_row, table_of_sym[self.num_row-1]))
            exit(1002)

        elif str == "Невідповідність токенів":
            (num_line, lexeme, token, lex, tok) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - ({3}, {4}).".
                  format(num_line, lexeme, token, lex, tok))
            exit(1)

        elif str == "Невідповідність інструкцій":
            print('heree')
            (num_line, lex, tok, expected) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.".format(
                num_line, lex, tok, expected))
            exit(2)

        elif str == "Невiдповiднiсть у Expression.Factor":
            (num_line, lex, tok, expected) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.".format(
                num_line, lex, tok, expected))
            exit(3)

        elif str == "Невідповідність в BoolExpr" or str == "Невiдповiднiсть у Power":
            (num_line, lex, tok, expected) = tuple
            print("Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2}). \n\t Очікувався - {3}.".format(
                num_line, lex, tok, expected))
            exit(4)

    # StatementList = Statement {';' Statement}
    def parse_statement_list(self):
        print(" " * self.column + "parse_statement_list():")
        while self.parse_statement():
            pass
        
        return True


    # Statement = Assign | Inp | Out | ForStatement |DoWhileStatement| IfStatement
    def parse_statement(self):
        self.column = 2
        print(" " * self.column + "parse_statement():")
        num_line, lex, tok = self.get_sym()

        if tok == "id":
            self.parse_assign()
            self.parse_token(";", "punct")
            return True

        elif (lex, tok) == ("print", "keyword"):
            self.parse_print()
            self.parse_token(";", "punct")
            return True

        elif (lex, tok) == ("readline", "keyword"):
            self.parse_readline()
            self.parse_token(";", "punct")
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
        print(" " * self.column + "parse_declaration():")
        num_line, lex, tok = self.get_sym()

        if tok == "keyword" and lex in ("int", "double", "bool"):
            print(" " * self.column + 'в рядку {0} - {1}'.format(lex, tok))
            self.num_row += 1

            if not self.parse_id_declaration_list():
                num_line, lex, tok = self.get_sym()
                self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, 'id'))
            
            self.parse_token(";", "punct")

            return True
        else:
            return False


    def parse_id_declaration_list(self):
        self.column += 1
        print(" " * self.column + "parse_id_declaration_list():")

        if not self.parse_id():
            return False

        while True:
            num_line, lex, tok = self.get_sym()

            if lex == ",":
                print(" " * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
                self.parse_token(",", "punct")
                num_line, lex, tok = self.get_sym()

                if not self.parse_id():
                    self.fail_parse("Невідповідність інструкцій", (self.num_row, lex, tok, 'id'))
            elif lex == ";":
                break
            else:
                self.fail_parse("Невідповідність токенів", (num_line, lex, tok, ';', 'punct'))
                return False
            
        return True


    # ForStatement = for '(' Assign';' BoolExp';' Assign ')' '{' StatementList '}'
    def parse_for(self):
        self.column += 1
        print(" " * self.column + "parse_for():")
        _, lex, tok = self.get_sym()
        if lex == "for" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op")
            self.parse_assign()
            self.parse_token(";", "punct")
            self.parse_bool_expr()
            self.parse_token(";", "punct")
            self.parse_assign()
            self.parse_token(")", "breacket_op")
            self.parse_token("{", "breacket_op")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op")
            return True
        else:
            return False


    # DoWhileStatement = do '{' StatementList '}' while '(' BoolExp ')'
    def parse_do_while(self):
        self.column += 1
        print(" " * self.column+ "parse_do_while():")
        _, lex, tok = self.get_sym()

        if lex == "do" and tok == "keyword":
            self.num_row += 1
            self.parse_token("{", "breacket_op")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op")
            self.parse_token("while", "keyword")
            self.parse_token("(", "breacket_op")
            self.parse_bool_expr()
            self.parse_token(")", "breacket_op")

            return True
        else: 
            return False


    # WhileStatement = while '(' BoolExp ')' '{' StatementList '}' 
    def parse_while(self):
        self.column += 1
        print(" " * self.column + "parse_while():")
        _, lex, tok = self.get_sym()

        if lex == "while" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op")
            self.parse_bool_expr()
            self.parse_token(")", "breacket_op")
            self.parse_token("{", "breacket_op")
            self.parse_statement_list()
            self.parse_token("}", "breacket_op")

            return True
        else: 
            return False


    # IfStatement = if '(' BoolExp ')' '{' StatementList '}'
    def parse_if(self):
        self.column += 1
        print(" " * self.column + "parse_if():")
        num_line, lex, tok = self.get_sym()

        if lex == "if" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op")
            self.parse_bool_expr()
            self.parse_token(")", "breacket_op")
            self.parse_token("{", "breacket_op")
            self.parse_statement_list()            
            self.parse_token("}", "breacket_op")

            _, lex, tok = self.get_sym()

            if lex == "else" and tok == "keyword":
                self.parse_token("else", "keyword")
                self.parse_token("{", "breacket_op")
                self.parse_statement_list()
                self.parse_token("}", "breacket_op")

            return True
        else: 
            return False

    def parse_bool_expr(self):
        self.parse_expression()
        num_line, lex, tok = self.get_sym()
        valid_rel_ops = ['<', '>', '<=', '>=', '==', '!=']

        if tok in ('rel_op'):
            self.num_row += 1
            if lex not in valid_rel_ops:
                self.fail_parse("Невідповідність в BoolExpr", (num_line, lex, tok, 'rel_op'))

            if lex in ('==', '!='):
                self.parse_expression()
            else:
                left_exp_type = self.get_exp_type(-2)
                right_exp_type = self.get_exp_type(0)
                if (left_exp_type == 'boolval' and right_exp_type == 'boolval') or \
                   (left_exp_type != 'boolval' and right_exp_type != 'boolval'):
                    self.parse_expression()
                else:
                    num_line, lex, tok = self.get_sym()
                    self.fail_parse("Невідповідність в BoolExpr", (num_line, lex, tok, 'id'))

        elif tok in ("boolval"):
            self.num_row += 1
        else:
            self.fail_parse("Невідповідність в BoolExpr", (num_line, lex, tok, 'rel_op'))

        return True

    def get_exp_type(self, n):
        if self.num_row < 2:
            return
        prev_row = table_of_sym[self.num_row + n]
        _, prev_lex, prev_tok, _ = prev_row
        if prev_tok in ('intnum', 'doublenum'):
            return 'numeric'
        elif (prev_lex, prev_tok) in [('true', 'boolval'), ('false', 'boolval')]:
            return 'boolval'
        elif prev_tok == "id":
            return "id"
        else:
            return 'unknown'

    def check_bool_context(self):
        if self.num_row < 2:
            return False
        prev_row = table_of_sym[self.num_row - 1]
        prev_lex = prev_row[1]
        return prev_lex in ("==", "!=")



    # Output = print '(' id ')'
    def parse_print(self):
        self.column += 1
        print(" " * self.column + "parse_print():")
        _, lex, tok = self.get_sym()

        if lex == "print" and tok == "keyword":
            self.num_row += 1
            self.parse_token("(", "breacket_op")
            self.parse_expression()
       #     if not self.parse_id():
       #         self.fail_parse("Невідповідність токенів", (self.num_row, lex, tok, 'id'))
            self.parse_token(")", "breacket_op")
            return True
        else:
            return False


    def parse_id_list(self):
        self.column += 1
        print(" " * self.column + "parse_id_list():")

        if not self.parse_id():
            return False

        #while self.parse_id():
        while True:
            num_line, lex, tok = self.get_sym()
         #   print(num_line, lex, tok)
         #   self.num_row += 1
            if lex == ",":
                print(" " * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
                self.parse_token(",", "punct")
                num_line, lex, tok = self.get_sym()
                if lex == ")":
                    self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, 'id'))
                #self.num_row += 1
                #self.parse_token(",", "punct")
                if not self.parse_id():
                    self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, 'id'))
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
        print(" " * self.column + "parse_id():")
        num_line, lex, tok = self.get_sym()

        if tok in "id":
            self.num_row += 1
            print(" " * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
            return True
        else:
            return False


    # Input = readline '(' IdList ')'
    def parse_readline(self):
        self.column += 1
        print(" " * self.column + "parse_readline():")
        num_line, lex, tok = self.get_sym()
        if lex == "readline" and tok == "keyword":
            print(" " * self.column + 'в рядку {0} - {1}'.format(lex, tok))
            self.num_row += 1
            self.parse_token("(", "breacket_op")
            # self.parse_id_list()
            if not self.parse_id_list():
                _, lex, tok = self.get_sym()
                self.fail_parse("Невідповідність інструкцій", (num_line, lex, tok, 'id'))
            self.parse_token(")", "breacket_op")
            return True
        else:
            return False


    # Assign = Ident ‘=’ Expression ‘;’
    def parse_assign(self):
        self.column += 1
        print(" " * self.column + "parse_assign():")
        num_line, lex, tok = self.get_sym()
        self.num_row += 1
        print(" " * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))

        if self.parse_token("=", "assign_op"):
           # self.num_row += 1
            self.parse_expression()
            return True
        else:
            return False


    def parse_expression(self):
        self.column += 1
        print(" " * self.column + "parse_expression():")
        self.parse_term()
        F = True

        while F:
            num_line, lex, tok = self.get_sym()
            if tok in ("add_op", "power_op", "mult_op"):
                self.num_row += 1
                print(" " * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
                self.parse_term()
            else:
                F = False

        return True


    def parse_term(self):
        self.column += 1
        print(" " * self.column + "parse_term():")
        self.parse_factor()
        F = True

        while F:
            num_line, lex, tok = self.get_sym()
            if tok in "mult_op":
                self.num_row += 1
                print(" " * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
                self.parse_factor()
            if lex in ("true", "false"):
                self.fail_parse("Невідповідність в BoolExpr",
                                (num_line, lex, tok, "intnum, doublenum, id або (Expression)"))

            else:
                F = False
        return True


    def parse_factor(self):
        self.column += 1
        print(" " * self.column + "parse_factor():")
        num_line, lex, tok = self.get_sym()

        print(" " * self.column + "parseFactor(): рядок: {0} (lex, tok): {1}".format(num_line, (lex, tok)))
        if tok in ("intnum", "doublenum", "id"):
            self.num_row += 1
            print(" " * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
        elif lex == "(":
            self.num_row += 1
            self.parse_expression()
            self.parse_token(")", "breacket_op")
            print(" " * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
        elif lex == "-" and tok == "add_op":
            self.num_row += 1
            self.parse_factor()
        elif lex == "^" and tok == "power_op":
            self.num_row += 1
            self.parse_power()

     #   elif lex == "true" or lex == "false":
      #      self.num_row += 1
      #      return True
        elif lex == "true" or lex == "false":
            # Перевірка контексту для правильного використання true та false
            if self.check_bool_context():
                self.num_row += 1
                num_line, lex, tok = self.get_sym()
                if tok in ("add_op", "mult_op", "power_op"):
                    self.fail_parse("Невідповідність в BoolExpr",
                                    (num_line, lex, tok, "rel_op)"))
                print(" " * self.column + 'в рядку {0} - {1}'.format(num_line, (lex, tok)))
                return True
            else:
                self.fail_parse("Невідповідність в BoolExpr",
                                (num_line, lex, tok, "intnum, doublenum, id або (Expression)"))

        else:
            self.fail_parse("Невiдповiднiсть у Expression.Factor", (num_line, lex, tok, "intnum, doublenum, id або (Expression)"))

        return True

    def check_bool_context(self):
        if self.num_row < 2:
            return False
        prev_row = table_of_sym[self.num_row - 1]
        prev_lex = prev_row[1]
        verdad = prev_lex in ("==", "!=", "<", ">", "<=" ">=") or prev_row[1] == "="
        return prev_lex in ("==", "!=", "<", ">", "<=" ">=", "(") or prev_row[1] == "="

    def parse_power(self):
        self.column += 1
        print(" " * self.column + "parse_power():")
        self.parse_factor()
        num_line, lex, tok = self.get_sym()

        if tok == "power_op" and lex == "^":
            self.num_row += 1
            print(" " * self.column + "в рядку {0} - {1}".format(num_line, (lex, tok)))
            self.parse_factor()
        else:
            self.fail_parse("Невiдповiднiсть у Power", (num_line, lex, tok, "^ Factor"))


lex()
print('-' * 30)
print('tableOfSymb:{0}'.format(table_of_sym))
print('-' * 30)
parser = Parser().parse_main()

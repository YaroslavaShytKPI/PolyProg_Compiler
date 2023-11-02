from tocken_table import *   #from PolyProg_Compiler.analyzer.tocken_table import *
from state_transition_function import *   #from PolyProg_Compiler.analyzer.state_transition_function import *

table_of_id = {}     # таблиця ідентифікаторів
table_of_const = {}  # таблиць констант
table_of_sym = {}    # таблиця символів програми (таблиця розбору)

state = init_state   # поточний стан


f = open('test_files/program.pol', 'r')  # зчитування файлу програми мовою PolyProg   f = open('../test_files/test.pol', 'r')
source_code = f.read()
f.close()

F_success = (True, 'Lexer')   # F_success - ознака успішності розбору

len_code = len(source_code) - 1  # номер останнього символу у файлі з кодом програми
num_line = 1                     # лексичний аналіз починаємо з першого рядка
num_char = -1                    # з першого символу (в Python нумерація - з 0)
char = ''                        # ще не брали жодного символу
lexeme = ''                      # ще не починали розпізнавати лексеми


# початок лексичного аналізу
def lex():
    global state, num_line, char, lexeme, num_char, F_success
    try:
        print(f"L№  lex        token       id ")
        while num_char < len_code:
            char = next_char()
            class_ch = class_of_char(char)
            state = next_state(state, class_ch)
            if is_final(state):
                processing()
            elif state == init_state:
                lexeme = ''
            else:
                lexeme += char
        print('-' * 30)
        print('Lexer: Лексичний аналіз завершено успішно')
    except SystemExit as e:
        F_success = (False, 'Lexer')
        print('-' * 30)
        print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))


# збільшення лічильника номеру прочитаного символу
def next_char():
    global num_char
    num_char += 1
    return source_code[num_char]


# визначення класу символу
def class_of_char(char):
    if char in 'abcdefghijklmnopqrstuvwxyz':
        result = 'Letter'
    elif char in '0123456789':
        result = 'Digit'
    elif char == '.':
        result = 'Dot'
    elif char in '\t ':
        result = 'WhiteSpace'
    elif char in '\n':
        result = 'EndOfLine'
    elif char in ':=*+-/^(){}<>;!,':
        result = char
    else:
        result = 'символ не належить алфавіту'
    return result


# визначення наступного стану
def next_state(state, class_ch):
    try:
        return stf[(state, class_ch)]
    except KeyError:
        return stf[(state, 'OtherChar')]


# перевірка на заключний стан
def is_final(state):
    if (state in F):
        return True
    else:
        return False


# обробка станів
def processing():
    global state, lexeme, char, num_line, num_char, table_of_sym

    if state in (14, 19):
        num_line += 1
        lexeme = ''
        state = init_state

    if state in (2, 4, 6, 9, 12, 20):
        token = get_token(state, lexeme)

        if token != 'keyword':
            index = index_id_const(state, lexeme)
            print('-' * 30)
            print(f"{num_line:<3d} {lexeme:<10s} {token:<10s} {index}")
            table_of_sym[len(table_of_sym) + 1] = (num_line, lexeme, token, index)
        else:
            print('-' * 30)
            print(f"{num_line:<3d} {lexeme:<10s} {token:<10s}")
            table_of_sym[len(table_of_sym) + 1] = (num_line, lexeme, token, '')

        lexeme = ''
        num_char = put_char_back(num_char)
        state = init_state

    if state in (14, 8, 11, 13, 16):
        lexeme += char
        token = get_token(state, lexeme)
        print('-' * 30)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
        table_of_sym[len(table_of_sym) + 1] = (num_line, lexeme, token, '')
        lexeme = ''
        state = init_state

    if state in F_error:
        fail()


# отримання токена з таблиці
def get_token(state, lexeme):
    try:
        return token_table[lexeme]
    except KeyError:
        return tok_state_table[state]


# визначення індексу лексеми
def index_id_const(state, lexeme):
    indx = 0
    if state == 2:
        if lexeme in table_of_id:
            indx = table_of_id[lexeme]
        else:
            indx = len(table_of_id) + 1
            table_of_id[lexeme] = indx
    if state in (4, 6):
        if lexeme in table_of_const:
            if isinstance(table_of_const[lexeme], tuple):
                indx = table_of_const[lexeme][1]
            else:
                indx = table_of_const[lexeme]
        else:
            indx = len(table_of_const) + 1
            table_of_const[lexeme] = (tok_state_table[state], indx)
    return indx


# зменшення лічильника номеру прочитаного символу
def put_char_back(num_char):
    return num_char - 1


# обробка стану-помилки
def fail():
    global state, num_line, char

    if state == 100:
        print('Lexer: у рядку ', num_line, ' неіснуючий символ ' + char)
        exit(100)

    if state == 101:
        print('Lexer: у рядку ', num_line, ' не очiкувався символ класу \'Letter\'')
        exit(101)

    if state == 102:
        print('Lexer: у рядку ', num_line, ' неочікуваний символ ' + char)
        exit(102)


# запуск лексичного аналізатора
#lex()

# Таблиці: розбору, ідентифікаторів та констант
#print('-' * 50)
#print('Table Of Symbols: {0}'.format(table_of_sym))
#print('Table Of IDs    : {0}'.format(table_of_id))
#print('Table Of Const  : {0}'.format(table_of_const))

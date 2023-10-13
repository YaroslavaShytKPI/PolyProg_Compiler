stf = {(0, 'WhiteSpace'): 0, \
       (0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'OtherChar'): 2, \
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'OtherChar'): 4, \
       (3, 'Dot'): 5, (5, 'Digit'): 5, (5, 'OtherChar'): 6, \
       (3, 'Letter'): 101, \
       (5, 'Letter'): 101, \
       (0, '>'): 7, (0, '<'): 7, (7, '='): 8, \
       (7, 'OtherChar'): 9, \
       (0, '='): 10, (10, '='): 11, \
       (10, 'OtherChar'): 12, \
       (0, '+'): 8, (0, '-'): 8, (0, '*'): 8, (0, '/'): 8, (0, '('): 8, \
       (0, ')'): 8, (0, '}'): 8, (0, '{'): 8, (0, '^'): 8, (0, ':'): 8, (0, ';'): 8, \
       (0, 'EndOfLine'): 14, \
       (0, '!'): 15, (15, '='): 16, \
       (15, 'OtherChar'): 102, \
       (0, 'OtherChar'): 100,
       }

initState = 0  # q0 - стартовий стан
F = {2, 4, 6, 8, 9, 11, 12, 13, 14, 16, 100, 101, 102}  # множина заключних станів
Fstar = {2, 4, 6}  # зірочка
Ferror = {100, 101, 102}  # обробка помилок

tokenTable = {'main': 'keyword', 'int': 'keyword', 'double': 'keyword', \
              'bool': 'keyword', 'for': 'keyword', 'if': 'keyword', \
              'else': 'keyword', 'print': 'keyword', 'readLine': 'keyword', \
              'do': 'keyword', 'while': 'keyword', 'true': 'boolval', \
              'false': 'boolval', '=': 'assign_op', '+': 'add_op', \
              '-': 'add_op', '*': 'mult_op', '/': 'mult_op', \
              '^': 'power_op', '<': 'rel_op', '<=': 'rel_op', '>': 'rel_op', \
              '>=': 'rel_op', '==': 'rel_op', '!=': 'rel_op', \
              '(': 'breacket_op', ')': 'breacket_op', '{': 'breacket_op', \
              '}': 'breacket_op', '.': 'punct', ',': 'punct', ':': 'punct', \
              ';': 'punct', '\t': 'ws', ' ': 'ws', '\n': 'eol'}
tokStateTable = {2: 'id', 4: 'intnum', 6: 'doublenum'}

tableOfId = {}  # Таблиця ідентифікаторів
tableOfConst = {}  # Таблиць констант
tableOfSymb = {}  # Таблиця символів програми (таблиця розбору)

state = initState  # поточний стан

f = open('program.pol', 'r')
sourceCode = f.read()
f.close()

# FSuccess - ознака успішності розбору
FSuccess = (True, 'Lexer')

lenCode = len(sourceCode) - 1  # номер останнього символа у файлі з кодом програми
numLine = 1  # лексичний аналіз починаємо з першого рядка
numChar = -1  # з першого символа (в Python'і нумерація - з 0)
char = ''  # ще не брали жодного символа
lexeme = ''  # ще не починали розпізнавати лексеми


def lex():
    global state, numLine, char, lexeme, numChar, FSuccess
    try:
        while numChar < lenCode:
            char = nextChar()
            classCh = classOfChar(char)
            state = nextState(state, classCh)
            if (is_final(state)):
                processing()
            elif state == initState:
                lexeme = ''
            else:
                lexeme += char
        print('Lexer: Лексичний аналіз завершено успішно')
    except SystemExit as e:
        FSuccess = (False, 'Lexer')
        print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))


def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]


def classOfChar(char):
    if char in 'abcdefghijklmnopqrstuvwxyz':
        result = 'Letter'
    elif char in '0123456789':
        result = 'Digit'
    elif char in '.':
        result = 'Dot'
    elif char in '\t ':
        result = 'WhiteSpace'
    elif char in '\n':
        result = 'EndOfLine'
    elif char in ':=*+-/^(){}<>;!':
        result = char
    else:
        result = 'символ не належить алфавіту'

    return result


def nextState(state, classCh):
    global numLine
    if classCh == 'EndOfLine':
        numLine += 1
    try:
        return stf[(state, classCh)]
    except KeyError:
        return stf[(state, 'OtherChar')]


def is_final(state):
    if (state in F):
        return True
    else:
        return False


def processing():
    global state, lexeme, char, numLine, numChar, tableOfSymb

    if state == 9:
        numLine += 1
        state = initState

    if state in (2, 4, 6, 12):
        token = getToken(state, lexeme)

        if token != 'keyword':
            index = indexIdConst(state, lexeme)
            print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(numLine, lexeme, token, index))
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:
            print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')

        lexeme = ''
        numChar = putCharBack(numChar)
        state = initState

    if state in (14, 8, 11, 13, 16):
        lexeme += char
        token = getToken(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = initState

    if state in Ferror:
        fail()


def getToken(state, lexeme):
    try:
        return tokenTable[lexeme]
    except KeyError:
        return tokStateTable[state]


def indexIdConst(state, lexeme):
    indx = 0
    if state == 2:
        indx = tableOfId.get(lexeme)

        if indx is None:
            indx = len(tableOfId) + 1
            tableOfId[lexeme] = indx

    if state in (4, 6):
        indx = tableOfConst.get(lexeme)

        if indx is None:
            indx = len(tableOfConst) + 1
            tableOfConst[lexeme] = (tokStateTable[state], indx)

    return indx


def putCharBack(numChar):
    return numChar - 1


def fail():
    global state, numLine, char

    if state == 100:
        print('Lexer: у рядку ', numLine, ' неочікуваний символ ' + char)
        exit(100)

    if state == 101:
        print('Lexer: у рядку ', numLine, ' очiкувався символ =, а не ' + char)
        exit(101)

    if state == 102:
        print('Lexer: у рядку ', numLine, ' не очiкувався символ класу \'Letter\'')
        exit(102)


# запуск лексичного аналізатора
lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-' * 30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('tableOfId:{0}'.format(tableOfId))
print('tableOfConst:{0}'.format(tableOfConst))

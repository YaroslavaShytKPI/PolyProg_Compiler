def print_res(table_of_label, table_of_vars, postfix_code):
    print('-' * 15)
    print(' Таблиця міток\n\nLabel\tValue')
    for label, value in table_of_label.items():
        print('{0}\t{1}'.format(label, value))
    print('-' * 15)

    print('-' * 35)
    print(' Таблиця ідентифікаторів\n\nIndex\tIdent\tType\tValue')
    for ident, info in table_of_vars.items():
        print('{0}\t{1}\t{2}\t{3}'.format(info[0], ident, info[1], info[2]))
    print('-' * 35)

    print('-' * 35)
    print(' Код програми у постфiкснiй формi (ПОЛIЗ):\n\n№\tValue')
    count = 0
    for value in postfix_code:
        count += 1
        print('{0}\t{1}'.format(count, postfix_code[count - 1]))
    print('-' * 35)

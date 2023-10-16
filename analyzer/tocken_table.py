token_table = {
    # головна функція програми
    'main': 'keyword',
    # типи даних
    'int': 'keyword', 'double': 'keyword', 'bool': 'keyword',
    # цикли
    'for': 'keyword', 'do': 'keyword', 'while': 'keyword',
    # ввід-вивід
    'print': 'keyword', 'readline': 'keyword',
    # розгалуження
    'if': 'keyword', 'else': 'keyword',
    # булеві значення
    'true': 'boolval', 'false': 'boolval',
    # математичні оператори
    '+': 'add_op', '-': 'add_op',
    '*': 'mult_op', '/': 'mult_op',
    '^': 'power_op',
    # оператор присвоєння
    '=': 'assign_op',
    # оператори відношення
    '==': 'rel_op', '!=': 'rel_op',
    '<': 'rel_op', '<=': 'rel_op',
    '>': 'rel_op', '>=': 'rel_op',
    # дужки
    '(': 'breacket_op', ')': 'breacket_op',
    '{': 'breacket_op', '}': 'breacket_op',
    # пунктуаційні знаки
    '.': 'punct', ',': 'punct', ';': 'punct',
    # коментарі
    '//': 'comment',
    # пробіл
    '\t': 'ws', ' ': 'ws',
    # перехід на новий рядок
    '\n': 'eol'
}

tok_state_table = {2: 'id', 4: 'intnum', 6: 'doublenum'}
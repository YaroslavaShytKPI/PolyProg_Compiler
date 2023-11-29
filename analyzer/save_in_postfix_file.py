
def process_data(table_of_vars, table_of_label, table_of_const, postfix_code):
    # Знайти максимальну довжину ключа в кожній категорії
    max_var_length = max(len(var) for var in table_of_vars.keys())
    max_label_length = max(len(label) for label in table_of_label.keys())
    max_const_length = max(len(value) for value in table_of_const.keys())

    # Обробка таблиці змінних
    vars_data = "\n".join([f"   {var.ljust(max_var_length)}     {info[1]}" for var, info in table_of_vars.items()])

    # Обробка таблиці міток
    labels_data = "\n".join([f"   {label.ljust(max_label_length)}    {info}" for label, info in table_of_label.items()])

    # Обробка таблиці констант
    constants_data = "\n".join([f"   {value.ljust(max_const_length)}     {info[0][:-3]}" for value, info in table_of_const.items()])

    # Знайти максимальну довжину для кожного стовпця у розділі .code()
    max_code_lengths = [max(len(str(item[i])) for item in postfix_code) for i in range(2)]

    # Обробка коду
    code_data = "\n".join([f"   {item[0].ljust(max_code_lengths[0])}     {item[1]}" for item in postfix_code])

    return vars_data, labels_data, constants_data, code_data

def save_data_to_file(table_of_vars, table_of_label, table_of_const, postfix_code, filename):
    vars_data, labels_data, constants_data, code_data = process_data(table_of_vars, table_of_label, table_of_const, postfix_code)
    template = f"""\
.target: Postfix Machine
.version: 0.1

.vars(
{vars_data}
)

.labels(
{labels_data}
)

.constants(
{constants_data}
)

.code(
{code_data}
)
"""

    with open(f"analyzer/psm/test_files/{filename}.postfix", 'w') as file:
        file.write(template)
    print(f'Постфікс-код збережено до {filename}.postfix')

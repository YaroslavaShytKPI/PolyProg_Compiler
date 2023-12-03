from translator import *

def saveCIL(fileName):
  fname = fileName + ".il"
  f = open(fname, 'w')
  header = """// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly """ +fileName+ """
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module """ +fileName+ """.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
"""
  # f.write(header)

  cntVars = len(table_of_vars)      
  localVars = ""
  comma = ","
  for x in table_of_vars:
    index,tp,_ = table_of_vars[x][0], table_of_vars[x][1], table_of_vars[x][2]
    if tp == 'int': tpil = 'int32' 
    elif tp == 'double': tpil = 'float32'
    else: tpil = 'bool'
    if index == cntVars: comma = "\n     )"
    localVars += "       [{0}]  {1} {2}".format(index-1,tpil, x) + comma + "\n"
  # print((x,a))
  entrypoint = """
   .entrypoint
   //.maxstack  8\n"""
  code = ""
  current_token = None

  for token, token_type in postfix_code:
    if current_token:
        if token_type == 'jump':
            code += f"   br    {current_token}\n"
        elif token_type == 'jf':
            code += f"   brfalse    {current_token}\n"
        else:
            code += f"{current_token}:\n"
        current_token = None
        continue
    
    if token_type == 'label':
        current_token = token
        continue
    
    if token_type == 'l-val':
        code += f"   ldloca    {token}\n"
    elif token_type == 'r-val' or token_type == 'id':
        code += f"   ldloc    {token}\n"
    elif token_type == 'int':
        code += f"   ldc.i4    {token}\n"
    elif token_type == 'double':
        code += f"   ldc.r4    {token}\n"
    elif token_type == 'assign_op':
        code += f"   stind.{('i4' if token == 'int' else 'r4')}\n"
    elif token_type == 'print':
        code += f"   call    void [mscorlib]System.Console::WriteLine()\n"
    elif token_type == 'readline':
        code += f"   call    string [mscorlib]System.Console::ReadLine()\n"
    elif token_type == 'rel_op':
        if token == '>':
            code += "   cgt\n"
        elif token == '<':
            code += "   clt\n"
        elif token == '>=':
            code += "    clt\n    ldc.i4.0\n    ceq\n"
        elif token == '<=':
            code += "    cgt\n    ldc.i4.0\n    ceq\n"
        elif token == '==':
            code += "   ceq\n"
        elif token == '!=':
            code += "    ceq\n    ldc.i4.0\n    ceq\n"
    elif token_type == 'mult_op' or token_type == 'add_op':
        if token == '+':
            code += "   add\n"
        elif token == '-':
            code += "   sub\n"
        elif token == '*':
            code += "   mul\n"
        elif token == '/':
            code += "   div\n"
    elif token_type == 'power_op':
        # code += "    conv.r8\n      conv.r8\n      pow\n      conv.r4\n"
        code += "   pow\n"
    elif token_type == 'bool':
        code += f"   ldstr \"{token}\"\n"
    elif token_type == 'negate_op':
        code += "   neg\n"
    else:
        code += f"{token}!!!"
    
  # виведення значень змінних
  values = ""
  for x in table_of_vars:
    values += "\t" + 'ldstr "' + x + ' = "\n'
    values += "\t" + "call void [mscorlib]System.Console::Write(string) \n"
    _,tp,_ = table_of_vars[x][0], table_of_vars[x][1], table_of_vars[x][2]
    tp += '32'
    values += "\t" + "ldloc  " + x + "\n"
    values += "\t" + "call void [mscorlib]System.Console::WriteLine(" +tp + ") \n" 
    
  f.write(header + localVars + entrypoint +code + values +"\tret    \n}\n}")
  f.close()
  print(f"IL-програма для CLR збережена у файлі {fname}")

saveCIL("test1")
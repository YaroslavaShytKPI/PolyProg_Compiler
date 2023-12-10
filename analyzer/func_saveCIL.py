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
    if tp == 'double': tpil = 'float32' 
    else: tpil = 'int32'
    if index == cntVars: comma = ""
    localVars += "       [{0}]  {1} {2}".format(index-1,tpil, x) + comma + "\n"
  localVars += "     )"
  # print((x,a))
  entrypoint = """
   .entrypoint
   //.maxstack  8\n"""
  code = ""
  current_token = None
  prev = ''
  prev_id = ''

  for token, token_type in postfix_code:
    if token_type == 'jump':
        # code += f"{current_token}:\n"
        code += f"   br    {current_token}\n"
        current_token = None
        continue
    elif token_type == 'jf':
        # code += f"{current_token}:\n"
        code += f"   brfalse    {current_token}\n"
        current_token = None
        continue
    elif token_type == 'colon':
        code += f"{current_token}:\n"
        current_token = None
        continue
    
    elif token_type == 'label':
        current_token = token
        continue
    
    elif token_type == 'l-val':
        prev = table_of_vars[token][1]
        code += f"   ldloca    {token}\n"
    
    elif token_type == 'r-val':
        # prev = table_of_vars[token][1]
        type = table_of_vars[token][1]
        # if type == 'int':
        #     code += '   conv.r4\n'
        
        code += f"   ldloc    {token}\n"

        # if type == 'int' and prev == 'float':
        #     code += '   conv.r4\n'
        
        # code += f'   ldloc {token}\n'

        prev = type
    
    elif token_type == 'id':
        prev_id = token
        type = table_of_vars[token][1]
        prev = type

    elif token_type == 'int':
        code += f"   ldc.i4    {token}\n"
        if prev == 'double':
            code += '   conv.r4\n'
            prev = 'double'
        else:
            prev = 'int'

    elif token_type == 'double':
        if prev == 'int':
            code += '\tconv.r4\n'
        
        code += f"   ldc.r4    {token}\n"

        prev = 'double'
    
    elif token_type == 'string':
        code += f'\tldstr {token}\n'
        prev = 'string'

    elif token_type == 'assign_op':
        code += f"   stind.{('i4' if prev == 'int' else 'r4')}\n"
    elif token_type == 'print':
        if prev == 'int':
            type = prev + '32'
        elif prev == 'double':
            type = 'float32'
        else:
            type = prev
        code += f'   call void [mscorlib]System.Console::WriteLine({type})\n'
        prev = ''
    elif token_type == 'readline':
        code += f"   call    string [mscorlib]System.Console::ReadLine()\n"
        
        code += f'   call {prev}32 [mscorlib]System.{"Int32" if prev == "int" else "Double32"}::Parse(string)\n'
        
        code += f'   stloc {prev_id}\n'

        prev = ''
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
            if prev == 'int':
                code += "   conv.r4\n"
            code += "   mul\n"
            prev = 'double'
        elif token == '/':
            if prev == 'int':
                code += "   conv.r4\n"
            code += "   div\n"
            prev = 'double'
        elif token == 'NEG':
            code += "   neg\n"
    elif token_type == 'power_op':
        if prev == 'int':
            code += '   conv.r8\n'
        code += "   call   float64 [mscorlib]System.Math::Pow(float64, float64)\n"
        if prev == 'int':
            code += '   conv.i4\n'
    elif token_type == 'bool':
        code += f"   ldstr \"{token}\"\n"
        prev = "bool"
    else:
        pass
    
  # виведення значень змінних
  # values = ""
  # typ = ""
  # for x in table_of_vars:
  #   values += "\t" + 'ldstr "' + x + ' = "\n'
  #   values += "\t" + "call void [mscorlib]System.Console::Write(string) \n"
  #   _,tp,_ = table_of_vars[x][0], table_of_vars[x][1], table_of_vars[x][2]
  #   if tp == 'int':
  #       typ = 'int32'
  #   elif tp == 'double':
  #       typ = 'float32'
  #   elif tp == 'bool':
  #       typ = 'bool'
  #   values += "\t" + "ldloc  " + x + "\n"
  #   values += "\t" + "call void [mscorlib]System.Console::WriteLine(" +typ + ") \n" 
    
  f.write(header + localVars + entrypoint + code +"\tret    \n}\n}")   # + values
  f.close()
  print(f"IL-програма для CLR збережена у файлі {fname}")

saveCIL("test1")
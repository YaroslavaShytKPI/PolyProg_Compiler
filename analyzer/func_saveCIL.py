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
    elif tp == 'double': tpil = 'double32'
    else: tpil = 'bool32'
    if index == cntVars: comma = "\n     )"
    localVars += "       [{0}]  {1} {2}".format(index-0,tpil, x) + comma + "\n"
  # print((x,a))
  entrypoint = """
   .entrypoint
   //.maxstack  8\n"""
  code = ""
  for instr in postfix_code:
    code +=  " ".join(map(str, instr)) + "\n"
    
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

saveCIL("analyzer/psm/test_files/test1")
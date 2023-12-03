// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly analyzer/psm/test_files/test1
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module analyzer/psm/test_files/test1.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  int32 x,
       [1]  bool ind,
       [2]  float32 num,
       [3]  int32 i,
       [4]  float32 res
     )

   .entrypoint
   //.maxstack  8
   ldloca    x
   ldc.i4    3
   stind.r4
   ldloca    i
   ldloc    x
   stind.r4
   ldloc    i
   call    void [mscorlib]System.Console::WriteLine()
   ldloca    num
   ldc.r4    3.3
   stind.r4
   ldloc    x
   call    string [mscorlib]System.Console::ReadLine()
   ldloca    i
   ldc.i4    1
   stind.r4
   ldloc    i
   ldc.i4    0
   cgt
   brfalse    m4
   br    m2
   ldloca    i
   ldloc    i
   ldc.i4    1
   sub
   stind.r4
   br    m1
   ldloc    i
   ldc.i4    2
   ceq
   brfalse    m5
   ldstr "true"
   call    void [mscorlib]System.Console::WriteLine()
m5:
   ldloc    i
   call    void [mscorlib]System.Console::WriteLine()
   br    m3
   ldloca    x
   ldc.i4    0
   stind.r4
m7:
   ldc.i4    0
    cgt
    ldc.i4.0
    ceq
   brfalse    m8
:!!!   ldloca    x
   ldloc    x
   ldc.i4    1
   add
   stind.r4
   ldloc    x
   call    void [mscorlib]System.Console::WriteLine()
   br    m7
m8:
   ldloc    num
   ldc.r4    1.1
   cgt
   brfalse    m9
   ldloc    num
   call    void [mscorlib]System.Console::WriteLine()
   br    m10
m9:
   ldloc    num
   ldloc    num
   mul
   call    void [mscorlib]System.Console::WriteLine()
m10:
   ldloca    res
   ldloc    num
   ldc.i4    15
   add
   stind.r4
   ldloc    res
   ldc.i4    15
    ceq
    ldc.i4.0
    ceq
   brfalse    m13
   ldloc    res
   call    void [mscorlib]System.Console::WriteLine()
m13:
   ldloc    res
   ldc.i4    3
   clt
   brfalse    m15
   ldstr "true"
   call    void [mscorlib]System.Console::WriteLine()
m15:
   ldloc    x
   ldc.i4    3
    cgt
    ldc.i4.0
    ceq
   brfalse    m17
   ldloca    res
   ldc.r4    10.1
   ldc.i4    5
   pow
   stind.r4
m17:
   ldloca    x
   ldloc    x
   ldc.i4    6
   add
   stind.r4
   ldloca    x
   ldloc    x
   ldc.i4    6
   sub
   stind.r4
   ldloca    num
   ldloc    num
   ldc.i4    1
   sub
   stind.r4
   ldloc    num
   ldc.i4    0
    clt
    ldc.i4.0
    ceq
   brfalse    m12
   br    m11
	ldstr "x = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  x
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "ind = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  ind
	call void [mscorlib]System.Console::WriteLine(bool32) 
	ldstr "num = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  num
	call void [mscorlib]System.Console::WriteLine(double32) 
	ldstr "i = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  i
	call void [mscorlib]System.Console::WriteLine(int32) 
	ldstr "res = "
	call void [mscorlib]System.Console::Write(string) 
	ldloc  res
	call void [mscorlib]System.Console::WriteLine(double32) 
	ret    
}
}
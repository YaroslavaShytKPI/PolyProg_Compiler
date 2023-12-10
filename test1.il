// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly test1
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module test1.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  int32 x,
       [1]  int32 ind,
       [2]  float32 num,
       [3]  int32 i,
       [4]  float32 res
     )
   .entrypoint
   //.maxstack  8
   ldloca    x
   ldc.i4    2
   ldc.i4    2
   ldc.i4    3
   conv.r8
   call   float64 [mscorlib]System.Math::Pow(float64, float64)
   conv.i4
   conv.r8
   call   float64 [mscorlib]System.Math::Pow(float64, float64)
   conv.i4
   stind.i4
   ldloca    i
   ldloc    x
   stind.i4
   ldloc    i
   call void [mscorlib]System.Console::WriteLine(int32)
   ldloca    num
   ldc.r4    4.0
   stind.r4
   call    string [mscorlib]System.Console::ReadLine()
   call int32 [mscorlib]System.Int32::Parse(string)
   stloc x
   ldloca    res
   ldloc    num
   ldloc    x
   conv.r4
   div
   stind.r4
   ldloc    res
   call void [mscorlib]System.Console::WriteLine(float32)
   ldloca    i
   ldc.i4    1
   stind.i4
   br    m2
m1:
   ldloc    i
   ldc.i4    0
   cgt
   brfalse    m4
   br    m2
m3:
   ldloca    i
   ldloc    i
   ldc.i4    1
   sub
   stind.i4
   br    m1
m2:
   ldloc    i
   ldc.i4    2
   ceq
   brfalse    m5
   ldstr "true"
   call void [mscorlib]System.Console::WriteLine(bool)
m5:
   ldloc    i
   call void [mscorlib]System.Console::WriteLine(int32)
   br    m3
m4:
   ldloca    x
   ldc.i4    0
   stind.i4
m7:
   ldloc    x
   ldc.i4    0
    cgt
    ldc.i4.0
    ceq
   brfalse    m8
   ldloca    x
   ldloc    x
   ldc.i4    1
   add
   stind.i4
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(int32)
   br    m7
m8:
   ldloc    num
   ldc.r4    1.1
   cgt
   brfalse    m9
   ldloc    num
   call void [mscorlib]System.Console::WriteLine(float32)
   br    m10
m9:
   ldloc    num
   ldloc    num
   mul
   call void [mscorlib]System.Console::WriteLine(float32)
m10:
m11:
   ldloca    res
   ldloc    num
   ldc.i4    15
   conv.r4
   add
   stind.r4
   ldloc    res
   ldc.i4    15
   conv.r4
    ceq
    ldc.i4.0
    ceq
   brfalse    m13
   ldloc    res
   call void [mscorlib]System.Console::WriteLine(float32)
m13:
   ldloc    res
   ldc.i4    3
   conv.r4
   clt
   brfalse    m15
   ldloc    res
   call void [mscorlib]System.Console::WriteLine(float32)
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
   conv.r4
   call   float64 [mscorlib]System.Math::Pow(float64, float64)
   stind.r4
m17:
   ldloca    x
   ldloc    x
   ldc.i4    6
   add
   stind.i4
   ldloca    x
   ldloc    x
   ldc.i4    6
   sub
   stind.i4
   ldloca    num
   ldloc    num
   ldc.i4    1
   conv.r4
   sub
   stind.r4
   ldloc    num
   ldc.i4    0
   conv.r4
    clt
    ldc.i4.0
    ceq
   brfalse    m12
   br    m11
m12:
	ret    
}
}
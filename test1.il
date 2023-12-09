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
       [0]  float32 i
     )

   .entrypoint
   //.maxstack  8
   ldloca    i
   ldc.r4    2.3
   stind.r4
   br    m2
m1:
   ldloc    i
   ldc.i4    5
   conv.r4
    cgt
    ldc.i4.0
    ceq
   brfalse    m4
   br    m2
m3:
   ldloca    i
   ldloc    i
   ldc.i4    1
   conv.r4
   add
   stind.r4
   br    m1
m2:
   ldloc    i
   call void [mscorlib]System.Console::WriteLine(float32)
   br    m3
m4:
	ret    
}
}
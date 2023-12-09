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
       [0]  int32 x
     )

   .entrypoint
   //.maxstack  8
   ldloca    x
   ldc.i4    0
   stind.i4
m1:
   ldloca    x
   ldloc    x
   ldc.i4    1
   add
   stind.i4
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(int32)
   ldloc    x
   ldc.i4    5
   cgt
   brfalse    m2
   br    m1
m2:
	ret    
}
}
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
       [1]  int32 x,
       [2]  bool ind,
       [3]  float32 num,
       [4]  int32 i,
       [5]  float32 res
     )

   .entrypoint
   //.maxstack  8
x l-val
3 int
= assign_op
i l-val
x r-val
= assign_op
i id
OUT print
num l-val
3.3 double
= assign_op
x id
IN readline
i l-val
1 int
= assign_op
i r-val
0 int
> rel_op
m4 label
JF jf
m2 label
JMP jump
i l-val
i r-val
1 int
- add_op
= assign_op
m1 label
JMP jump
i r-val
2 int
== rel_op
m5 label
JF jf
true bool
OUT print
m5 label
: colon
i id
OUT print
m3 label
JMP jump
x l-val
0 int
= assign_op
m7 label
x r-val
0 int
<= rel_op
m8 label
JF jf
: colon
x l-val
x r-val
1 int
+ add_op
= assign_op
x id
OUT print
m7 label
JMP jump
m8 label
: colon
num r-val
1.1 double
> rel_op
m9 label
JF jf
num id
OUT print
m10 label
JMP jump
m9 label
: colon
num id
num r-val
* mult_op
OUT print
m10 label
: colon
res l-val
num r-val
15 int
+ add_op
= assign_op
res r-val
15 int
!= rel_op
m13 label
JF jf
res id
OUT print
m13 label
: colon
res r-val
3 int
< rel_op
m15 label
JF jf
true bool
OUT print
m15 label
: colon
x r-val
3 int
<= rel_op
m17 label
JF jf
res l-val
10.1 double
5 int
^ power_op
= assign_op
m17 label
: colon
x l-val
x r-val
6 int
+ add_op
= assign_op
x l-val
x r-val
6 int
- add_op
= assign_op
num l-val
num r-val
1 int
- add_op
= assign_op
num r-val
0 int
>= rel_op
m12 label
JF jf
m11 label
JMP jump
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
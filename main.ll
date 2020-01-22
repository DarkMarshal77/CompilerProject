@.str = private constant [3 x i8] c"%d\00"

define i32 @main() 
{
entry:
  %str = getelementptr inbounds [3 x i8]* @.str, i32 0, i32 0
  %0 = alloca i32, align 4
  %1 = call i32 (i8*, ...)* @scanf(i8* %str, i32* %0)
  %2 = load i32* %0, align 4
  %call = call i32 (i8*, ...)* @printf(i8* %str, i32 %2)
  ret i32 0
}

declare i32 @printf(i8*, ...)
declare i32 @scanf(i8*, ...)

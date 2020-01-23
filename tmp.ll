; simple code of main.ll

@.str = private constant [3 x i8] c"%d\00"

define i32 @main() #0
{
  %str = getelementptr inbounds [3 x i8], [3 x i8]* @.str, i32 0, i32 0
  %1 = alloca i32, align 4
  %2 = call i32 (i8*, ...) @scanf(i8* %str, i32* %1)
  %3 = load i32, i32* %1, align 4
  %call = call i32 (i8*, ...) @printf(i8* %str, i32 %3)
  ret i32 0
}

declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1

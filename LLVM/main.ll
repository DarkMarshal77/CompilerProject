@.const0 = private constant [3 x i8] c"%c\00"


define i32 @main()
{
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%1 = call i32 (i8*, ...) @printf(i8* %str0, i8 99)
ret i32 0
}

declare i32 @printf(i8*, ...) #1

@.const0 = private constant [3 x i8] c"%d\00"
@.const1 = private constant [3 x i8] c"%c\00"


define i32 @main()
{
%1 = alloca i32, align 4
store i32 11, i32* %1
br label %L0
L0:
%2 = load i32, i32* %1
%3 = icmp sle i32 %2, 10
br i1 %3, label %L1, label %L2
L1:
%4 = alloca i32, align 4
store i32 1, i32* %4
%5 = load i32, i32* %4
%6 = add nsw i32 %5, 1
store i32 %6, i32* %4
%7 = load i32, i32* %4
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%8 = call i32 (i8*, ...) @printf(i8* %str0, i32 %7)
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%9 = call i32 (i8*, ...) @printf(i8* %str1, i8 10)
br label %L0
L2:
%10 = add nsw i32 2, 3
ret i32 %10
}

declare i32 @printf(i8*, ...)

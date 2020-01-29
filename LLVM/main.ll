@.const0 = private constant [3 x i8] c"%d\00"
@.const1 = private constant [3 x i8] c"%c\00"


define i32 @main()
{
%a_ptr = alloca i32, align 4
store i32 5, i32* %a_ptr
br label %L0
L0:
%1 = load i32, i32* %a_ptr
%2 = icmp ne i32 %1, 0
br i1 %2, label %L1, label %L2
L1:
%3 = load i32, i32* %a_ptr
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%4 = call i32 (i8*, ...) @printf(i8* %str0, i32 %3)
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%5 = call i32 (i8*, ...) @printf(i8* %str1, i8 99)
%6 = load i32, i32* %a_ptr
%7 = sub nsw i32 %6, 1
store i32 %7, i32* %a_ptr
br label %L0
L2:
ret i32 0
}

declare i32 @printf(i8*, ...) #1

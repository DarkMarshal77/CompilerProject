@.const0 = private constant [3 x i8] c"%d\00"
define i32 @main(i32 %first_ptr, double %second_ptr)
{
%a_ptr = alloca i32, align 4
store i32 1, i32* %a_ptr
%b_ptr = alloca i32, align 4
store i32 2, i32* %b_ptr
%1 = load i32, i32* %a_ptr
%2 = icmp eq i32 %1, 1
br i1 %2, label %L0, label %L1
L0:
store i32 1, i32* %b_ptr
br label %L1
L1:
%3 = load i32, i32* %b_ptr
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%4 = call i32 (i8*, ...) @printf(i8* %str0, i32 %3)
ret i32 0
}
declare i32 @printf(i8*, ...) #1

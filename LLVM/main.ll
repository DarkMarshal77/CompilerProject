@.const0 = private constant [3 x i8] c"%d\00"
@.const1 = private constant [3 x i8] c"%f\00"
define i32 @main(i32 %first_ptr, double %second_ptr)
{
%a_ptr = alloca i32, align 4
store i32 12, i32* %a_ptr
%bool_ptr = alloca i1, align 1
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%1 = alloca i32, align 4
%2 = call i32 (i8*, ...) @scanf(i8* %str0, i32* %1)
%3 = load i32, i32* %1
%4 = icmp ne i32 %3, 0
store i1 %4, i1* %bool_ptr
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%5 = call i32 (i8*, ...) @printf(i8* %str1, double %second_ptr)
ret i32 0
}
declare i32 @scanf(i8*, ...) #1
declare i32 @printf(i8*, ...) #1

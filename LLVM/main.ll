@.const0 = private constant [5 x i8] c"%s\0A\0D\00"
@.const1 = private constant [5 x i8] c"ahff\00"
@.const2 = private constant [5 x i8] c"%c\0A\0D\00"
@.const3 = private constant [5 x i8] c"%f\0A\0D\00"
@.const4 = private constant [5 x i8] c"%d\0A\0D\00"
define i32 @main() #0
{
%str0 = getelementptr inbounds [5 x i8], [5 x i8]* @.const0, i32 0, i32 0
%var_str_ptr1 = getelementptr inbounds [5 x i8], [5 x i8]* @.const1, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str0, i8* %var_str_ptr1)
%str2 = getelementptr inbounds [5 x i8], [5 x i8]* @.const2, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str2, i8 102)
%str3 = getelementptr inbounds [5 x i8], [5 x i8]* @.const3, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str3, double 12.212)
%str4 = getelementptr inbounds [5 x i8], [5 x i8]* @.const4, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str4, i32 515)
ret i32 0
}
declare i32 @printf(i8*, ...) #1

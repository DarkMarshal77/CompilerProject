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

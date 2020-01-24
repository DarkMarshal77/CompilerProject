define i32 @main() #0
{
%str = getelementptr inbounds [5 x i8], [5 x i8]* @.const0, i32 0, i32 0
%var_str_ptr = getelementptr inbounds [5 x i8], [5 x i8]* @.const1, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str, i8* %var_str_ptr)
ret i32 0
}

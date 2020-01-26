@a_ptr = global double 0.0
@b_ptr = global i8 0
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%var_str_ptr1 = getelementptr inbounds [8 x i8], [8 x i8]* @.const1, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str0, i8* %var_str_ptr1)
store double 99.0, double* @a_ptr

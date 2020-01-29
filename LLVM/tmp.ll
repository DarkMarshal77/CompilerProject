define i32 @main()
{
%1 = alloca i1, align 1
store i1 true, i1* %1
%2 = load i1, i1* %1
br i1 %2, label %L0, label %L1
L0:
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%var_str_ptr1 = getelementptr inbounds [4 x i8], [4 x i8]* @.const1, i32 0, i32 0
%3 = call i32 (i8*, ...) @printf(i8* %str0, i8* %var_str_ptr1)
br label %L2
L1:
%str2 = getelementptr inbounds [3 x i8], [3 x i8]* @.const2, i32 0, i32 0
%var_str_ptr3 = getelementptr inbounds [3 x i8], [3 x i8]* @.const3, i32 0, i32 0
%4 = call i32 (i8*, ...) @printf(i8* %str2, i8* %var_str_ptr3)
br label %L2
L2:
ret i32 0
}


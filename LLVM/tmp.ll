define i32 @main()
{
%a_ptr = alloca i32, align 4
store i32 1, i32* %a_ptr
br label %L0
L0:
%1 = load i32, i32* %a_ptr
%2 = icmp sle i32 %1, 10
br i1 %2, label %L1, label %L2
L1:
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%var_str_ptr1 = getelementptr inbounds [7 x i8], [7 x i8]* @.const1, i32 0, i32 0
%3 = call i32 (i8*, ...) @printf(i8* %str0, i8* %var_str_ptr1)
%4 = load i32, i32* %a_ptr
%str2 = getelementptr inbounds [3 x i8], [3 x i8]* @.const2, i32 0, i32 0
%5 = call i32 (i8*, ...) @printf(i8* %str2, i32 %4)
%6 = load i32, i32* %a_ptr
%7 = add nsw i32 %6, 1
store i32 %7, i32* %a_ptr
%str3 = getelementptr inbounds [3 x i8], [3 x i8]* @.const3, i32 0, i32 0
%8 = call i32 (i8*, ...) @printf(i8* %str3, i8 10)
br label %L0
L2:
ret i32 0
}


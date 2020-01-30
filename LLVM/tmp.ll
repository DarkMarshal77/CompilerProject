define i32 @fib(i32 %n_ptr)
{
%tmp_1 = icmp eq i32 %n_ptr, 1
%tmp_2 = icmp eq i32 %n_ptr, 2
%tmp_3 = or i1 %tmp_1, %tmp_2
br i1 %tmp_3, label %L0, label %L1
L0:
ret i32 1
br label %L2
L1:
%tmp_5 = sub i32 %n_ptr, 2
%tmp_6 = call i32 (i32) @fib (i32 %tmp_5)
%tmp_7 = sub i32 %n_ptr, 1
%tmp_8 = call i32 (i32) @fib (i32 %tmp_7)
%tmp_9 = add i32 %tmp_6, %tmp_8
ret i32 %tmp_9
br label %L2
L2:
ret i32 10000
}

define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 1, i32* %1
br label %L3
L3:
%tmp_3 = load i32, i32* %1
%tmp_4 = icmp sle i32 %tmp_3, 20
br i1 %tmp_4, label %L4, label %L5
L4:
%tmp_5 = load i32, i32* %1
%tmp_6 = call i32 (i32) @fib (i32 %tmp_5)
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_7 = call i32 (i8*, ...) @printf(i8* %str0, i32 %tmp_6)
%tmp_8 = load i32, i32* %1
%tmp_9 = add i32 %tmp_8, 1
store i32 %tmp_9, i32* %1
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_10 = call i32 (i8*, ...) @printf(i8* %str1, i8 10)
br label %L3
L5:
ret i32 0
ret i32 10000
}


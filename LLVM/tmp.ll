define i32 @main()
{
%1 = alloca i32, align 4
store i32 1, i32* %1
br label %L0
L0:
%2 = load i32, i32* %1
%3 = icmp sle i32 %2, 10
br i1 %3, label %L1, label %L2
L1:
%4 = load i32, i32* %1
%5 = add nsw i32 %4, 1
store i32 %5, i32* %1
%6 = load i32, i32* %1
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%7 = call i32 (i8*, ...) @printf(i8* %str0, i32 %6)
br label %L0
L2:
ret i32 0
}


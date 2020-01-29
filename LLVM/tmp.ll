define i32 @main()
{
%1 = icmp sge i32 2, 2
%2 = zext i1 %1 to i32
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%3 = call i32 (i8*, ...) @printf(i8* %str0, i32 %2)
ret i32 0
}


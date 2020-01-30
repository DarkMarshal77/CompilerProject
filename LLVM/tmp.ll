define i32 @f()
{
ret i32 0
br label %L0
L0:
ret i32 0
}

define void @g()
{
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_1 = call i32 (i8*, ...) @printf(i8* %str0, i32 1)
ret void 
}

define i32 @main()
{
%tmp_1 = call i32() @f ()
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_2 = call i32 (i8*, ...) @printf(i8* %str1, i32 %tmp_1)
call void() @g ()
br label %L1
L1:
ret i32 0
}


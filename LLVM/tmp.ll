define i8* @fun()
{
%tmp_1 = alloca i8*, align 8
%tmp_2 = getelementptr inbounds [9 x i8], [9 x i8]* @.const0, i32 0, i32 0
store i8* %tmp_2, i8** %tmp_1
%tmp_3 = alloca i8*, align 8
%tmp_4 = load i8*, i8** %tmp_1
store i8* %tmp_4, i8** %tmp_3
%tmp_5 = load i8*, i8** %tmp_3
ret i8* %tmp_5
br label %L0
L0:
ret i8* getelementptr inbounds ([1 x i8], [1 x i8]* @.str_func_def_ret, i32 0, i32 0)
}

define i32 @main()
{
%tmp_1 = call i8*() @fun ()
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_2 = call i32 (i8*, ...) @printf(i8* %str1, i8* %tmp_1)
ret i32 0
br label %L1
L1:
ret i32 0
}


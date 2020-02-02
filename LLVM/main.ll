@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [32 x i8] c"hello world!\0Aashkan is here...\0D\00"
@.const1 = private constant [3 x i8] c"%s\00"


define i32 @main()
{
%tmp_1 = alloca i8*, align 8
%tmp_2 = getelementptr inbounds [32 x i8], [32 x i8]* @.const0, i32 0, i32 0
store i8* %tmp_2, i8** %tmp_1
%tmp_3 = load i8*, i8** %tmp_1
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_4 = call i32 (i8*, ...) @printf(i8* %str1, i8* %tmp_3)
br label %L0
L0:
ret i32 0
}

declare i32 @printf(i8*, ...)

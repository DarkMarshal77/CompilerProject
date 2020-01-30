@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [9 x i8] c"dfhdbfhj\00"
@.const1 = private constant [7 x i8] c"dddddd\00"
@.const2 = private constant [3 x i8] c"%s\00"
@.const3 = private constant [3 x i8] c"%s\00"


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
%tmp_1 = alloca i8*, align 8
%tmp_2 = getelementptr inbounds [7 x i8], [7 x i8]* @.const1, i32 0, i32 0
store i8* %tmp_2, i8** %tmp_1
%tmp_3 = alloca i8*, align 8
%tmp_4 = load i8*, i8** %tmp_1
store i8* %tmp_4, i8** %tmp_3
%str2 = getelementptr inbounds [3 x i8], [3 x i8]* @.const2, i32 0, i32 0
%tmp_5 = alloca [512 x i8], align 16%tmp_6 = getelementptr inbounds [512 x i8], [512 x i8]* %tmp_5, i32 0, i32 0
%tmp_7 = call i32 (i8*, ...) @scanf(i8* %str2, i8* %tmp_6)
store i8* %tmp_6, i8** %tmp_3
%tmp_9 = load i8*, i8** %tmp_3
%str3 = getelementptr inbounds [3 x i8], [3 x i8]* @.const3, i32 0, i32 0
%tmp_10 = call i32 (i8*, ...) @printf(i8* %str3, i8* %tmp_9)
ret i32 0
br label %L1
L1:
ret i32 0
}

declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)

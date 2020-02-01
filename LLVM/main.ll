@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [3 x i8] c"%d\00"


define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 2, i32* %tmp_1
%tmp_2 = load i32, i32* %tmp_1
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_3 = call i32 (i8*, ...) @printf(i8* %str0, i32 %tmp_2)
br label %L0
L0:
ret i32 0
}

declare i32 @printf(i8*, ...)

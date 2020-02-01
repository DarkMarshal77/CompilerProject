@.str_func_def_ret = private constant [1 x i8] c"\00"


define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 10, i32* %tmp_1
%tmp_2 = alloca i32, align 4
store i32 1, i32* %tmp_2
%tmp_3 = load i32, i32* %tmp_1
%tmp_4 = add i32 %tmp_3, 5
%tmp_5 = mul i32 6, %tmp_4
%tmp_6 = alloca i32, i32 %tmp_5, align 16
br label %L0
L0:
ret i32 0
}


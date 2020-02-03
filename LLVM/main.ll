@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [3 x i8] c"%f\00"


define i32 @main()
{
%tmp_1 = alloca double, align 4
store double 1.5, double* %tmp_1
%tmp_2 = alloca double, align 4
%tmp_3 = sub i32 0, 18
%tmp_4 = add i32 %tmp_3, 2
%tmp_5 = sub i32 %tmp_4, 1
%tmp_6 = sitofp i32 %tmp_5 to double
store double %tmp_6, double* %tmp_2
%tmp_7 = load double, double* %tmp_2
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_8 = call i32 (i8*, ...) @printf(i8* %str0, double %tmp_7)
br label %L0
L0:
ret i32 0
}

declare i32 @printf(i8*, ...)

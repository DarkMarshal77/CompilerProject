define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 2, i32* %tmp_1
%tmp_2 = alloca i32, align 4
store i32 3, i32* %tmp_2
%tmp_3 = alloca double, align 4
store double 4.1, double* %tmp_3
%tmp_4 = alloca double, align 4
store double 5.9, double* %tmp_4
%tmp_5 = alloca i8, align 1
store i8 97, i8* %tmp_5
%tmp_6 = alloca i8, align 1
store i8 98, i8* %tmp_6
%tmp_7 = alloca i1, align 1
store i1 true, i1* %tmp_7
%tmp_8 = alloca i1, align 1
store i1 false, i1* %tmp_8
%tmp_9 = load i32, i32* %tmp_2
%tmp_10 = load double, double* %tmp_3
%tmp_11 = sitofp i32 %tmp_9 to double
%tmp_12 = fmul double %tmp_11, %tmp_10
%tmp_13 = load i32, i32* %tmp_1
%tmp_14 = sitofp i32 %tmp_13 to double
%tmp_15 = fadd double %tmp_14, %tmp_12
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_16 = call i32 (i8*, ...) @printf(i8* %str0, double %tmp_15)
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_17 = call i32 (i8*, ...) @printf(i8* %str1, i8 10)
%tmp_18 = load i32, i32* %tmp_1
%tmp_19 = load i32, i32* %tmp_2
%tmp_20 = add i32 %tmp_18, %tmp_19
%tmp_21 = load double, double* %tmp_3
%tmp_22 = sitofp i32 %tmp_20 to double
%tmp_23 = fmul double %tmp_22, %tmp_21
%str2 = getelementptr inbounds [3 x i8], [3 x i8]* @.const2, i32 0, i32 0
%tmp_24 = call i32 (i8*, ...) @printf(i8* %str2, double %tmp_23)
br label %L0
L0:
ret i32 0
}


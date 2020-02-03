@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [3 x i8] c"%d\00"


define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 3, i32* %tmp_1
%tmp_2 = alloca i32, align 4
store i32 4, i32* %tmp_2
%tmp_3 = load i32, i32* %tmp_1
%tmp_4 = load i32, i32* %tmp_2
%tmp_5 = mul i32 %tmp_4, %tmp_3
%tmp_6 = alloca i32, i32 %tmp_5, align 16
%tmp_7 = alloca i32, align 4
store i32 0, i32* %tmp_7
%tmp_8 = alloca i32, align 4
store i32 0, i32* %tmp_8
br label %L0
L0:
%tmp_10 = load i32, i32* %tmp_7
%tmp_11 = load i32, i32* %tmp_1
%tmp_12 = icmp slt i32 %tmp_10, %tmp_11
br i1 %tmp_12, label %L1, label %L2
L1:
br label %L3
L3:
%tmp_14 = load i32, i32* %tmp_8
%tmp_15 = load i32, i32* %tmp_2
%tmp_16 = icmp slt i32 %tmp_14, %tmp_15
br i1 %tmp_16, label %L4, label %L5
L4:
%tmp_17 = load i32, i32* %tmp_8
%tmp_18 = mul i32 %tmp_17, %tmp_4
%tmp_19 = getelementptr inbounds i32, i32* %tmp_6, i32 %tmp_18
%tmp_20 = load i32, i32* %tmp_7
%tmp_21 = getelementptr inbounds i32, i32* %tmp_19, i32 %tmp_20
%tmp_22 = load i32, i32* %tmp_8
%tmp_23 = mul i32 2, %tmp_22
%tmp_24 = load i32, i32* %tmp_7
%tmp_25 = add i32 %tmp_24, %tmp_23
store i32 %tmp_25, i32* %tmp_21
%tmp_26 = load i32, i32* %tmp_8
%tmp_27 = add i32 %tmp_26, 1
store i32 %tmp_27, i32* %tmp_8
br label %L3
L5:
%tmp_29 = load i32, i32* %tmp_7
%tmp_30 = add i32 %tmp_29, 1
store i32 %tmp_30, i32* %tmp_7
br label %L0
L2:
store i32 0, i32* %tmp_7
store i32 0, i32* %tmp_8
br label %L6
L6:
%tmp_33 = load i32, i32* %tmp_7
%tmp_34 = load i32, i32* %tmp_1
%tmp_35 = icmp slt i32 %tmp_33, %tmp_34
br i1 %tmp_35, label %L7, label %L8
L7:
br label %L9
L9:
%tmp_37 = load i32, i32* %tmp_8
%tmp_38 = load i32, i32* %tmp_2
%tmp_39 = icmp slt i32 %tmp_37, %tmp_38
br i1 %tmp_39, label %L10, label %L11
L10:
%tmp_40 = load i32, i32* %tmp_8
%tmp_41 = mul i32 %tmp_40, %tmp_4
%tmp_42 = getelementptr inbounds i32, i32* %tmp_6, i32 %tmp_41
%tmp_43 = load i32, i32* %tmp_7
%tmp_44 = getelementptr inbounds i32, i32* %tmp_42, i32 %tmp_43
%tmp_45 = load i32, i32* %tmp_44
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_46 = call i32 (i8*, ...) @printf(i8* %str0, i32 %tmp_45)
%tmp_47 = load i32, i32* %tmp_8
%tmp_48 = add i32 %tmp_47, 1
store i32 %tmp_48, i32* %tmp_8
br label %L9
L11:
%tmp_50 = load i32, i32* %tmp_7
%tmp_51 = add i32 %tmp_50, 1
store i32 %tmp_51, i32* %tmp_7
br label %L6
L8:
br label %L12
L12:
ret i32 0
}

declare i32 @printf(i8*, ...)

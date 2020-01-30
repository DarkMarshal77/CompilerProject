@.const0 = private constant [3 x i8] c"%c\00"
@.const1 = private constant [3 x i8] c"%d\00"


define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 1, i32* %tmp_1
%tmp_2 = alloca double, align 4
store double 3.0, double* %tmp_2
%tmp_3 = alloca i8, align 1
store i8 99, i8* %tmp_3
%tmp_4 = load i32, i32* %tmp_1
%tmp_5 = icmp eq i32 %tmp_4, 1
br i1 %tmp_5, label %L0, label %L1
L0:
%tmp_6 = load double, double* %tmp_2
%tmp_7 = fcmp oeq double %tmp_6, 3.0
br i1 %tmp_7, label %L2, label %L3
L2:
br label %L4
L4:
%tmp_9 = load i8, i8* %tmp_3
%tmp_10 = zext i8 %tmp_9 to i32
%tmp_11 = icmp ne i32 %tmp_10, 106
br i1 %tmp_11, label %L5, label %L6
L5:
%tmp_12 = load i8, i8* %tmp_3
%tmp_13 = zext i8 %tmp_12 to i32
%tmp_14 = add i32 %tmp_13, 1
%tmp_15 = trunc i32 %tmp_14 to i8
store i8 %tmp_15, i8* %tmp_3
br label %L4
L6:
%tmp_17 = load i8, i8* %tmp_3
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_18 = call i32 (i8*, ...) @printf(i8* %str0, i8 %tmp_17)
br label %L3
L3:
br label %L7
L1:
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_21 = call i32 (i8*, ...) @printf(i8* %str1, i32 -1)
br label %L7
L7:
br label %L8
L8:
ret i32 0
}

declare i32 @printf(i8*, ...)

@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [3 x i8] c"%d\00"
@.const1 = private constant [2 x i8] c"\0A\00"
@.const2 = private constant [3 x i8] c"%s\00"
@.const3 = private constant [3 x i8] c"%d\00"


define i32 @main()
{
%tmp_1 = alloca i32, i32 4, align 16
%tmp_2 = alloca i32, align 4
store i32 0, i32* %tmp_2
%tmp_3 = getelementptr inbounds i32, i32* %tmp_1, i32 0
store i32 1, i32* %tmp_3
%tmp_4 = getelementptr inbounds i32, i32* %tmp_1, i32 1
store i32 2, i32* %tmp_4
%tmp_5 = getelementptr inbounds i32, i32* %tmp_1, i32 0
%tmp_6 = getelementptr inbounds i32, i32* %tmp_1, i32 1
%tmp_7 = getelementptr inbounds i32, i32* %tmp_1, i32 1
%tmp_8 = getelementptr inbounds i32, i32* %tmp_1, i32 0
%tmp_9 = load i32, i32* %tmp_7
%tmp_10 = load i32, i32* %tmp_8
store i32 %tmp_9, i32* %tmp_5
store i32 %tmp_10, i32* %tmp_6
%tmp_11 = getelementptr inbounds i32, i32* %tmp_1, i32 0
%tmp_12 = load i32, i32* %tmp_11
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_13 = call i32 (i8*, ...) @printf(i8* %str0, i32 %tmp_12)
%tmp_14 = getelementptr inbounds [2 x i8], [2 x i8]* @.const1, i32 0, i32 0
%str2 = getelementptr inbounds [3 x i8], [3 x i8]* @.const2, i32 0, i32 0
%tmp_15 = call i32 (i8*, ...) @printf(i8* %str2, i8* %tmp_14)
%tmp_16 = getelementptr inbounds i32, i32* %tmp_1, i32 1
%tmp_17 = load i32, i32* %tmp_16
%str3 = getelementptr inbounds [3 x i8], [3 x i8]* @.const3, i32 0, i32 0
%tmp_18 = call i32 (i8*, ...) @printf(i8* %str3, i32 %tmp_17)
br label %L0
L0:
ret i32 0
}

declare i32 @printf(i8*, ...)

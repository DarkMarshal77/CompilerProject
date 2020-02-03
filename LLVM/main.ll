@.str_func_def_ret = private constant [1 x i8] c"\00"
@.const0 = private constant [6 x i8] c"salam\00"
@.const1 = private constant [7 x i8] c"ashkan\00"
@.const2 = private constant [8 x i8] c"%tmp_11\00"
@.const3 = private constant [8 x i8] c"%tmp_12\00"
@.const4 = private constant [3 x i8] c"%s\00"
@.const5 = private constant [2 x i8] c"\0A\00"
@.const6 = private constant [3 x i8] c"%s\00"
@.const7 = private constant [3 x i8] c"%s\00"


define i32 @main()
{
%tmp_1 = alloca i8*, i32 4, align 16
%tmp_2 = alloca i32, align 4
store i32 0, i32* %tmp_2
%tmp_3 = getelementptr inbounds i8*, i8** %tmp_1, i32 0
%tmp_4 = getelementptr inbounds [6 x i8], [6 x i8]* @.const0, i32 0, i32 0
store i8* %tmp_4, i8** %tmp_3
%tmp_5 = getelementptr inbounds i8*, i8** %tmp_1, i32 1
%tmp_6 = getelementptr inbounds [7 x i8], [7 x i8]* @.const1, i32 0, i32 0
store i8* %tmp_6, i8** %tmp_5
%tmp_7 = getelementptr inbounds i8*, i8** %tmp_1, i32 0
%tmp_8 = getelementptr inbounds i8*, i8** %tmp_1, i32 1
%tmp_9 = getelementptr inbounds i8*, i8** %tmp_1, i32 1
%tmp_10 = getelementptr inbounds i8*, i8** %tmp_1, i32 0
%tmp_11 = load i8*, i8** %tmp_9
%tmp_12 = load i8*, i8** %tmp_10
%tmp_13 = getelementptr inbounds [8 x i8], [8 x i8]* @.const2, i32 0, i32 0
store i8* %tmp_13, i8** %tmp_7
%tmp_14 = getelementptr inbounds [8 x i8], [8 x i8]* @.const3, i32 0, i32 0
store i8* %tmp_14, i8** %tmp_8
%tmp_15 = getelementptr inbounds i8*, i8** %tmp_1, i32 0
%tmp_16 = load i8*, i8** %tmp_15
%str4 = getelementptr inbounds [3 x i8], [3 x i8]* @.const4, i32 0, i32 0
%tmp_17 = call i32 (i8*, ...) @printf(i8* %str4, i8* %tmp_16)
%tmp_18 = getelementptr inbounds [2 x i8], [2 x i8]* @.const5, i32 0, i32 0
%str6 = getelementptr inbounds [3 x i8], [3 x i8]* @.const6, i32 0, i32 0
%tmp_19 = call i32 (i8*, ...) @printf(i8* %str6, i8* %tmp_18)
%tmp_20 = getelementptr inbounds i8*, i8** %tmp_1, i32 1
%tmp_21 = load i8*, i8** %tmp_20
%str7 = getelementptr inbounds [3 x i8], [3 x i8]* @.const7, i32 0, i32 0
%tmp_22 = call i32 (i8*, ...) @printf(i8* %str7, i8* %tmp_21)
br label %L0
L0:
ret i32 0
}

declare i32 @printf(i8*, ...)

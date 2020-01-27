@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@a_ptr = global i32 1
@b_ptr = global i32 0
define i32 @main() #0 {
%1 = load i32, i32* @a_ptr
%2 = icmp ne i32 %1, 0

br i1 %2, label %L0, label %L1
L0:
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 1)
store i32 2, i32* @a_ptr
br label %L2
L1:
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 2)
store i32 1, i32* @a_ptr
br label %L2
L2:
ret i32 0
}

declare i32 @printf(i8*, ...) #1


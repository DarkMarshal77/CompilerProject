@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@a_ptr = global i32 1
@b_ptr = global i32 0

define i32 @func(i32 %first, i32 %sec) {
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 %sec)
ret i32 0
}
define i32 @main() {
%1 = call i32 @func(i32 5, i32 6)
ret i32 %1
}

declare i32 @printf(i8*, ...)


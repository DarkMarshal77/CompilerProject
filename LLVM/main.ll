@.const0 = private constant [3 x i8] c"%d\00"
@d_ptr = global i32 0
store i32 10, i32* @d_ptr
@a_ptr = global i32 0
@b_ptr = global i32 0
@c_ptr = global i32 0
@0 = load i32, i32* @c_ptr
@1 = mul nsw i32 @0, 10
@2 = load i32, i32* @b_ptr
@3 = add nsw i32 @2, @1
store i32 @3, i32* @a_ptr
@e_ptr = global i32 0
@4 = load i32, i32* @a_ptr
@5 = add nsw i32 10, @4
store i32 @5, i32* @e_ptr
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str0, i32 10)
declare i32 @printf(i8*, ...) #1

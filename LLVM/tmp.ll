@a_ptr = global i32 0
@b_ptr = global i32 0
@0 = load i32, i32* @a_ptr
@1 = load i32, i32* @b_ptr
@2 = add nsw i32 @0, @1
L0:
store i32 1, i32* @a_ptr
br label %L2
L1:
store i32 2, i32* @a_ptr
L2:

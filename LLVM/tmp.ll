@a_ptr = global i32 0
@b_ptr = global i32 0
@0 = load i32, i32* @a_ptr
@1 = icmp ne i32 @0, 0
@2 = zext i1 @1 to i8
br i1 @2, label %L0, label %L1
L0:
store i32 2, i32* @a_ptr
br label %L2
L1:
store i32 1, i32* @a_ptr
br label %L2
L2:

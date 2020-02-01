define i32 @sum(i32 %a_ptr, i32 %b_ptr)
{
%tmp_1 = add i32 %a_ptr, %b_ptr
ret i32 %tmp_1
br label %L0
L0:
ret i32 0
}

define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 10, i32* %tmp_1
%tmp_2 = load i32, i32* %tmp_1

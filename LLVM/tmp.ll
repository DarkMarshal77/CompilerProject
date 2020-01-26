@a_ptr = global double 0.0
@b_ptr = global i8 0
@0 = load i8, i8* @b_ptr
@1 = sitofp i8 @0 to double
@2 = fadd double 10.5, @1
store double @2, double* @a_ptr
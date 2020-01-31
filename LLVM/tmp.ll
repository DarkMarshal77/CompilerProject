define i32 @main()
{
%tmp_1 = alloca i32, align 4
store i32 2, i32* %tmp_1
%tmp_2 = alloca i32, align 4
store i32 3, i32* %tmp_2
%tmp_3 = alloca double, align 4
store double 4.1, double* %tmp_3
%tmp_4 = alloca double, align 4
store double 5.9, double* %tmp_4
%tmp_5 = alloca i8, align 1
store i8 97, i8* %tmp_5
%tmp_6 = alloca i8, align 1
store i8 98, i8* %tmp_6
%tmp_7 = alloca i1, align 1
store i1 true, i1* %tmp_7
%tmp_8 = alloca i1, align 1
store i1 false, i1* %tmp_8
%tmp_9 = load i32, i32* %tmp_2
%tmp_10 = load double, double* %tmp_3
%tmp_11 = sitofp i32 %tmp_9 to double
%tmp_12 = fmul double %tmp_11, %tmp_10
%tmp_13 = load i32, i32* %tmp_1
%tmp_14 = sitofp i32 %tmp_13 to double
%tmp_15 = fadd double %tmp_14, %tmp_12
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
%tmp_16 = call i32 (i8*, ...) @printf(i8* %str0, double %tmp_15)
%str1 = getelementptr inbounds [3 x i8], [3 x i8]* @.const1, i32 0, i32 0
%tmp_17 = call i32 (i8*, ...) @printf(i8* %str1, i8 10)
%tmp_18 = load i32, i32* %tmp_1
%tmp_19 = load i32, i32* %tmp_2
%tmp_20 = add i32 %tmp_18, %tmp_19
%tmp_21 = load double, double* %tmp_3
%tmp_22 = sitofp i32 %tmp_20 to double
%tmp_23 = fmul double %tmp_22, %tmp_21
%str2 = getelementptr inbounds [3 x i8], [3 x i8]* @.const2, i32 0, i32 0
%tmp_24 = call i32 (i8*, ...) @printf(i8* %str2, double %tmp_23)
%str3 = getelementptr inbounds [3 x i8], [3 x i8]* @.const3, i32 0, i32 0
%tmp_25 = call i32 (i8*, ...) @printf(i8* %str3, i8 10)
%tmp_26 = load i32, i32* %tmp_2
%tmp_27 = sub i32 %tmp_26, 3
%tmp_28 = load i8, i8* %tmp_5
%tmp_29 = zext i8 %tmp_28 to i32
%tmp_30 = sub i32 %tmp_29, 97
%tmp_31 = icmp ne i32 %tmp_27, 0
%tmp_32 = icmp ne i32 %tmp_30, 0
%tmp_33 = or i1 %tmp_31, %tmp_32
%tmp_34 = zext i1 %tmp_33 to i32
%str4 = getelementptr inbounds [3 x i8], [3 x i8]* @.const4, i32 0, i32 0
%tmp_35 = call i32 (i8*, ...) @printf(i8* %str4, i32 %tmp_34)
%str5 = getelementptr inbounds [3 x i8], [3 x i8]* @.const5, i32 0, i32 0
%tmp_36 = call i32 (i8*, ...) @printf(i8* %str5, i8 10)
%tmp_37 = load i32, i32* %tmp_2
%tmp_38 = sub i32 %tmp_37, 2
%tmp_39 = load i8, i8* %tmp_5
%tmp_40 = zext i8 %tmp_39 to i32
%tmp_41 = sub i32 %tmp_40, 97
%tmp_42 = icmp ne i32 %tmp_38, 0
%tmp_43 = icmp ne i32 %tmp_41, 0
%tmp_44 = or i1 %tmp_42, %tmp_43
%tmp_45 = zext i1 %tmp_44 to i32
%str6 = getelementptr inbounds [3 x i8], [3 x i8]* @.const6, i32 0, i32 0
%tmp_46 = call i32 (i8*, ...) @printf(i8* %str6, i32 %tmp_45)
%str7 = getelementptr inbounds [3 x i8], [3 x i8]* @.const7, i32 0, i32 0
%tmp_47 = call i32 (i8*, ...) @printf(i8* %str7, i8 10)
%tmp_48 = load i32, i32* %tmp_2
%tmp_49 = sub i32 %tmp_48, 2
%tmp_50 = load i8, i8* %tmp_5
%tmp_51 = zext i8 %tmp_50 to i32
%tmp_52 = sub i32 %tmp_51, 97
%tmp_53 = icmp ne i32 %tmp_49, 0
%tmp_54 = icmp ne i32 %tmp_52, 0
%tmp_55 = and i1 %tmp_53, %tmp_54
%tmp_56 = zext i1 %tmp_55 to i32
%str8 = getelementptr inbounds [3 x i8], [3 x i8]* @.const8, i32 0, i32 0
%tmp_57 = call i32 (i8*, ...) @printf(i8* %str8, i32 %tmp_56)
%str9 = getelementptr inbounds [3 x i8], [3 x i8]* @.const9, i32 0, i32 0
%tmp_58 = call i32 (i8*, ...) @printf(i8* %str9, i8 10)
%tmp_59 = load i32, i32* %tmp_2
%tmp_60 = sub i32 %tmp_59, 2
%tmp_61 = load i8, i8* %tmp_5
%tmp_62 = zext i8 %tmp_61 to i32
%tmp_63 = sub i32 %tmp_62, 98
%tmp_64 = icmp ne i32 %tmp_60, 0
%tmp_65 = icmp ne i32 %tmp_63, 0
%tmp_66 = or i1 %tmp_64, %tmp_65
%tmp_67 = zext i1 %tmp_66 to i32
%str10 = getelementptr inbounds [3 x i8], [3 x i8]* @.const10, i32 0, i32 0
%tmp_68 = call i32 (i8*, ...) @printf(i8* %str10, i32 %tmp_67)
%str11 = getelementptr inbounds [3 x i8], [3 x i8]* @.const11, i32 0, i32 0
%tmp_69 = call i32 (i8*, ...) @printf(i8* %str11, i8 10)
%tmp_70 = load i32, i32* %tmp_2
%tmp_71 = load i1, i1* %tmp_7
%tmp_72 = zext i1 %tmp_71 to i32
%tmp_73 = sub i32 %tmp_70, %tmp_72
%str12 = getelementptr inbounds [3 x i8], [3 x i8]* @.const12, i32 0, i32 0
%tmp_74 = call i32 (i8*, ...) @printf(i8* %str12, i32 %tmp_73)
%str13 = getelementptr inbounds [3 x i8], [3 x i8]* @.const13, i32 0, i32 0
%tmp_75 = call i32 (i8*, ...) @printf(i8* %str13, i8 10)
%tmp_76 = load i32, i32* %tmp_1
%tmp_77 = load i32, i32* %tmp_2
%tmp_78 = mul i32 %tmp_76, %tmp_77
%tmp_79 = srem i32 13, 4
%tmp_80 = add i32 %tmp_78, %tmp_79
%str14 = getelementptr inbounds [3 x i8], [3 x i8]* @.const14, i32 0, i32 0
%tmp_81 = call i32 (i8*, ...) @printf(i8* %str14, i32 %tmp_80)
%str15 = getelementptr inbounds [3 x i8], [3 x i8]* @.const15, i32 0, i32 0
%tmp_82 = call i32 (i8*, ...) @printf(i8* %str15, i8 10)
%tmp_83 = load i32, i32* %tmp_1
%tmp_84 = load i32, i32* %tmp_2
%tmp_85 = mul i32 %tmp_83, %tmp_84
%tmp_86 = add i32 %tmp_85, 13
%tmp_87 = srem i32 %tmp_86, 4
%str16 = getelementptr inbounds [3 x i8], [3 x i8]* @.const16, i32 0, i32 0
%tmp_88 = call i32 (i8*, ...) @printf(i8* %str16, i32 %tmp_87)
br label %L0
L0:
ret i32 0
}


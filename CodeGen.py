import atexit
import copy
from queue import Queue
from lark import Transformer
from CONFIG import *


class Node:
    def __init__(self, value, type):
        self.value = value
        self.type = type


class CodeGen(Transformer):
    def __init__(self):
        super().__init__()
        atexit.register(self.cleanup)
        self.ST_stack = [INIT_ST.copy()]
        self.ss = []
        self.label_stack = []
        self.label_counter = 0

        self.scope_level = 0
        self.const_cnt = 0
        self.temp_cnt = [0, 1]
        self.dcls = ''
        self.consts = '@.str_func_def_ret = private constant [1 x i8] c"\\00"\n'

        self.in_func_def = False
        self.display = ''

        self.tmp = open("LLVM/tmp.ll", 'w')

    def ST(self):
        return self.ST_stack[-1]

    def get_label(self):
        label = "L" + str(self.label_counter)
        self.label_counter += 1
        return label

    def cleanup(self):
        self.tmp.close()
        main = open("LLVM/main.ll", 'w')
        self.tmp = open("LLVM/tmp.ll", 'r')

        main.write(self.consts)
        main.write("\n\n")
        main.write(self.tmp.read())
        main.write(self.dcls)

        self.tmp.close()
        main.close()

    def global_def_assignment(self, args):
        rhs = self.ss.pop()
        type = self.ss.pop()
        lhs = self.ss.pop()

        if type not in types:
            raise Exception("ERROR: Invalid var type, type = {}".format(type))

        if lhs.value in self.ST():
            if lhs.value in INIT_ST:
                print("'", lhs.value, "' is a reserved name. Try another name for your variable.")
            else:
                print("Double declaration of '", lhs.value, "'")
            quit()

        value_name = self.type_cast(type, rhs.value, rhs.type, True)
        var_ptr_name = str(self.temp_cnt[0])
        self.temp_cnt[0] += 1
        if type == "ESCAPED_STRING":
            i = 0
            value_len = len(value_name)
            value_name = self.replace_special_char(value_name)
            while i < STRING_MAX_SIZE - value_len:
                value_name += '\\00'
                i += 1

            self.tmp.write('@{} = global [{} x i8] c"{}", align 16\n'.format(var_ptr_name, STRING_MAX_SIZE, value_name))
            self.ST()[lhs.value] = {"type": "ESCAPED_STRING", "name": var_ptr_name, "by_value": False}
        else:
            self.tmp.write(
                '@{} = global {} {}, align {}\n'.format(var_ptr_name, type_convert[type], value_name, size_map[type]))
            self.ST()[lhs.value] = {"type": type, "size": size_map[type], "name": var_ptr_name, "by_value": False}

    def global_def(self, args):
        type = self.ss.pop()
        var = self.ss.pop()

        if type not in types:
            raise Exception("ERROR: Invalid var type, type = {}".format(type))

        if var.value in self.ST():
            if var.value in INIT_ST:
                print("'", var.value, "' is a reserved name. Try another name for your variable.")
            else:
                print("Double declaration of '", var.value, "'")
            quit()

        var_ptr_name = str(self.temp_cnt[0])
        self.temp_cnt[0] += 1
        if type == "ESCAPED_STRING":
            self.tmp.write('@{} = global [{} x i8] zeroinitializer, align 16\n'.format(var_ptr_name, STRING_MAX_SIZE))
            self.ST()[var.value] = {"type": "ESCAPED_STRING", "name": var_ptr_name, "by_value": self.in_func_def}
        else:
            self.tmp.write(
                '@{} = global {} 0, align {}\n'.format(var_ptr_name, type_convert[type], size_map[type]))
            self.ST()[var.value] = {"type": type, "size": size_map[type], "name": var_ptr_name, "by_value": self.in_func_def}

    def add_to_st(self, args):
        type = self.ss.pop()
        var = self.ss.pop()
        self.ss.append(var)

        if type not in types:
            raise Exception("ERROR: Invalid var type, type = {}".format(type))

        if var.value in self.ST():
            if var.value in INIT_ST:
                print("'", var.value, "' is a reserved name. Try another name for your variable.")
            else:
                print("Double declaration of '", var.value, "'")
            quit()

        var_ptr_name = 'tmp_' + str(self.temp_cnt[1])
        self.temp_cnt[1] += 1
        if type == "ESCAPED_STRING":
            if not self.in_func_def:
                self.tmp.write('%{} = alloca i8*, align 8\n'.format(var_ptr_name))
                self.ST()[var.value] = {"type": "ESCAPED_STRING", "name": var_ptr_name, "by_value": False}
            else:
                self.ST()[var.value] = {"type": "ESCAPED_STRING", "name": var.value + '_ptr', "by_value": False}
        else:
            if not self.in_func_def:
                self.tmp.write(
                    '%{} = alloca {}, align {}\n'.format(var_ptr_name, type_convert[type], size_map[type]))
                self.ST()[var.value] = {"type": type, "size": size_map[type], "name": var_ptr_name,
                                        "by_value": self.in_func_def}
            else:
                self.ST()[var.value] = {"type": type, "size": size_map[type], "name": var.value + '_ptr',
                                        "by_value": self.in_func_def}

    def integer_push(self, args):
        self.ss.append("SIGNED_INT")
        return "integer"

    def real_push(self, args):
        self.ss.append("SIGNED_FLOAT")
        return "real"

    def string_push(self, args):
        self.ss.append("ESCAPED_STRING")
        return "string"

    def character_push(self, args):
        self.ss.append("CHAR")
        return "character"

    def boolean_push(self, args):
        self.ss.append("BOOL")
        return "boolean"

    def id(self, args):
        if args[0].value == 'true' or args[0].value == 'false':
            self.ss.append(Node(args[0].value, 'BOOL'))
        else:
            self.push_ss(args)
        return args[0]

    def push_ss(self, args):
        if args[0].type == 'CHAR':
            if len(args[0].value) != 3:
                raise Exception("Expected a character. But something else is given!")
            args[0].value = ord(args[0].value[1])
        if args[0].type == 'ESCAPED_STRING':
            args[0].value = args[0].value[1:-1]
        self.ss.append(args[0])

    def pop_ss(self, args):
        if not self.in_func_def:
            self.ss.pop()

    def empty_ss(self, args):
        if len(self.ss) >= 10000:
            self.ss = self.ss[5000:]

    def strlen(self):
        var = self.ss.pop()
        opr_type, opr_name = self.operand_fetch(var, False)

        if opr_type != 'ESCAPED_STRING':
            raise Exception('strlen input must be String. input type: {}'.format(opr_type))

        if 'declare i64 @strlen(i8*)' not in self.dcls:
            self.dcls += 'declare i64 @strlen(i8*)\n'
        if var.type == 'CNAME':
            self.tmp.write('%tmp_{0} = getelementptr inbounds [{1} x i8], [{1} x i8]* {2}, i32 0, i32 0\n'.format(
                self.temp_cnt[1], STRING_MAX_SIZE, opr_name))
            self.temp_cnt[1] += 1
            self.tmp.write('%tmp_{} = call i64 @strlen(i8* %tmp_{})\n'.format(self.temp_cnt[1], self.temp_cnt[1] - 1))
            self.temp_cnt[1] += 1
        else:
            str_len = len(opr_name)
            opr_name = self.replace_special_char(opr_name)
            self.consts += '@.const{} = private constant [{} x i8] c"{}\\00"\n'.format(self.const_cnt,
                                                                                       str_len + 1,
                                                                                       opr_name)
            self.tmp.write(
                '%var_str_ptr{1} = getelementptr inbounds [{0} x i8], [{0} x i8]* @.const{1}, i32 0, i32 0\n'.format(
                    str_len + 1, self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i64 @strlen(i8* %var_str_ptr{})\n'.format(self.temp_cnt[1], self.const_cnt))
            self.temp_cnt[1] += 1
            self.const_cnt += 1

        # cast i64 to i32
        self.tmp.write('%tmp_{} = trunc i64 %tmp_{} to i32\n'.format(self.temp_cnt[1], self.temp_cnt[1]-1))
        self.ST()['{}__'.format(self.temp_cnt[1])] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                      "name": 'tmp_{}'.format(self.temp_cnt[1]),
                                                      "by_value": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[1]), 'CNAME'))
        self.temp_cnt[1] += 1

    def write(self):
        var = self.ss.pop()
        opr_type, opr_name = self.operand_fetch(var, True)

        if 'declare i32 @printf(i8*, ...)' not in self.dcls:
            self.dcls += 'declare i32 @printf(i8*, ...)\n'
        if opr_type == "SIGNED_INT":
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @printf(i8* %str{}, {} {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                    type_convert[opr_type], opr_name))
            printf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == "SIGNED_FLOAT":
            self.consts += '@.const{} = private constant [3 x i8] c"%f\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @printf(i8* %str{}, {} {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                    type_convert[opr_type], opr_name))
            printf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == "CHAR":
            self.consts += '@.const{} = private constant [3 x i8] c"%c\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @printf(i8* %str{}, {} {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                    type_convert[opr_type], opr_name))
            printf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == "ESCAPED_STRING":
            self.consts += '@.const{} = private constant [3 x i8] c"%s\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @printf(i8* %str{}, {} {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                    type_convert[opr_type], opr_name))
            printf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == "BOOL":
            opr_name = self.type_cast('SIGNED_INT', opr_name, opr_type, False if var.type == 'CNAME' else True)
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @printf(i8* %str{}, {} {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                    type_convert['SIGNED_INT'], opr_name))
            printf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        else:
            raise Exception('Unknown var type {}'.format(opr_type))

        self.ST()['{}__'.format(printf_return_var)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                       "name": 'tmp_{}'.format(printf_return_var),
                                                       "by_value": True}
        self.ss.append(Node('{}__'.format(printf_return_var), 'CNAME'))

    def read(self):
        var = self.ss.pop()
        if var.type != 'CNAME':
            raise Exception('ERROR: Expected a variable name.')

        opr_type, opr_name = self.operand_fetch(var, False)
        if 'declare i32 @scanf(i8*, ...)' not in self.dcls:
            self.dcls += 'declare i32 @scanf(i8*, ...)\n'
        if opr_type == 'SIGNED_INT':
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @scanf(i8* %str{}, i32* {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                     opr_name))
            scanf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == 'SIGNED_FLOAT':
            self.consts += '@.const{} = private constant [3 x i8] c"%f\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @scanf(i8* %str{}, double* {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                        opr_name))
            scanf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == 'CHAR':
            self.consts += '@.const{} = private constant [3 x i8] c"%c\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @scanf(i8* %str{}, i8* {})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                    opr_name))
            scanf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1
        elif opr_type == 'ESCAPED_STRING':
            self.consts += '@.const{} = private constant [3 x i8] c"%s\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            # define a temporary [512 x i8]
            self.tmp.write('%tmp_{} = alloca [{} x i8], align 16'.format(self.temp_cnt[1], STRING_MAX_SIZE))
            self.temp_cnt[1] += 1
            self.tmp.write('%tmp_{0} = getelementptr inbounds [{1} x i8], [{1} x i8]* %tmp_{2}, i32 0, i32 0\n'.format(
                self.temp_cnt[1], STRING_MAX_SIZE, self.temp_cnt[1]-1))
            self.temp_cnt[1] += 1
            # scanf
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @scanf(i8* %str{}, i8* %tmp_{})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                         self.temp_cnt[1] - 1))
            scanf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
            self.const_cnt += 1

            # save [512 x i8] to destination
            self.tmp.write('store i8* %tmp_{}, i8** {}\n'.format(
                self.temp_cnt[1]-2, opr_name))
            self.temp_cnt[1] += 1
        elif opr_type == 'BOOL':
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))

            self.tmp.write('%tmp_{} = alloca i32, align 4\n'.format(self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            self.tmp.write(
                '%tmp_{} = call i32 (i8*, ...) @scanf(i8* %str{}, i32* %tmp_{})\n'.format(self.temp_cnt[1], self.const_cnt,
                                                                                          self.temp_cnt[1] - 1))
            scanf_return_var = str(self.temp_cnt[1])
            self.temp_cnt[1] += 1

            self.tmp.write('%tmp_{} = load i32, i32* %tmp_{}\n'.format(self.temp_cnt[1], self.temp_cnt[1] - 2))
            self.temp_cnt[1] += 1
            i32_to_i1_converted_name = self.type_cast('BOOL', '%tmp_' + str(self.temp_cnt[1] - 1), 'SIGNED_INT', False)
            self.tmp.write('store i1 {}, i1* {}\n'.format(i32_to_i1_converted_name, opr_name))
            self.const_cnt += 1
        else:
            raise Exception('Unknown var type {}'.format(opr_type))

        self.ST()['{}__'.format(scanf_return_var)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                      "name": 'tmp_{}'.format(scanf_return_var),
                                                      "by_value": True}
        self.ss.append(Node('{}__'.format(scanf_return_var), 'CNAME'))

    def operand_fetch(self, opr, get_value):
        temp_cnt_ptr = 0 if self.scope_level == 0 else 1
        if opr.type == 'CNAME':
            found = False
            level = self.scope_level
            while level > 0:
                if opr.value in self.ST_stack[level]:
                    opr_descriptor = self.ST_stack[level][opr.value]
                    opr_type = opr_descriptor['type']
                    if opr_descriptor['by_value']:
                        opr_name = '%' + opr_descriptor['name']
                    else:
                        opr_name = '%' + opr_descriptor['name']
                        if get_value is True:
                            self.tmp.write('%tmp_{0} = load {1}, {1}* {2}\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                                                    type_convert[opr_type], opr_name))
                            opr_name = '%tmp_' + str(self.temp_cnt[temp_cnt_ptr])
                            self.temp_cnt[temp_cnt_ptr] += 1
                    found = True
                    break
                level -= 1

            if not found:
                if opr.value not in self.ST_stack[0]:
                    raise Exception('ERROR: {} is not defined.'.format(opr.value))
                else:
                    opr_descriptor = self.ST_stack[0][opr.value]
                    opr_type = opr_descriptor['type']
                    if opr_descriptor['by_value']:
                        opr_name = '@' + opr_descriptor['name']
                    else:
                        opr_name = '@' + opr_descriptor['name']
                        if get_value is True:
                            if opr_type != 'ESCAPED_STRING':
                                self.tmp.write('%tmp_{0} = load {1}, {1}* {2}\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                                                        type_convert[opr_type], opr_name))
                                opr_name = "%tmp_" + str(self.temp_cnt[temp_cnt_ptr])
                                self.temp_cnt[temp_cnt_ptr] += 1
                            else:
                                self.tmp.write('%tmp_{0} = getelementptr inbounds [{1} x i8], [{1} x i8]* {2}, i32 0, i32 0\n'.format(self.temp_cnt[1], STRING_MAX_SIZE, opr_name))
                                opr_name = '%tmp_' + str(self.temp_cnt[1])
                                self.temp_cnt[1] += 1
        else:
            if opr.type == 'ESCAPED_STRING':
                str_len = len(opr.value)
                opr.value = self.replace_special_char(opr.value)
                self.consts += '@.const{} = private constant [{} x i8] c"{}\\00"\n'.format(self.const_cnt, str_len+1, opr.value)
                self.tmp.write('%tmp_{0} = getelementptr inbounds [{1} x i8], [{1} x i8]* @.const{2}, i32 0, i32 0\n'.format(self.temp_cnt[1], str_len+1, self.const_cnt))
                opr_name = '%tmp_' + str(self.temp_cnt[1])
                self.temp_cnt[1] += 1
                self.const_cnt += 1
            else:
                opr_name = opr.value
            opr_type = opr.type

        return opr_type, opr_name

    def result_type_wrapper(self, opr1, opr2, op_type):
        first_type, first_name = self.operand_fetch(opr1, True)
        second_type, second_name = self.operand_fetch(opr2, True)

        res_type = result_type(op_type, first_type, second_type)
        return first_type, first_name, second_type, second_name, res_type

    def const_type_cast(self, res_type, opr_name, opr_type):
        if res_type == 'SIGNED_INT':
            if opr_type == 'SIGNED_FLOAT':
                return str(int(float(opr_name)))
            elif opr_type == 'BOOL':
                return '1' if opr_name == 'true' else '0'
            elif opr_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
            else:
                return str(opr_name)
        elif res_type == 'SIGNED_FLOAT':
            if opr_type == 'BOOL':
                return '1.0' if opr_name == 'true' else '0.0'
            elif opr_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
            elif opr_type == 'SIGNED_INT':
                return str(opr_name) + '.0'
            else:
                return str(opr_name) + '.0'
        elif res_type == 'BOOL':
            if opr_type == 'SIGNED_INT':
                return 'false' if int(opr_name) == 0 else 'true'
            elif opr_type == 'CHAR':
                return 'false' if int(opr_name) == 0 else 'true'
            elif opr_type == 'SIGNED_FLOAT':
                return 'false' if float(opr_name) == 0.0 else 'true'
            elif opr_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
        elif res_type == 'CHAR':
            if opr_type == 'SIGNED_INT':
                return str(opr_name)
            elif opr_type == 'BOOL':
                return '1' if opr_name == 'true' else '0'
            elif opr_type == 'SIGNED_FLOAT':
                return str(int(float(opr_name)))
            elif opr_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
        elif res_type == 'ESCAPED_STRING':
            rhs_name = self.type_cast('CHAR', opr_name, opr_type, True)
            self.tmp.write('%tmp_{0} = alloca [2 x i8], align 1\n'.format(self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            self.tmp.write('%tmp_{} = getelementptr inbounds [2 x i8], [2 x i8]* %tmp_{}, i64 0, i64 0\n'.format(self.temp_cnt[1], self.temp_cnt[1]-1))
            self.tmp.write('store i8 {}, i8* %tmp_{}\n'.format(rhs_name, self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            self.tmp.write('%tmp_{} = getelementptr inbounds [2 x i8], [2 x i8]* %tmp_{}, i64 0, i64 1\n'.format(self.temp_cnt[1], self.temp_cnt[1]-2))
            self.tmp.write('store i8 0, i8* %tmp_{}\n'.format(self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            return "%tmp_" + str(self.temp_cnt[1] - 2)
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

    def type_cast(self, res_type, opr_name, opr_type, const):
        if res_type == opr_type:
            return opr_name

        if opr_type == 'ESCAPED_STRING':
            raise Exception("ERROR: Illegal operand type")

        if const:
            return self.const_type_cast(res_type, opr_name, opr_type)

        temp_cnt_ptr = 0 if self.scope_level == 0 else 1
        if res_type == 'SIGNED_INT':
            if opr_type == 'SIGNED_FLOAT':
                self.tmp.write(
                    '%tmp_{} = fptosi double {} to i32\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                                 opr_name))
            else:
                self.tmp.write(
                    '%tmp_{} = zext {} {} to i32\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                           type_convert[opr_type], opr_name))
        elif res_type == 'SIGNED_FLOAT':
            self.tmp.write(
                '%tmp_{} = sitofp {} {} to double\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                            type_convert[opr_type],
                                                            opr_name))
        elif res_type == 'BOOL':
            if opr_type == 'SIGNED_FLOAT':
                self.tmp.write(
                    '%tmp_{} = fcmp une double {}, 0.0\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                                 opr_name))
            else:
                self.tmp.write('%tmp_{} = icmp ne {} {}, 0\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                                     type_convert[opr_type], opr_name))
        elif res_type == 'CHAR':
            if opr_type == 'SIGNED_FLOAT':
                self.tmp.write(
                    '%tmp_{} = fptosi double {} to i8\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                                opr_name))
            elif opr_type == 'BOOL':
                self.tmp.write(
                    '%tmp_{} = zext {} {} to i8\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                          type_convert[opr_type], opr_name))
            else:
                self.tmp.write(
                    '%tmp_{} = trunc {} {} to i8\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                           type_convert[opr_type], opr_name))
        elif res_type == 'ESCAPED_STRING':
            rhs_name = self.type_cast('CHAR', opr_name, opr_type, True)
            self.tmp.write('%tmp_{0} = alloca [2 x i8], align 1\n'.format(self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            self.tmp.write('%tmp_{} = getelementptr inbounds [2 x i8], [2 x i8]* %tmp_{}, i64 0, i64 0\n'.format(self.temp_cnt[1], self.temp_cnt[1]-1))
            self.tmp.write('store i8 {}, i8* %tmp_{}\n'.format(rhs_name, self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            self.tmp.write('%tmp_{} = getelementptr inbounds [2 x i8], [2 x i8]* %tmp_{}, i64 0, i64 1\n'.format(self.temp_cnt[1], self.temp_cnt[1]-2))
            self.tmp.write('store i8 0, i8* %tmp_{}\n'.format(self.temp_cnt[1]))
            self.temp_cnt[1] += 1
            return "%tmp_" + str(self.temp_cnt[1] - 2)
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

        self.temp_cnt[temp_cnt_ptr] += 1
        return "%tmp_" + str(self.temp_cnt[temp_cnt_ptr] - 1)

    def do_calc_operation(self, opr1, opr2, op_type):
        temp_cnt_ptr = 0 if self.scope_level == 0 else 1

        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2, op_type)
        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        if res_type == 'SIGNED_INT':
            if op_type == 'div' or op_type == 'rem':
                op_type = 's' + op_type
            self.tmp.write(
                '%tmp_{} = {} i32 {}, {}\n'.format(self.temp_cnt[temp_cnt_ptr], op_type, first_name, second_name))
            self.ST()['{}__'.format(self.temp_cnt[temp_cnt_ptr])] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                                     "name": 'tmp_{}'.format(self.temp_cnt[temp_cnt_ptr]),
                                                                     "by_value": True}
        elif res_type == 'SIGNED_FLOAT':
            self.tmp.write(
                '%tmp_{} = f{} double {}, {}\n'.format(self.temp_cnt[temp_cnt_ptr], op_type, first_name, second_name))
            self.ST()['{}__'.format(self.temp_cnt[temp_cnt_ptr])] = {"type": "SIGNED_FLOAT", "size": REAL_SIZE,
                                                                     "name": 'tmp_{}'.format(self.temp_cnt[temp_cnt_ptr]),
                                                                     "by_value": True}
        else:
            raise Exception('do_calc_operation: Internal Error.')

        self.ss.append(Node('{}__'.format(self.temp_cnt[temp_cnt_ptr]), 'CNAME'))
        self.temp_cnt[temp_cnt_ptr] += 1

    def add(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_calc_operation(first, second, 'add')

    def sub(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_calc_operation(first, second, 'sub')

    def mul(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_calc_operation(first, second, 'mul')

    def div(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_calc_operation(first, second, 'div')

    def mod(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_calc_operation(first, second, 'rem')

    def do_bitwise_calc(self, opr1, opr2, op_type):
        temp_cnt_ptr = 0 if self.scope_level == 0 else 1

        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2,
                                                                                              'bitwise_' + op_type)
        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        self.tmp.write(
            '%tmp_{} = {} i32 {}, {}\n'.format(self.temp_cnt[temp_cnt_ptr], op_type, first_name,
                                               second_name))
        self.ST()['{}__'.format(self.temp_cnt[temp_cnt_ptr])] = {"type": "SIGNED_INT",
                                                                 "size": INT_SIZE,
                                                                 "name": 'tmp_{}'.format(self.temp_cnt[temp_cnt_ptr]),
                                                                 "by_value": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[temp_cnt_ptr]), 'CNAME'))
        self.temp_cnt[temp_cnt_ptr] += 1

    def bitwise_and(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_bitwise_calc(first, second, 'and')

    def bitwise_or(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_bitwise_calc(first, second, 'or')

    def bitwise_xor(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_bitwise_calc(first, second, 'xor')

    def do_boolean_calc(self, opr1, opr2, op_type):
        temp_cnt_ptr = 0 if self.scope_level == 0 else 1

        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2,
                                                                                              'boolean_' + op_type)
        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        self.tmp.write(
            '%tmp_{} = {} i1 {}, {}\n'.format(self.temp_cnt[temp_cnt_ptr], op_type, first_name,
                                              second_name))

        self.ST()['{}__'.format(self.temp_cnt[temp_cnt_ptr])] = {"type": "BOOL",
                                                                 "size": BOOL_SIZE,
                                                                 "name": 'tmp_{}'.format(self.temp_cnt[temp_cnt_ptr]),
                                                                 "by_value": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[temp_cnt_ptr]), 'CNAME'))
        self.temp_cnt[temp_cnt_ptr] += 1

    def boolean_and(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_boolean_calc(first, second, 'and')

    def boolean_or(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_boolean_calc(first, second, 'or')

    def do_compare_calc(self, opr1, opr2, op_type):
        temp_cnt_ptr = 0 if self.scope_level == 0 else 1

        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2, op_type)
        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        self.tmp.write('%tmp_{} = {} {} {} {}, {}\n'.format(self.temp_cnt[temp_cnt_ptr],
                                                            COMP_SIGN_TO_FLAG[res_type]['op'],
                                                            COMP_SIGN_TO_FLAG[res_type][op_type], type_convert[res_type],
                                                            first_name, second_name))
        self.ST()['{}__'.format(self.temp_cnt[temp_cnt_ptr])] = {"type": "BOOL",
                                                                 "size": BOOL_SIZE,
                                                                 "name": 'tmp_{}'.format(self.temp_cnt[temp_cnt_ptr]),
                                                                 "by_value": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[temp_cnt_ptr]), 'CNAME'))
        self.temp_cnt[temp_cnt_ptr] += 1

    def comp_eq(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_compare_calc(first, second, '==')

    def comp_ne(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_compare_calc(first, second, '<>')

    def comp_gt(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_compare_calc(first, second, '>')

    def comp_ge(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_compare_calc(first, second, '>=')

    def comp_lt(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_compare_calc(first, second, '<')

    def comp_le(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_compare_calc(first, second, '<=')

    def push_q(self, args):
        self.ss.append(Queue())

    def pop_ss_push_q(self, args):
        temp = self.ss.pop()
        self.ss[-1].put(temp)

    def assignment(self, args):
        rhs = self.ss.pop()
        lhs = self.ss.pop()

        if lhs.type != 'CNAME':
            raise Exception('Left-hand-side must be a variable.')

        lhs_type, lhs_name = self.operand_fetch(lhs, False)
        rhs_type, rhs_name = self.operand_fetch(rhs, True)

        # todo uncomment
        # real_rhs_type = rhs.type
        # if rhs.type == 'CNAME':
        #     for st in self.ST_stack:
        #         if rhs in st:
        #             real_rhs_type = st[rhs.value]['type']
        # if lhs_type == real_rhs_type:
        #     self.ss.append(Node(1, 'SIGNED_INT'))
        # else:
        #     self.ss.append(Node(0, 'SIGNED_INT'))

        rhs_name = self.type_cast(lhs_type, rhs_name, rhs_type, False if rhs.type == 'CNAME' else True)
        self.tmp.write('store {0} {1}, {0}* {2}\n'.format(type_convert[lhs_type], rhs_name, lhs_name))

    def jz(self, args):
        be = self.ss.pop()

        be_type, be_name = self.operand_fetch(be, True)
        be_name = self.type_cast('BOOL', be_name, be_type, False if be.type == 'CNAME' else True)

        st1_label = self.get_label()
        st2_label = self.get_label()
        self.label_stack.append(st2_label)
        self.tmp.write('br i1 {}, label %{}, label %{}\n'.format(be_name, st1_label, st2_label))
        self.tmp.write(st1_label + ":\n")

    def cjz(self, args):
        st2_label = self.label_stack.pop()
        self.tmp.write("br label %" + st2_label + "\n")
        self.temp_cnt[1] += 1
        self.tmp.write(st2_label + ":\n")

    def cjp(self, args):
        out_label = self.label_stack.pop()
        self.tmp.write("br label %" + out_label + "\n")
        self.temp_cnt[1] += 1
        self.tmp.write(out_label + ":\n")

    def jp_cjz(self, args):
        st2_label = self.label_stack.pop()
        out_label = self.get_label()
        self.label_stack.append(out_label)
        self.tmp.write("br label %" + out_label + "\n")
        self.temp_cnt[1] += 1
        self.tmp.write(st2_label + ":\n")

    def make_begin_label_loop(self, args):
        begin_label = self.get_label()
        self.label_stack.append(begin_label)
        self.tmp.write("br label %" + begin_label + "\n")
        self.temp_cnt[1] += 1
        self.tmp.write(begin_label + ":\n")

    def branch_middle_loop(self, args):
        be = self.ss.pop()

        be_type, be_name = self.operand_fetch(be, True)
        be_name = self.type_cast('BOOL', be_name, be_type, False if be.type == 'CNAME' else True)

        in_label = self.get_label()
        out_label = self.get_label()
        self.label_stack.append(out_label)
        self.tmp.write('br i1 {}, label %{}, label %{}\n'.format(be_name, in_label, out_label))
        self.tmp.write(in_label + ":\n")

    def jp_begin_loop(self, args):
        out_label = self.label_stack.pop()
        begin_label = self.label_stack.pop()
        self.tmp.write("br label %" + begin_label + "\n")
        self.temp_cnt[1] += 1
        self.tmp.write(out_label + ":\n")

    def function_call(self, args):
        args = self.ss.pop()
        func_name = self.ss.pop()
        if str(func_name) == "read":
            self.ss.append(args.get())
            self.read()
        elif str(func_name) == "write":
            self.ss.append(args.get())
            self.write()
        elif str(func_name) == "strlen":
            self.ss.append(args.get())
            self.strlen()
            return
        elif str(func_name) in self.ST_stack[0]:
            object_args = self.ST_stack[0][func_name.value]["args"]
            output_type = self.ST_stack[0][func_name.value]["out_type"]
            signature = self.make_func_signature(output_type, object_args)
            output_string = "("
            for arg in args.queue:
                a_type, a_name = self.operand_fetch(arg, True)
                output_string = output_string + type_convert[a_type] + " " + a_name + ", "
            output_string = output_string[:-2] + ")"
            if not list(args.queue):
                output_string = "()"
            # todo type cast of inputs
            if output_type == "VOID":
                self.tmp.write("call {} @{} {}\n".format(signature, func_name.value, output_string))
                return
            temp = self.temp_cnt[1]
            self.tmp.write("%tmp_{} = call {} @{} {}\n".format(str(temp), signature, func_name.value, output_string))

            self.ST()['{}__'.format(self.temp_cnt[1])] = {"type": output_type, "size": size_map[output_type],
                                                          "name": 'tmp_{}'.format(self.temp_cnt[1]),
                                                          "by_value": True}
            self.ss.append(Node('{}__'.format(self.temp_cnt[1]), 'CNAME'))
            self.temp_cnt[1] += 1
            return
        else:
            raise Exception("Error. Function has not been declared in this scope.")

    def make_func_signature(self, output_type, object_args):
        if not list(object_args.queue):
            return type_convert[output_type] + "()"
        signature = type_convert[output_type] + " ("
        for arg in object_args.queue:
            signature = signature + type_convert[arg] + ", "
        signature = signature[:-2]
        signature = signature + ")"
        return signature

    def function_def(self, args):
        # print('function_def called')
        out_type = self.ss.pop()
        args = self.ss.pop()
        func_name = self.ss.pop()
        if func_name in self.ST_stack[0]:
            raise Exception("Function name already in use")
        # self.scope_level += 1
        arg_types = Queue()
        for arg in args.queue:
            arg_type, arg_name = self.operand_fetch(arg, False)
            arg_types.put(arg_type)

        self.ST_stack[0][func_name.value] = {"out_type": out_type, "args": arg_types}
        self.display = func_name.value

        func_args = ''
        while args.qsize() > 1:
            arg = args.get()
            arg_type, arg_name = self.operand_fetch(arg, False)
            func_args += '{} {}, '.format(type_convert[arg_type], arg_name)
        if args.qsize() == 1:
            arg = args.get()
            arg_type, arg_name = self.operand_fetch(arg, False)
            func_args += '{} {}'.format(type_convert[arg_type], arg_name)

        self.tmp.write('define {} @{}({})\n'.format(type_convert[out_type], func_name, func_args))
        self.tmp.write('{\n')

        self.temp_cnt[self.scope_level] = 1
        self.scope_level -= 1
        self.ss.append(self.ST_stack.pop())

    def push_st(self, args):
        # print('push_st called')
        self.scope_level += 1
        if self.ss and type(self.ss[-1]) == dict:
            self.ST_stack.append(self.ss.pop())
        else:
            self.ST_stack.append(INIT_ST.copy())

    def pop_st(self, args):
        # print('pop_st called')
        self.ST_stack.pop()
        self.scope_level -= 1

    def in_func_def_false(self, args):
        self.in_func_def = False

    def in_func_def_true(self, args):
        self.in_func_def = True

    def close_bracket(self, args):
        func_type = self.ST_stack[0][self.display]['out_type']
        label_temp = self.get_label()
        self.tmp.write("br label %" + label_temp + "\n")
        self.tmp.write(label_temp + ":\n")
        self.tmp.write("ret " + type_convert[func_type] + " " + temp_value[func_type] + "\n")
        self.tmp.write("}\n\n")
        self.display = ''

    def ret(self, args):
        a = self.ss.pop()
        a_type, a_name = self.operand_fetch(a, True)
        func_type = self.ST_stack[0][self.display]['out_type']
        # todo type cast return
        if func_type != a_type:
            raise Exception('ERROR: function type is {} but return type is {}'.format(func_type, a_type))

        if func_type == "ESCAPED_STRING":
            if a.type == 'CNAME':
                # self.tmp.write('%tmp_{0} = getelementptr inbounds [{1} x i8], [{1} x i8]* {2}, i32 0, i32 0\n'.format(
                #     self.temp_cnt[1], STRING_MAX_SIZE, a_name))
                self.tmp.write("ret i8* {}\n".format(a_name))
                # self.temp_cnt[1] += 1
            else:
                str_len = len(a_name)
                a_name = self.replace_special_char(a_name)
                self.consts += '@.const{} = private constant [{} x i8] c"{}\\00"\n'.format(self.const_cnt,
                                                                                           str_len + 1,
                                                                                           a_name)
                self.tmp.write(
                    '%var_str_ptr{1} = getelementptr inbounds [{0} x i8], [{0} x i8]* @.const{1}, i32 0, i32 0\n'.format(
                        str_len + 1, self.const_cnt))
                self.tmp.write("ret [512 x i8] @.const{}\n".format(self.const_cnt))
                self.const_cnt += 1
        else:
            self.tmp.write("ret {} {}\n".format(type_convert[a_type], a_name))

    def make_array_dscp(self, args):
        arr_dims = self.ss.pop()
        arr_type = self.ss.pop()
        arr_name = self.ss.pop()

        if arr_type not in types:
            raise Exception("ERROR: Invalid array type, type = {}".format(arr_type))

        if arr_name.value in self.ST():
            if arr_name.value in INIT_ST:
                print("'", arr_name.value, "' is a reserved name. Try another name for your variable.")
            else:
                print("Double declaration of '", arr_name.value, "'")
            quit()

        arr_dims_value = []
        while not arr_dims.empty():
            dim = arr_dims.get()
            dim_type, dim_name = self.operand_fetch(dim, True)
            dim_name = self.type_cast('SIGNED_INT', dim_name, dim_type, False if dim.type == 'CNAME' else True)
            arr_dims_value.append(dim_name)

        temporary_arr_dims = arr_dims_value.copy()
        calc_arr_index_helper = []
        while len(temporary_arr_dims) > 1:
            calc_arr_index_helper.append(temporary_arr_dims.pop())

            mul_res = '%tmp_' + str(self.temp_cnt[1])
            self.tmp.write('{} = mul i32 {}, {}\n'.format(mul_res, calc_arr_index_helper[-1], temporary_arr_dims.pop()))

            temporary_arr_dims.append(mul_res)
            self.temp_cnt[1] += 1

        var_ptr_name = 'tmp_' + str(self.temp_cnt[1])
        self.temp_cnt[1] += 1
        if not self.in_func_def:
            self.tmp.write('%{} = alloca {}, i32 {}, align 16\n'.format(var_ptr_name, type_convert[arr_type], temporary_arr_dims[0]))
            self.ST()[arr_name.value] = {"dims": arr_dims_value, "type": arr_type, 'calc_arr_index_helper': calc_arr_index_helper,
                                         "name": var_ptr_name, "by_value": False}
        else:
            self.ST()[arr_name.value] = {"dims": arr_dims_value, "type": arr_type, 'calc_arr_index_helper': calc_arr_index_helper,
                                         "name": arr_name.value + '_ptr', "by_value": False}
        temporary_arr_dims.clear()

    def proc_def(self, args):
        self.ss.append("VOID")
        self.function_def(args)

    def close_bracket_proc(self, args):
        func_type = self.ST_stack[0][self.display]['out_type']
        self.tmp.write("ret " + type_convert[func_type] + " " + temp_value[func_type] + "\n")
        self.tmp.write("}\n\n")
        self.display = ''

    def hex_convert(self, args):
        value = int(args[0].value, 0)
        type = "SIGNED_INT"
        return Node(value, type)

    def init_bulk(self, args):
        temp = self.ss.pop()
        self.push_q(args)
        self.ss.append(temp)
        self.pop_ss_push_q(args)

    def bulk(self, args):
        right_q = self.ss.pop()
        left_q = self.ss.pop()
        if len(right_q.queue) != len(left_q.queue):
            raise Exception("RHS and LHS in bulk assignment need to be of the same size")
        n = len(right_q.queue)

        temp_right_q = Queue()

        for i in range(n):
            right_token = right_q.queue[i]
            right_type, right_name = self.operand_fetch(right_token, True)
            if right_token.type == 'CNAME':
                self.ST()[right_name] = {"type": right_type,
                                         "name": right_name[1:],
                                         "by_value": True}
                temp_right_q.put(Node(right_name, 'CNAME'))
            else:
                temp_right_q.put(Node(right_name, right_type))
        for i in range(n):
            self.ss.append(left_q.get())
            self.ss.append(temp_right_q.get())
            self.assignment(args)

    def calc_arr_index(self, args):
        indices = self.ss.pop()
        arr_token = self.ss.pop()

        # finding arr descriptor
        arr_descriptor = {}
        found = False
        level = self.scope_level
        while level > 0:
            if arr_token.value in self.ST_stack[level]:
                arr_descriptor = self.ST_stack[level][arr_token.value]
                found = True
                break
            level -= 1
        if not found:
            if arr_token.value not in self.ST_stack[0]:
                raise Exception('ERROR: {} is not defined.'.format(arr_token.value))
            else:
                arr_descriptor = self.ST_stack[0][arr_token.value]

        arr_dims = arr_descriptor['dims'].copy()
        if indices.qsize() != len(arr_dims):
            indices = Queue()
            arr_dims.clear()
            raise Exception('argument count of {} is not correct'.format(arr_token.value))

        # addr calculation
        arr_type, arr_pointer = self.operand_fetch(arr_token, False)
        calc_arr_index_helper = arr_descriptor['calc_arr_index_helper'].copy()
        while len(calc_arr_index_helper) > 0:
            indice_type, indice_value = self.operand_fetch(indices.get(), True)
            self.tmp.write('%tmp_{} = mul i32 {}, {}\n'.format(self.temp_cnt[1], indice_value, calc_arr_index_helper.pop()))
            self.temp_cnt[1] += 1

            self.tmp.write('%tmp_{0} = getelementptr inbounds {1}, {1}* {2}, i32 %tmp_{3}\n'.format(self.temp_cnt[1], type_convert[arr_type], arr_pointer, self.temp_cnt[1]-1))
            arr_pointer = '%tmp_' + str(self.temp_cnt[1])
            self.temp_cnt[1] += 1
        indice_type, indice_value = self.operand_fetch(indices.get(), True)
        self.tmp.write('%tmp_{0} = getelementptr inbounds {1}, {1}* {2}, i32 {3}\n'.format(self.temp_cnt[1], type_convert[arr_type], arr_pointer, indice_value))

        self.ST()['{}__'.format(self.temp_cnt[1])] = {"type": arr_type,
                                                      "name": 'tmp_{}'.format(self.temp_cnt[1]),
                                                      "by_value": False}
        self.ss.append(Node('{}__'.format(self.temp_cnt[1]), 'CNAME'))
        self.temp_cnt[1] += 1

        indices = Queue()
        arr_dims.clear()
        calc_arr_index_helper.clear()

    def replace_special_char(self, in_str):
        return in_str.replace('\t', '\\09').replace('\n', '\\0A').replace('\v', '\\0B').replace('\f', '\\0C').replace('\r', '\\0D')

    def unary_sub(self, args):
        operand = self.ss.pop()
        self.ss.append(Node(0, "SIGNED_INT"))
        self.ss.append(operand)
        self.sub(args)

    def unary_not(self, args):
        operand = self.ss.pop()
        self.ss.append(Node("true", "BOOL"))
        self.ss.append(operand)
        self.boolean_and(args)
        operand = self.ss.pop()
        self.ss.append(Node(1, "SIGNED_INT"))
        self.ss.append(operand)
        self.sub(args)

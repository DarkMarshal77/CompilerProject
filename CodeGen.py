import atexit
from lark import Transformer
from CONFIG import *
from queue import Queue


class Node:
    def __init__(self, value, type):
        self.value = value
        self.type = type


class CodeGen(Transformer):
    def __init__(self):
        super().__init__()
        atexit.register(self.cleanup)
        self.ST_stack = [INIT_ST.copy()]
        self.ST = self.ST_stack[0]
        self.ss = []
        self.label_stack = []
        self.label_counter = 0

        self.scope_level = 0
        self.const_cnt = 0
        self.temp_cnt = [0]
        self.dcls = ''
        self.consts = ''

        self.tmp = open("LLVM/tmp.ll", 'w')

    def get_label(self):
        label = "L" + str(self.label_counter)
        self.label_counter += 1
        return label

    def cleanup(self):
        self.tmp.close()
        main = open("LLVM/main.ll", 'w')
        self.tmp = open("LLVM/tmp.ll", 'r')

        main.write(self.consts)
        main.write(self.tmp.read())
        main.write(self.dcls)

        self.tmp.close()
        main.close()

    def add_to_st(self, args):
        var = self.ss.pop()
        type = self.ss.pop()
        self.ss.append(var)
        print()

        for symbol_table in self.ST_stack:
            if var.value in symbol_table:
                if var.value in INIT_ST:
                    print("'", var.value, "' is a reserved name. Try another name for your variable.")
                else:
                    print("Double declaration of '", var.value, "'")
                quit()

        if type == "SIGNED_INT":
            if self.scope_level == 0:
                self.tmp.write('@{}_ptr = global i32 0\n'.format(var.value))
            else:
                self.tmp.write('%{}_ptr = alloca i32\n'.format(var.value))
            self.ST[var.value] = {"type": "SIGNED_INT", "size": INT_SIZE, "ptr_name": var.value+'_ptr', "is_temp": False}
        elif type == "ESCAPED_STRING":
            if self.scope_level == 0:
                self.tmp.write('@{}_ptr = global [{} x i8] zeroinitializer 0\n'.format(var.value, STRING_MAX_SIZE))
            else:
                self.tmp.write('%{}_ptr = allca [{} x i8]\n'.format(var.value, STRING_MAX_SIZE))
            self.ST[var.value] = {"type": "ESCAPED_STRING", "ptr_name": var.value+'_ptr', "is_temp": False}
        elif type == "SIGNED_FLOAT":
            if self.scope_level == 0:
                self.tmp.write('@{}_ptr = global double 0.0\n'.format(var.value))
            else:
                self.tmp.write('%{}_ptr = allca double\n'.format(var.value))
            self.ST[var.value] = {"type": "SIGNED_FLOAT", "size": REAL_SIZE, "ptr_name": var.value+'_ptr', "is_temp": False}
        elif type == "CHAR":
            if self.scope_level == 0:
                self.tmp.write('@{}_ptr = global i8 0\n'.format(var.value))
            else:
                self.tmp.write('%{}_ptr = allca i8\n'.format(var.value))
            self.ST[var.value] = {"type": "CHAR", "size": CHAR_SIZE, "ptr_name": var.value+'_ptr', "is_temp": False}
        elif type == "BOOL":
            if self.scope_level == 0:
                self.tmp.write('@{}_ptr = global i8 0\n'.format(var.value))
            else:
                self.tmp.write('%{}_ptr = allca i8\n'.format(var.value))
            self.ST[var.value] = {"type": "BOOL", "size": BOOL_SIZE, "ptr_name": var.value+'_ptr', "is_temp": False}
        else:
            raise Exception("ERROR: Invalid var type, type = {}".format(type))

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
            args[0].value = ord(args[0].value)
        if args[0].type == 'ESCAPED_STRING':
            args[0].value = args[0].value[1:-1]
        self.ss.append(args[0])

    def empty_ss(self, args):
        self.ss = []

    def write(self):
        var = self.ss.pop()
        opr_type, opr_name = self.operand_fetch(var, True)

        if 'declare i32 @printf(i8*, ...) #1' not in self.dcls:
            self.dcls += 'declare i32 @printf(i8*, ...) #1\n'
        if opr_type == "SIGNED_INT":
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, i32 {})\n'.format(self.const_cnt, opr_name))
            self.const_cnt += 1
        elif opr_type == "SIGNED_FLOAT":
            self.consts += '@.const{} = private constant [3 x i8] c"%f\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, double {})\n'.format(self.const_cnt, opr_name))
            self.const_cnt += 1
        elif opr_type == "CHAR":
            self.consts += '@.const{} = private constant [3 x i8] c"%c\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, i8 {})\n'.format(self.const_cnt, opr_name))
            self.const_cnt += 1
        elif opr_type == "ESCAPED_STRING":
            self.consts += '@.const{} = private constant [3 x i8] c"%s\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.const_cnt += 1
            self.consts += '@.const{} = private constant [{} x i8] c"{}\\00"\n'.format(self.const_cnt, len(opr_name) + 1,
                                                                                       opr_name)
            self.tmp.write(
                '%var_str_ptr{1} = getelementptr inbounds [{0} x i8], [{0} x i8]* @.const{1}, i32 0, i32 0\n'.format(
                    len(opr_name) + 1, self.const_cnt))
            self.tmp.write(
                'call i32 (i8*, ...) @printf(i8* %str{}, i8* %var_str_ptr{})\n'.format(self.const_cnt - 1,
                                                                                       self.const_cnt))
            self.const_cnt += 1
        else:
            raise Exception('Unknown var type {}'.format(opr_type))

    def read(self, args):
        # todo test
        if args not in self.ST.keys():
            raise Exception('Error: {} is not declare in this scope.'.format(args))

        var_name = self.ST[args]['name']
        var_type = self.ST[args]['type']
        if 'declare i32 @scanf(i8*, ...) #1' not in self.dcls:
            self.dcls += 'declare i32 @scanf(i8*, ...) #1\n'
        if var_type == 'SIGNED_INT':
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @scanf(i8* %str{}, i32* {})\n'.format(self.const_cnt, var_name))
            self.const_cnt += 1
        elif var_type == 'SIGNED_FLOAT':
            self.consts += '@.const{} = private constant [3 x i8] c"%f\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @scanf(i8* %str{}, double* {})\n'.format(self.const_cnt, var_name))
            self.const_cnt += 1
        elif var_type == 'CHAR':
            self.consts += '@.const{} = private constant [3 x i8] c"%c\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @scanf(i8* %str{}, i8* {})\n'.format(self.const_cnt, var_name))
            self.const_cnt += 1
        elif var_type == 'ESCAPED_STRING':
            self.consts += '@.const{} = private constant [3 x i8] c"%s\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.tmp.write('%{0} = getelementptr inbounds [{1} x i8], [{1} x i8]* {2}, i32 0, i32 0\n'.format(
                self.temp_cnt[self.scope_level], STRING_MAX_SIZE, var_name))
            self.tmp.write('call i32 (i8*, ...) @scanf(i8* %str{}, i8* %{})\n'.format(self.const_cnt, self.temp_cnt[self.scope_level]))
            self.const_cnt += 1
            self.temp_cnt[self.scope_level] += 1
        else:
            raise Exception('Unknown var type {}'.format(var_type))

    def operand_fetch(self, opr, get_value):
        if opr.type == 'CNAME':
            if self.scope_level == 0 or opr.value not in self.ST_stack[self.scope_level]:
                if opr.value not in self.ST_stack[0]:
                    raise Exception('ERROR: {} is not defined.'.format(opr.value))
                else:
                    opr_type = self.ST_stack[0][opr.value]['type']
                    if self.ST_stack[0][opr.value]['is_temp']:
                        opr_name = '@' + self.ST_stack[0][opr.value]['name']
                    else:
                        opr_name = '@' + self.ST_stack[0][opr.value]['ptr_name']
                        if get_value is True:
                            self.tmp.write('{0}{1} = load {2}, {2}* {3}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], type_convert[opr_type], opr_name))
                            opr_name = var_sign[self.scope_level] + str(self.temp_cnt[self.scope_level])
                            self.temp_cnt[self.scope_level] += 1
            else:
                opr_type = self.ST[opr.value]['type']
                if self.ST[opr.value]['is_temp']:
                    opr_name = '%' + self.ST[opr.value]['name']
                else:
                    opr_name = '%' + self.ST[opr.value]['ptr_name']
                    if get_value is True:
                        self.tmp.write('{0}{1} = load {2}, {2}* {3}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], type_convert[opr_type], opr_name))
                        opr_name = var_sign[self.scope_level] + str(self.temp_cnt[self.scope_level])
                        self.temp_cnt[self.scope_level] += 1
        else:
            opr_type = opr.type
            opr_name = opr.value

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
                return 'false' if int(float(opr_name)) == 0 else 'true'
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
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

    def type_cast(self, res_type, opr_name, opr_type, const):
        if res_type == opr_type:
            return opr_name

        if opr_type == 'ESCAPED_STRING':
            raise Exception("ERROR: Illegal operand type")

        if const:
            return self.const_type_cast(res_type, opr_name, opr_type)

        if res_type == 'SIGNED_INT':
            if opr_type == 'SIGNED_FLOAT':
                self.tmp.write('{}{} = fptosi double {} to i32\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], opr_name))
            else:
                self.tmp.write('{}{} = zext i8 {} to i32\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], opr_name))

        elif res_type == 'SIGNED_FLOAT':
            if opr_type == 'SIGNED_INT':
                self.tmp.write('{}{} = sitofp i32 {} to double\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], opr_name))
            else:
                self.tmp.write('{}{} = sitofp i8 {} to double\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], opr_name))

        elif res_type == 'BOOL':
            if opr_type == 'SIGNED_FLOAT':
                self.tmp.write('{}{} = fcmp une double {}, 0.0\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], opr_name))
            else:
                self.tmp.write('{}{} = icmp ne {} {}, 0\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], type_convert[opr_type], opr_name))
            opr_name = '{}{}'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level])
            self.temp_cnt[self.scope_level] += 1
            self.tmp.write('{}{} = zext i1 {} to i8\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], opr_name))
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

        self.temp_cnt[self.scope_level] += 1
        return var_sign[self.scope_level] + str(self.temp_cnt[self.scope_level]-1)

    def do_calc_operation(self, opr1, opr2, op_type):
        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2, op_type)

        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)
        if res_type == 'SIGNED_INT':
            if op_type == 'mod' or op_type == 'div':
                op_type = 's' + op_type

            self.tmp.write('{}{} = {} nsw i32 {}, {}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_type, first_name, second_name))
            self.ST['{}__'.format(self.temp_cnt[self.scope_level])] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                                       "name": '{}'.format(self.temp_cnt[self.scope_level]), "is_temp": True}
        elif res_type == 'SIGNED_FLOAT':
            self.tmp.write('{}{} = f{} double {}, {}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_type, first_name, second_name))
            self.ST['{}__'.format(self.temp_cnt[self.scope_level])] = {"type": "SIGNED_FLOAT", "size": REAL_SIZE,
                                                                       "name": '{}'.format(self.temp_cnt[self.scope_level]), "is_temp": True}
        else:
            raise Exception('do_calc_operation: Internal Error.')

        self.ss.append(Node('{}__'.format(self.temp_cnt[self.scope_level]), 'CNAME'))
        self.temp_cnt[self.scope_level] += 1

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
        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2, 'bitwise_'+op_type)

        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        self.tmp.write('{}{} = {} i32 {}, {}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_type, first_name, second_name))
        self.ST['{}__'.format(self.temp_cnt[self.scope_level])] = {"type": "SIGNED_INT",
                                                                   "size": INT_SIZE,
                                                                   "name": '{}'.format(self.temp_cnt[self.scope_level]),
                                                                   "is_temp": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[self.scope_level]), 'CNAME'))
        self.temp_cnt[self.scope_level] += 1

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
        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2, 'boolean_'+op_type)

        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        self.tmp.write('{}{} = {} i8 {}, {}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_type, first_name, second_name))
        tmp_name = '{}{}'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level])
        self.temp_cnt[self.scope_level] += 1
        self.tmp.write('{}{} = trunc i8 {} to i1\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], tmp_name))
        self.ST['{}__'.format(self.temp_cnt[self.scope_level])] = {"type": "BOOL",
                                                                   "size": BOOL_SIZE,
                                                                   "name": '{}'.format(self.temp_cnt[self.scope_level]),
                                                                   "is_temp": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[self.scope_level]), 'CNAME'))
        self.temp_cnt[self.scope_level] += 1

    def boolean_and(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_boolean_calc(first, second, 'and')

    def boolean_or(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.do_boolean_calc(first, second, 'or')

    def do_compare_calc(self, opr1, opr2, op_type):
        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(opr1, opr2, op_type)

        first_name = self.type_cast(res_type, first_name, first_type, False if opr1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if opr2.type == 'CNAME' else True)

        self.tmp.write('{}{} = {} {} {} {}, {}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], COMP_SIGN_TO_FLAG[res_type]['op'], COMP_SIGN_TO_FLAG[res_type][op_type], type_convert[res_type], first_name, second_name))
        tmp_name = '{}{}'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level])
        self.temp_cnt[self.scope_level] += 1
        self.tmp.write('{}{} = zext i1 {} to i8\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], tmp_name))
        self.ST['{}__'.format(self.temp_cnt[self.scope_level])] = {"type": "BOOL",
                                                                   "size": BOOL_SIZE,
                                                                   "name": '{}'.format(self.temp_cnt[self.scope_level]),
                                                                   "is_temp": True}
        self.ss.append(Node('{}__'.format(self.temp_cnt[self.scope_level]), 'CNAME'))
        self.temp_cnt[self.scope_level] += 1

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

    def main_begin(self):
        self.tmp.write('define i32 @main() #0\n')
        self.tmp.write('{\n')

    def main_end(self):
        self.tmp.write('ret i32 0\n')
        self.tmp.write('}\n')

    def function_call(self, args):
        args = self.ss.pop()
        func_name = self.ss.pop()
        if str(func_name) == "read":
            # todo read
            return
        elif str(func_name) == "write":
            self.ss.append(args.get())
            self.write()
        elif str(func_name) == "strlen":
            # todo strlen
            return
        elif str(func_name) in self.ST_stack[0]:
            # todo func_call
            return
        else:
            raise Exception("Error. Function has not been declared in this scope.")

    def push_q(self, args):
        self.ss.append(Queue())

    def pop_ss_push_q(self, args):
        temp = self.ss.pop()
        self.ss[-1].put(temp)

    def assignment(self, args):
        rhs = self.ss.pop()
        lhs = self.ss.pop()

        lhs_type, lhs_name = self.operand_fetch(lhs, False)
        rhs_type, rhs_name = self.operand_fetch(rhs, True)

        rhs_name = self.type_cast(lhs_type, rhs_name, rhs_type, False if rhs.type == 'CNAME' else True)

        self.tmp.write('store {0} {1}, {0}* {2}\n'.format(type_convert[lhs_type], rhs_name, lhs_name))

    def jz(self, args):
        be = self.ss.pop()
        print(self.ST[be.value])
        pass

    def cjz(self, args):
        pass

    def cjp(self, args):
        pass

    def jp_cjz(self, args):
        pass

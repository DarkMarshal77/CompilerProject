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
        self.label_counter = 0

        self.scope_level = 0
        self.const_cnt = 0
        self.temp_cnt = [0, 0]
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
        self.ss.append(args[0])

    def empty_ss(self, args):
        self.ss = []

    def write(self):
        # todo print variable
        var = self.ss.pop()
        if 'declare i32 @printf(i8*, ...) #1' not in self.dcls:
            self.dcls += 'declare i32 @printf(i8*, ...) #1\n'
        if var.type == "SIGNED_INT":
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, i32 {})\n'.format(self.const_cnt, var))
            self.const_cnt += 1
        elif var.type is "SIGNED_FLOAT":
            self.consts += '@.const{} = private constant [3 x i8] c"%f\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, double {})\n'.format(self.const_cnt, var))
            self.const_cnt += 1
        elif var.type == "CHAR":
            self.consts += '@.const{} = private constant [3 x i8] c"%c\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, i8 {})\n'.format(self.const_cnt, ord(var)))
            self.const_cnt += 1
        elif var.type == "ESCAPED_STRING":
            var = var[1: -1]

            self.consts += '@.const{} = private constant [3 x i8] c"%s\\00"\n'.format(self.const_cnt)
            self.tmp.write('%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                self.const_cnt))
            self.const_cnt += 1
            self.consts += '@.const{} = private constant [{} x i8] c"{}\\00"\n'.format(self.const_cnt, len(var) + 1,
                                                                                       var)
            self.tmp.write(
                '%var_str_ptr{1} = getelementptr inbounds [{0} x i8], [{0} x i8]* @.const{1}, i32 0, i32 0\n'.format(
                    len(var) + 1, self.const_cnt))
            self.tmp.write(
                'call i32 (i8*, ...) @printf(i8* %str{}, i8* %var_str_ptr{})\n'.format(self.const_cnt - 1,
                                                                                       self.const_cnt))
            self.const_cnt += 1
        else:
            raise Exception('Unknown var type {}'.format(type(var)))

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

    def operand_fetch(self, op, get_value):
        if op.type == 'CNAME':
            if self.scope_level == 0 or op.value not in self.ST_stack[self.scope_level]:
                if op.value not in self.ST_stack[0]:
                    raise Exception('ERROR: {} is not defined.'.format(op.value))
                else:
                    op_type = self.ST_stack[0][op.value]['type']
                    if self.ST_stack[0][op.value]['is_temp']:
                        op_name = '@' + self.ST_stack[0][op.value]['name']
                    else:
                        op_name = '@' + self.ST_stack[0][op.value]['ptr_name']
                        if get_value is True:
                            self.tmp.write('{0}{1} = load {2}, {2}* {3}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], type_convert[op_type], op_name))
                            op_name = var_sign[self.scope_level] + str(self.temp_cnt[self.scope_level])
                            self.temp_cnt[self.scope_level] += 1
            else:
                op_type = self.ST[op.value]['type']
                if self.ST[op.value]['is_temp']:
                    op_name = '%' + self.ST[op.value]['name']
                else:
                    op_name = '%' + self.ST[op.value]['ptr_name']
                    if get_value is True:
                        self.tmp.write('{0}{1} = load {2}, {2}* {3}\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], type_convert[op_type], op_name))
                        op_name = var_sign[self.scope_level] + str(self.temp_cnt[self.scope_level])
                        self.temp_cnt[self.scope_level] += 1
        else:
            op_type = op.type
            op_name = op.value

        return op_type, op_name

    def result_type_wrapper(self, op1, op2, op_type):
        first_type, first_name = self.operand_fetch(op1, True)
        second_type, second_name = self.operand_fetch(op2, True)

        res_type = result_type(op_type, first_type, second_type)
        return first_type, first_name, second_type, second_name, res_type

    def const_type_cast(self, res_type, op_name, op_type):
        if res_type == 'SIGNED_INT':
            if op_type == 'SIGNED_FLOAT':
                return str(int(float(op_name)))
            elif op_type == 'BOOL':
                return '1' if op_name == 'true' else '0'
            elif op_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
            else:
                return str(ord(op_name))

        elif res_type == 'SIGNED_FLOAT':
            if op_type == 'BOOL':
                return '1.0' if op_name == 'true' else '0.0'
            elif op_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
            elif op_type == 'SIGNED_INT':
                return op_name + '.0'
            else:
                return str(ord(op_name)) + '.0'

        elif res_type == 'BOOL':
            if op_type == 'SIGNED_INT':
                return 'false' if int(op_name) == 0 else 'true'
            elif op_type == 'CHAR':
                return 'false' if ord(op_name) == 0 else 'true'
            elif op_type == 'SIGNED_FLOAT':
                return 'false' if int(float(op_name)) == 0 else 'true'
            elif op_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')

        elif res_type == 'CHAR':
            if op_type == 'SIGNED_INT':
                return op_name
            elif op_type == 'BOOL':
                return '1' if op_name == 'true' else '0'
            elif op_type == 'SIGNED_FLOAT':
                return str(int(float(op_name)))
            elif op_type == 'ESCAPED_STRING':
                raise Exception('ERROR: Unable to cast string')
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

    def type_cast(self, res_type, op_name, op_type, const):
        if res_type == op_type:
            return op_name

        if const:
            return self.const_type_cast(res_type, op_name, op_type)

        # todo: incomplete
        if res_type == 'SIGNED_INT':
            if op_type == 'SIGNED_FLOAT':
                self.tmp.write('{}{} = fptosi double {} to i32\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_name))
            else:
                self.tmp.write('{}{} = zext i8 {} to i32\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_name))

        elif res_type == 'SIGNED_FLOAT':
            if op_type == 'SIGNED_INT':
                self.tmp.write('{}{} = sitofp i32 {} to double\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_name))
            else:
                self.tmp.write('{}{} = sitofp i8 {} to double\n'.format(var_sign[self.scope_level], self.temp_cnt[self.scope_level], op_name))

        elif res_type == 'BOOL':
            pass
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

        self.temp_cnt[self.scope_level] += 1
        return var_sign[self.scope_level] + str(self.temp_cnt[self.scope_level]-1)

    def do_calc_operation(self, op1, op2, op_type):
        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(op1, op2, op_type)

        first_name = self.type_cast(res_type, first_name, first_type, False if op1.type == 'CNAME' else True)
        second_name = self.type_cast(res_type, second_name, second_type, False if op1.type == 'CNAME' else True)
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

        self.tmp.write('store {0} {1}, {0}* {2}'.format(type_convert[lhs_type], rhs_name, lhs_name))

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

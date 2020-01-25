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
        self.ST = self.ST_stack[-1]
        self.ss = []

        self.const_cnt = 0
        self.temp_cnt = 1
        self.dcls = ''
        self.consts = ''

        self.tmp = open("LLVM/tmp.ll", 'w')

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
        # todo allocations

        id = str(args[1])
        for symbol_table in self.ST_stack:
            if id in symbol_table:
                if id in INIT_ST:
                    print("'", id, "' is a reserved name. Try another name for your variable.")
                else:
                    print("Double declaration of '", id, "'")
                quit()
        if args[0] == "integer":
            self.ST[id] = {"type": "SIGNED_INT", "size": INT_SIZE}
        elif args[0] == "string":
            self.ST[id] = {"type": "ESCAPED_STRING"}
        elif args[0] == "real":
            self.ST[id] = {"type": "SIGNED_FLOAT", "size": REAL_SIZE}
        elif args[0] == "character":
            self.ST[id] = {"type": "CHAR", "size": CHAR_SIZE}
        elif args[0] == "boolean":
            self.ST[id] = {"type": "BOOL", "size": BOOL_SIZE}

    def integer_push(self, args):
        return "integer"

    def real_push(self, args):
        return "real"

    def string_push(self, args):
        return "string"

    def character_push(self, args):
        return "character"

    def boolean_push(self, args):
        return "boolean"

    def id(self, args):
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
        if var.type == "SIGNED_INTEGER":
            self.consts += '@.const{} = private constant [3 x i8] c"%d\\00"\n'.format(self.const_cnt)
            self.tmp.write(
                '%str{0} = getelementptr inbounds [3 x i8], [3 x i8]* @.const{0}, i32 0, i32 0\n'.format(
                    self.const_cnt))
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str{}, i32 {})\n'.format(self.const_cnt, var))
            self.const_cnt += 1
        elif type(var) is float:
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
                self.temp_cnt, STRING_MAX_SIZE, var_name))
            self.tmp.write('call i32 (i8*, ...) @scanf(i8* %str{}, i8* %{})\n'.format(self.const_cnt, self.temp_cnt))
            self.const_cnt += 1
            self.temp_cnt += 1
        else:
            raise Exception('Unknown var type {}'.format(var_type))

    def result_type_wrapper(self, op1, op2, op_type):
        if op1.type == 'CNAME':
            if op1.value not in self.ST:
                if op1.value not in self.ST_stack[0]:
                    raise Exception()
                else:
                    first_type = self.ST_stack[0][op1.value]['type']
                    first_name = '@' + self.ST_stack[0][op1.value]['type']
            else:
                first_type = self.ST[op1.value]['type']
                first_name = '%' + self.ST[op1.value]['type']
        else:
            first_type = op1.type
            first_name = op1.value

        if op2.type == 'CNAME':
            if op2.value not in self.ST:
                if op2.value not in self.ST_stack[0]:
                    raise Exception()
                else:
                    second_type = self.ST_stack[0][op2.value]['type']
                    second_name = '@' + self.ST_stack[0][op2.value]['type']
            else:
                second_type = self.ST[op2.value]['type']
                second_name = '%' + self.ST[op2.value]['type']
        else:
            second_type = op2.type
            second_name = op2.value

        res_type = result_type(op_type, first_type, second_type)
        return first_type, first_name, second_type, second_name, res_type

    def type_cast(self, res_type, op_name, op_type):
        if res_type == op_type:
            return op_name

        if res_type == 'SIGNED_INT':
            if op_type == 'SIGNED_FLOAT':
                self.tmp.write('%{} = fptosi double {} to i32'.format(self.temp_cnt, op_name))
            else:
                self.tmp.write('%{} = zext i8 {} to i32'.format(self.temp_cnt, op_name))

            self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                     "name": '{}'.format(self.temp_cnt)}
        elif res_type == 'SIGNED_FLOAT':
            if op_type == 'SIGNED_INT':
                self.tmp.write('%{} = sitofp i32 {} to double'.format(self.temp_cnt, op_name))
            else:
                self.tmp.write('%{} = sitofp i8 {} to double'.format(self.temp_cnt, op_name))

            self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_FLOAT", "size": REAL_SIZE,
                                                     "name": '{}'.format(self.temp_cnt)}
        elif res_type == 'BOOL':
            pass
        else:
            raise Exception('FATAL ERROR: {} type is not defined'.format(res_type))

        self.temp_cnt += 1
        return '%' + str(self.temp_cnt-1)

    def do_calc_operation(self, op1, op2, op_type):
        first_type, first_name, second_type, second_name, res_type = self.result_type_wrapper(op1, op2, op_type)

        first_name = self.type_cast(res_type, first_name, first_type)
        second_name = self.type_cast(res_type, second_name, second_type)
        if res_type == 'SIGNED_INT':
            if op_type == 'mod' or op_type == 'div':
                op_type = 's' + op_type

            self.tmp.write('%{} = {} nsw i32 {}, {}'.format(self.temp_cnt, op_type, first_name, second_name))
            self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                     "name": '{}'.format(self.temp_cnt)}
        elif res_type == 'SIGNED_FLOAT':
            self.tmp.write('%{} = f{} double {}, {}'.format(self.temp_cnt, op_type, first_name, second_name))
            self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_FLOAT", "size": REAL_SIZE,
                                                     "name": '{}'.format(self.temp_cnt)}

        self.ss.append(Node('{}__'.format(self.temp_cnt), 'CNAME'))
        self.temp_cnt += 1

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

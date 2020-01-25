import atexit
from lark import Transformer
from CONFIG import *
from queue import Queue


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
            self.ST[id] = {"type": "CHARACTER", "size": CHAR_SIZE}
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

    def add(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.tmp.write('%{} = add i32 {}, {}'.format(self.temp_cnt, self.ST[first]['name'], self.ST[second]['name']))
        self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                 "name": '%{}'.format(self.temp_cnt)}
        self.ss.append('{}__'.format(self.temp_cnt))
        self.temp_cnt += 1

    def sub(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.tmp.write('%{} = sub i32 {}, {}'.format(self.temp_cnt, self.ST[first]['name'], self.ST[second]['name']))
        self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                 "name": '%{}'.format(self.temp_cnt)}
        self.ss.append('{}__'.format(self.temp_cnt))
        self.temp_cnt += 1

    def mult(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.tmp.write('%{} = mul i32 {}, {}'.format(self.temp_cnt, self.ST[first]['name'], self.ST[second]['name']))
        self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                 "name": '%{}'.format(self.temp_cnt)}
        self.ss.append('{}__'.format(self.temp_cnt))
        self.temp_cnt += 1

    def div(self, args):
        second = self.ss.pop()
        first = self.ss.pop()

        self.tmp.write('%{} = sdiv i32 {}, {}'.format(self.temp_cnt, self.ST[first]['name'], self.ST[second]['name']))
        self.ST['{}__'.format(self.temp_cnt)] = {"type": "SIGNED_INT", "size": INT_SIZE,
                                                 "name": '%{}'.format(self.temp_cnt)}
        self.ss.append('{}__'.format(self.temp_cnt))
        self.temp_cnt += 1

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

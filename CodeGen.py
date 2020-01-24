import atexit

from lark import Transformer

from CONFIG import *


class CodeGen(Transformer):
    def __init__(self):
        super().__init__()
        atexit.register(self.cleanup)
        self.ST_stack = [INIT_ST]
        self.ST = self.ST_stack[-1]
        self.ss = []

        self.cont_cnt = 0
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
                print("Double Declaration")
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
        return args[0]

    def push_ss(self, args):
        self.ss.append(args)

    def empty_ss(self, args):
        self.ss = []

    def write(self):
        var = self.ss[-1]
        self.dcls += 'declare i32 @printf(i8*, ...) #1\n'
        if type(var) is int:
            self.consts += '@.const{} = private constant [5 x i8] c"%d\\0A\\0D\\00"\n'.format(self.cont_cnt)
            self.tmp.write('%str = getelementptr inbounds [5 x i8], [5 x i8]* @.const{}, i32 0, i32 0\n'.format(self.cont_cnt))
            self.cont_cnt += 1
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str, i32 {})\n'.format(var))
        elif type(var) is float:
            self.consts += '@.const{} = private constant [5 x i8] c"%f\\0A\\0D\\00"\n'.format(self.cont_cnt)
            self.tmp.write('%str = getelementptr inbounds [5 x i8], [5 x i8]* @.const{}, i32 0, i32 0\n'.format(self.cont_cnt))
            self.cont_cnt += 1
            self.tmp.write('call i32 (i8*, ...) @printf(i8* %str, double {})\n'.format(var))
        elif type(var) is str:
            if len(var) == 1:
                self.consts += '@.const{} = private constant [5 x i8] c"%c\\0A\\0D\\00"\n'.format(self.cont_cnt)
                self.tmp.write('%str = getelementptr inbounds [5 x i8], [5 x i8]* @.const{}, i32 0, i32 0\n'.format(self.cont_cnt))
                self.cont_cnt += 1
                self.tmp.write('call i32 (i8*, ...) @printf(i8* %str, i8 {})\n'.format(ord(var)))
            else:
                self.consts += '@.const{} = private constant [5 x i8] c"%s\\0A\\0D\\00"\n'.format(self.cont_cnt)
                self.tmp.write('%str = getelementptr inbounds [5 x i8], [5 x i8]* @.const{}, i32 0, i32 0\n'.format(self.cont_cnt))
                self.cont_cnt += 1
                self.consts += '@.const{} = private constant [{} x i8] c"{}\\00"\n'.format(self.cont_cnt, len(var)+1, var)
                self.tmp.write('%var_str_ptr = getelementptr inbounds [{0} x i8], [{0} x i8]* @.const{1}, i32 0, i32 0\n'.format(len(var)+1, self.cont_cnt))
                self.cont_cnt += 1
                self.tmp.write('call i32 (i8*, ...) @printf(i8* %str, i8* %var_str_ptr)\n')
        else:
            raise Exception('Unknown var type {}'.format(type(var)))

    def main_begin(self):
        self.tmp.write('define i32 @main() #0\n')
        self.tmp.write('{\n')

    def main_end(self):
        self.tmp.write('ret i32 0\n')
        self.tmp.write('}\n')

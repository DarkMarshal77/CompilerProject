from lark import Transformer
from CONFIG import *


class CodeGen(Transformer):
    def __init__(self):
        super().__init__()
        self.ST = INIT_ST
        self.ss = []
        self.pc = 0
        self.dest = "main.ll"

        file = open(self.dest, 'w')
        file.close()

    def add_to_st(self, args):
        # todo allocations

        id = str(args[1])
        if id in self.ST:
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
        self.ss.append(args[0])

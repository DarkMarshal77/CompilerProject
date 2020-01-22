from lark import Transformer
from CONFIG import *


class CodeGen(Transformer):
    def __init__(self):
        super().__init__()
        self.ST = dict()
        self.ss = []

    def add_to_st(self, args):
        # todo allocations

        id = str(args[1])
        if id in self.ST:
            print("Double Declaration")
            quit()
        if args[0] == "integer":
            self.ST[id] = {"type": "integer", "size": INT_SIZE}
        elif args[0] == "string":
            self.ST[id] = {"type": "string"}
        elif args[0] == "real":
            self.ST[id] = {"type": "real", "size": REAL_SIZE}
        elif args[0] == "character":
            self.ST[id] = {"type": "character", "size": CHAR_SIZE}
        elif args[0] == "boolean":
            self.ST[id] = {"type": "character", "size": BOOL_SIZE}

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

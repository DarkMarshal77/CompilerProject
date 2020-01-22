from lark import Transformer


class CodeGen(Transformer):
    def __init__(self):
        super().__init__()
        self.ST = dict()

    def add(self, args):
        print("add", args[0], args[1])
        ST["alaki"] = {"Type": "INTEGER", "size": 4, }
        return int(args[0]) + int(args[1])

    def sub(self, args):
        return int(args[0]) - int(args[1])
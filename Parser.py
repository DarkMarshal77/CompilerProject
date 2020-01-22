from lark import Lark
from CodeGen import CodeGen

grammar = """
start: func_def start
     | proc_def start
     | var_dcl start
     |
     
id : WORD
func_def: "function" id 
proc_def: NUMBER
var_dcl: WORD NUMBER

%import common.NUMBER
%import common.WORD
%import common.WS
%ignore WS
"""

parser = Lark(grammar, parser="lalr", transformer=CodeGen())
print(parser.parse("""

"""))


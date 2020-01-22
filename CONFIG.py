INT_SIZE = 4
BOOL_SIZE = 1
CHAR_SIZE = 1
REAL_SIZE = 4

types = ["SIGNED_INT", "ESCAPED_STRING", "SIGNED_FLOAT", "CHARACTER", "BOOL"]

INIT_ST = {"array": {},
           "assign": {},
           "boolean": {},
           "break": {},
           "begin": {},
           "char": {},
           "continue": {},
           "do": {},
           "else": {},
           "end": {},
           "function": {},
           "procedure": {},
           "if": {},
           "integer": {},
           "of": {},
           "real": {},
           "return": {},
           "string": {},
           "while": {},
           "var": {},
           "false": {"type": "BOOL", "size": BOOL_SIZE},
           "true": {"type": "BOOL", "size": BOOL_SIZE}}

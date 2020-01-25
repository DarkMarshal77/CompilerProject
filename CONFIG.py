INT_SIZE = 4
BOOL_SIZE = 1
CHAR_SIZE = 1
REAL_SIZE = 4
STRING_MAX_SIZE = 512

Null = "\00"

types = ["SIGNED_INT", "ESCAPED_STRING", "SIGNED_FLOAT", "CHARACTER", "BOOL"]

type_convert = {"SIGNED_INT": "i" + str(INT_SIZE * 8),
                "SIGNED_FLOAT": "double",
                "CHARACTER": "i1",
                "BOOL": "i1"
                }

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
           "true": {"type": "BOOL", "size": BOOL_SIZE}
           }

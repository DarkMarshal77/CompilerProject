INT_SIZE = 4
BOOL_SIZE = 1
CHAR_SIZE = 1
REAL_SIZE = 4
STRING_MAX_SIZE = 512

Null = "\00"

types = ["SIGNED_INT", "ESCAPED_STRING", "SIGNED_FLOAT", "CHAR", "BOOL"]

type_convert = {"SIGNED_INT": "i" + str(INT_SIZE * 8),
                "SIGNED_FLOAT": "double",
                "CHAR": "i8",
                "BOOL": "i8",
                "ESCAPED_STRING": "i8*",
                }

var_sign = ['@', '%']

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
           "write": {},
           "read": {},
           "false": {"type": "BOOL", "size": BOOL_SIZE},
           "true": {"type": "BOOL", "size": BOOL_SIZE}
           }

unary_op = ["-", "~"]

OP_NAME_TO_SIGN = {"add": "+",
                   "sub": "-",
                   "mul": "*",
                   "div": "/",
                   "rem": "%",
                   }

bitwise_op = ["|", "^", "&"]
boolean_op = ["and", "or"]
compare_op = [">", "<", ">=", "<=", "==", "<>"]
calc_op = ["+", "*", "/", "%", "-"]


def result_type(operation, type1, type2):
    combined_types = (type1, type2)
    if combined_types == ("SIGNED_INT", "SIGNED_INT") and OP_NAME_TO_SIGN[operation] in calc_op + bitwise_op + compare_op:
        return "SIGNED_INT"
    if combined_types == ("SIGNED_INT", "SIGNED_INT") and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"

    if combined_types in [("SIGNED_INT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_INT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_INT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_INT", "BOOL"), ("BOOL", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("SIGNED_INT", "BOOL"), ("BOOL", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_INT", "BOOL"), ("BOOL", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_INT", "CHAR"), ("CHAR", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("SIGNED_INT", "CHAR"), ("CHAR", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_INT", "CHAR"), ("CHAR", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_FLOAT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_FLOAT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_FLOAT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_FLOAT", "BOOL"), ("BOOL", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_FLOAT", "BOOL"), ("BOOL", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_FLOAT", "BOOL"), ("BOOL", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_FLOAT", "CHAR"), ("CHAR", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_FLOAT", "CHAR"), ("CHAR", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_FLOAT", "CHAR"), ("CHAR", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("BOOL", "BOOL"), ("BOOL", "BOOL")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("BOOL", "BOOL"), ("BOOL", "BOOL")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("BOOL", "BOOL"), ("BOOL", "BOOL")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("BOOL", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("BOOL", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("BOOL", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("CHAR", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("CHAR", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("CHAR", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

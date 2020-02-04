from lark import Lark
from Tests import *
from CodeGen import CodeGen

grammar = """
start: func_def start
     | proc_def start
     | global_var_dcl ";" start
     |

global_var_dcl: global_simple_var
       | global_array_var
       
global_simple_var: id ":" type global_assignment_prime

global_assignment_prime: global_assignment -> global_def_assignment
                | -> global_def
          
global_array_var: "array" type id global_assignment_prime
         
global_assignment: ":=" constant -> push_ss

var_dcl: simple_var
       | array_var
       
simple_var: id ":" type add_to_st assignment_prime
add_to_st: -> add_to_st
assignment_prime: assignment
                | -> pop_ss
          
array_var: id ":" "array" push_q "[" dims "]" "of" type -> make_array_dscp
dims: expr pop_ss_push_q dims_prime
dims_prime: "," expr pop_ss_push_q dims_prime
          | 
         
assignment: ":=" expr -> assignment

func_def: "function" in_func_def_true push_st id push_q "(" args ")" ":" type call_func_def in_func_def_false block -> close_bracket
call_func_def: -> function_def
push_st: -> push_st
in_func_def_true: -> in_func_def_true
in_func_def_false: -> in_func_def_false

proc_def: "procedure" in_func_def_true push_st id push_q "(" args ")" call_proc_def in_func_def_false block -> close_bracket_proc
call_proc_def: -> proc_def

args: var_dcl pop_ss_push_q args_prime
    | 
args_prime: "," var_dcl pop_ss_push_q args_prime
          | 
pop_ss_push_q: -> pop_ss_push_q

block: "begin" push_st stl "end" pop_st
pop_st: -> pop_st

stl: st ";" empty_ss stl
   | loop empty_ss stl
   | conditional empty_ss stl
   |
empty_ss: -> empty_ss

st: bulk
  | expr
  | id assignment
  | arr_use assignment
  | var_dcl
  | loop 
  | "return" expr -> ret
  | conditional

id_plus: "," id id_plus 
       | "," id
       | "," arr_use
       | "," arr_use id_plus

// ___________________________________________ expression handling here
op: constant -> push_ss
  | function_call
  | id
  | arr_use

// _______________________ or and
expr: expr "or" expr_or -> boolean_or
    | expr_or
expr_or: expr_or "and" e -> boolean_and
       | e
       
// _______________________ | ^ & 
e: e "|" e_or -> bitwise_or
 | e_or
e_or: e_or "^" e_xor -> bitwise_xor
    | e_xor
e_xor: e_xor "&" e_and -> bitwise_and
     | e_and
     
// _______________________ >= > < <= == <>
e_and: e_and "==" e_eq -> comp_eq
     | e_and "<>" e_eq -> comp_ne
     | e_eq
e_eq: e_eq ">" e_lg -> comp_gt
    | e_eq ">=" e_lg -> comp_ge
    | e_eq "<" e_lg -> comp_lt
    | e_eq "<=" e_lg -> comp_le
    | e_lg

// _______________________ + - / * % - ~
e_lg: e_lg "+" t -> add
    | e_lg "-" t -> sub
    | t
t: t "*" f -> mul
 | t "/" f -> div
 | t "%" f -> mod
 | f
f: "-" p -> unary_sub
 | "~" p -> unary_not
 | p
p: op
 | "(" expr ")"

// ___________________________________________________________________
function_call: id push_q "(" exprs ")" -> function_call

push_q: -> push_q

exprs: expr pop_ss_push_q exprs_prime
     | 
exprs_prime: "," expr pop_ss_push_q exprs_prime
           | 
           
id: CNAME -> id

arr_use: id push_q "[" dims "]" -> calc_arr_index

?constant: SIGNED_INT
         | HEX -> hex_convert
         | SIGNED_FLOAT
         | ESCAPED_STRING
         | CHAR 
         
HEX: "0x" SIGNED_INT
   | "-" "0x" SIGNED_INT

?type: "integer" -> integer_push
     | "real" -> real_push
     | "string" -> string_push
     | "boolean" -> boolean_push
     | "character" -> character_push
     | "long" -> long_push

loop: make_begin_label_loop "while" "(" expr ")" branch_middle_loop "do" block -> jp_begin_loop
make_begin_label_loop: -> make_begin_label_loop
branch_middle_loop: -> branch_middle_loop

conditional: "if" "(" expr ")" jz "then" block ep

jz: -> jz
jp_cjz: -> jp_cjz

ep: "else" jp_cjz block -> cjp
  | -> cjz
 
CHAR: /'[^']*'/

bulk: "(" id "," init_bulk bulk_left ")" ":=" push_q "(" bulk_right ")" -> bulk
    | "(" arr_use "," init_bulk bulk_left ")" ":=" push_q "(" bulk_right ")" -> bulk
bulk_left: id pop_ss_push_q id_plus_bulk
         | arr_use pop_ss_push_q id_plus_bulk
bulk_right: exprs
id_plus_bulk: "," id pop_ss_push_q id_plus_bulk 
            | "," arr_use pop_ss_push_q id_plus_bulk 
            |
init_bulk: -> init_bulk

%import common.SIGNED_NUMBER
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
//%import common.ESCAPED_STRING
ESCAPED_STRING: /"[^"]*"/
%import common.NEWLINE
%import common.CNAME
//%import common.WS
WS: /(\\v|\\t|\\n|\\r|\\f| )/+
%ignore WS

COMMENT: "<--" /(.|\\v|\\t|\\n|\\r|\\f)+/ "-->"    
       | "--" /(.)+/ NEWLINE
       | "//" /(.)+/ NEWLINE
%ignore COMMENT
"""

parser = Lark(grammar, parser="lalr", transformer=CodeGen(), debug=False)

print(parser.parse(test20).pretty())

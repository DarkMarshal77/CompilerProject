from lark import Lark

from CodeGen import CodeGen

grammar = """
start: func_def start
     | proc_def start
     | var_dcl ";" start
     |

var_dcl: simple_var
       | array_var
       
simple_var: type id add_to_st assignment_prime
add_to_st: -> add_to_st
assignment_prime: assignment
                |
          
array_var: "array" type id assignment_prime
         
assignment: ":=" expr -> assignment
       
func_def: "function" id "(" args ")" ":" type block

proc_def: "procedure" id "(" args ")" block

args: var_dcl args_prime
    | 
args_prime: "," var_dcl args_prime
          | 

block: "begin" stl "end"

stl: st ";" empty_ss stl
   | 
empty_ss: -> empty_ss

st: expr
  | "(" id id_plus ")" assignment
  | id assignment
  | var_dcl
  | loop 
  | "return" id
  | conditional

id_plus: "," id id_plus 
       | "," id
// ___________________________________________ expression handling here
op: constant -> push_ss
  | function_call
  | id

// _______________________ or and
expr: expr_or "or" expr -> boolean_or
    | expr_or
expr_or: e "and" expr_or -> boolean_and
       | e
       
// _______________________ | ^ & 
e: e_or "|" e -> bitwise_or
 | e_or
e_or: e_xor "^" e_or -> bitwise_xor
    | e_xor
e_xor: e_and "&" e_xor -> bitwise_and
     | e_and
     
// _______________________ >= > < <= == <>
e_and: e_eq "==" e_and -> comp_eq
     | e_eq "<>" e_and -> comp_ne
     | e_eq
e_eq: e_lg ">" e_eq -> comp_gt
    | e_lg ">=" e_eq -> comp_ge
    | e_lg "<" e_eq -> comp_lt
    | e_lg "<=" e_eq -> comp_le
    | e_lg

// _______________________ + - / * % - ~
e_lg: t "+" e_and -> add
     | t "-" e_and -> sub
     | t
t: f "*" t -> mul
 | f "/" t -> div
 | f "%" t -> mod
 | f
f: "-" p
 | "~" p
 | p
p: op
 | "(" expr ")"

// ___________________________________________________________________
function_call: id push_q "(" exprs ")" -> function_call

push_q: -> push_q

exprs: expr exprs_prime -> pop_ss_push_q
     | 
exprs_prime: "," expr exprs_prime
           | 
           
id: CNAME -> id

?constant: SIGNED_INT
        | "0x" SIGNED_INT
        | SIGNED_FLOAT
        | ESCAPED_STRING
        | "\'" CHAR "\'"

?type: "integer" -> integer_push
    | "real" -> real_push
    | "string" -> string_push
    | "boolean" -> boolean_push
    | "char" -> character_push

loop: make_begin_label_loop "while" "(" expr ")" branch_middle_loop "do" block -> jp_begin_loop
make_begin_label_loop: -> make_begin_label_loop
branch_middle_loop: -> branch_middle_loop

conditional: "if" "(" expr ")" jz "then" block ep

jz: -> jz
jp_cjz: -> jp_cjz

ep: "else" jp_cjz block -> cjp
  | -> cjz
 
CHAR: /./

%import common.SIGNED_NUMBER
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.ESCAPED_STRING
%import common.NEWLINE
%import common.CNAME
%import common.WS
%ignore WS

COMMENT: "<--" /(.|\\n|\\r)+/ "-->"    
       | "--" /(.)+/ NEWLINE
%ignore COMMENT
"""

parser = Lark(grammar, parser="lalr", transformer=CodeGen(), debug=False)
# parser = Lark(grammar)

# print(parser.parse("""
# <-- salam salam
# hello world!
# -->
# function main() : integer
# begin
# real b;
# integer a;
# char c;
# string s := "salam";
# if (9 + b(20)) then
# begin
# a := -10.941 + b;
# c := 't';
# end
# else begin
# a := a + b;
# -- salamdsfadsjfkaldg;
# end;
# end
# """).pretty())

print(parser.parse("""
function main() : integer
begin

integer a;
integer b;
--while (a + b) do begin
--    a := 2;
--end;

if(a + b) then begin
    a := 1;
end
else begin
    a := 2;
end;

end
""").pretty())

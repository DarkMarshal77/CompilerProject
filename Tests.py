test1 = """
procedure f(integer a) begin
    write(a);
end

function main() : integer
begin
    integer a := 10;
    f(a);
    return 0;
end
"""

test2 = """
function fib(integer  n): integer
begin
    if (n == 1 or n == 0) then begin 
        return 1;
    end else begin
        return fib(n - 2) + fib(n - 1);
    end
end

function main(): integer begin
    integer a := 0;
    while(a <= 20) do begin
        write("fib of ");
        write(a);
        write(" is: ");
        write(fib(a));
        write('\n');
        a := a + 1;
    end
    return 0;
end
"""

test3 = """
function main(): integer begin
    integer a := 2;
    integer b := 3;
    
    real c := 4.1;
    real d := 5.9;
    
    char e := 'a';
    char f := 'b';
    
    boolean g := true;
    boolean h := false;
    
    write(a + b * c);
    write('\n');
    write((a + b) * c);
    write('\n');
    write(b - 3 or e - 'a');
    write('\n');
    write(b - 2 or e - 'a');
    write('\n');
    write(b - 2 and e - 'a');
    write('\n');
    write(b - 2 or e - 'b');
    write('\n');
    write(b - g);
    write('\n');
    write(a * b + 13 % 4);
    write('\n');
    write((a * b + 13) % 4);
end
"""

test4 = """
integer a := 10;

procedure f(integer b) begin
    integer a := 2;
    write(a);
    write('\n');
end

procedure g(integer b) begin
    real a := 1.5;
    write(a);
    write('\n');
end

procedure h(integer a) begin
    write(a);
    write('\n');
end

procedure i(integer b) begin
    write(a);
    write('\n');
end

function main(): integer begin
    f(0);g(0);h(0);i(0);
end
"""

test5 = """
integer a := 1;
function main(): integer begin
    write(a);
    integer a := 2;
    write(a);
    if(true) then begin
        write(a);
        integer a := 3;
        write(a);
    end
    write(a);
    return 0;
end
"""

test6 = """
function f(): integer begin
    return 0;
end

procedure g() begin
    write(1);
end

function main(): integer begin
    write(f());g();
    return 1;
end
"""

test7 = """
function main(): integer begin
    integer a := 1;
    real  b := 3;
    char c := 'c';
    
    if (a == 1) then begin
        if (b == 3) then begin
            while (c <> 106) do begin
                c := c + 1;
            end
            write(c);
        end
    end else begin
        write(-1);
    end
end
"""

test8 = """
function main(): integer begin
    integer a  := 18 - 2 + 1;
    write(a);
end
"""

test9 = """
function main(): integer begin
    integer a  := - 2;
    write(a);
end
"""

test10 = """
function write(): integer begin
    return 0;
end

function main(): integer begin
    return 0;
end
"""

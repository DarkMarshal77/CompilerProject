test1 = """
procedure f(a: integer) begin
    write(a);
end

function main() : integer
begin
    a: integer := 10;
    f(a);
    return 0;
end
"""

test2 = """
function fib(n: integer): integer
begin
    if (n == 1 or n == 0) then begin 
        return 1;
    end else begin
        return fib(n - 2) + fib(n - 1);
    end
end

function main(): integer begin
    a:integer := 0;
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
    a:integer := 2;
    b:integer := 3;
    
    c :real := 4.1;
    d :real := 5.9;
    
    e : character := 'a';
    f : character := 'b';
    
    g: boolean := true;
    h: boolean := false;
    
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
a: integer := 10;

procedure f(b: integer) begin
    a: integer := 2;
    write(a);
    write('\n');
end

procedure g(b: integer) begin
    a: real := 1.5;
    write(a);
    write('\n');
end

procedure h(a: integer) begin
    write(a);
    write('\n');
end

procedure i(b: integer) begin
    write(a);
    write('\n');
end

function main(): integer begin
    f(0);g(0);h(0);i(0);
end
"""

test5 = """
a: integer := 1;
function main(): integer begin
    write(a);
    a: integer := 2;
    write(a);
    if(true) then begin
        write(a);
        a: integer := 3;
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
    a: integer := 1;
    b: real := 3;
    c: character := 'c';
    
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
    a: integer := 18 - 2 + 1;
    write(a);
end
"""

test9 = """
function main(): integer begin
    a: integer := - 2;
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

test11 = """
function main(): integer begin
    a: character := 5;
    b: character := 1.5;
    (a, b) := ('a', 'b');
    write(a);
    write('\n');
    write(b);
    write('\n');
end
"""

test12 = """
function main(): integer begin
    a: array integer of [4];
    i: integer := 0;
    
    a[0] := 1;
    a[1] := 2;

    (a[0], a[1]) := (a[1], a[0]);
    write(a[0]);
    write("\n");
    write(a[1]);
end
"""

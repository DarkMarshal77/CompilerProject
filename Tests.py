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
    a: array [4]] of integer;
    i: integer := 0;
    
    a[0] := 1;
    a[1] := 2;

    (a[0], a[1]) := (a[1], a[0]);
    write(a[0]);
    write("\n");
    write(a[1]);
end
"""

test13 = """
function main(): integer begin
    fib: array [2000] of integer;
    fib[0] := 1;
    fib[1] := 1;
    
    i: integer := 2;
    while (i <= 30) do begin
        fib[i] := fib[i - 1] + fib[i - 2];
        write(fib[i]);
        write("\n");
        i := i + 1;
    end
end
"""

test14 = """
function main(): integer begin
    comb: array [100, 100] of integer;
    
    n: integer := 1;
    k: integer := 1;
    while (n < 30) do begin
        k := 1;
        while (k <= n) do begin
            if (k == 1) then begin
                comb[n, k] := n;
            end else begin
                if (n == k) then begin
                    comb[n, k] := 1;
                end else begin
                    comb[n, k] := comb[n - 1, k] + comb[n - 1, k - 1]; 
                end  
            end
            
            write(n);
            write(", ");
            write(k);
            write(": ");
            write(comb[n, k]);
            write("\n");
            
            k := k + 1;
        end
        n := n + 1;
    end
end
"""

test15 = """
function main(): integer begin
    s: array [100] of character;
    s[0] := 'a';
    s[1] := 's';
    s[2] := 'h';
    s[3] := 'k';
    s[4] := 'a';
    s[5] := 'n';
    s[6] := '\0';
    i: integer := 0;
    
    while (i <= 5) do begin
        write(s[i]);
        i := i + 1;
    end
end
"""

test16 = """
function main(): integer begin
    s: array [10] of boolean;
    i: integer := 0;
    while (i < 10) do begin
        if (i % 2 == 0) then begin
            s[i] := true;
        end else begin
            s[i] := false;
        end
        i := i + 1;
    end
    
    i := 0;
    while (i < 10) do begin
        write(i);
        write(" ");
        write(s[i]);
        write("\n");
        i := i + 1;
    end
end
"""

test17 = """
//this is a comment

function main(): integer begin
    write("salam");
    <-- write("comment");
    write("also comment");
    write("here comment again");-->
    write(" khubi?");
    --      write("comment");
    return 0;
end
"""

test18 = """
function main(): integer begin
    n: integer;
    read(n);
    write(n);
    write("\n");
    
    arr : array [n] of character;
    i: integer;
    i := 0;
    
    while (i < n) do begin
        arr[i] := i;
        i:= i + 1;
    end
    
    i:= 0;
    while (i < n) do begin
        write(i);
        write(' ');
        write(arr[i]);
        write('\n');
        i := i + 1;
    end
end 
"""

test19 = """
function main(): integer begin
    a: long := 1;
    while (a < 1000000000000000000000000) do begin
        write(a);
        write("\n");
        a:= a * 4;
    end
end 
"""

test20 = """
function main(): integer begin
    n: long := 90;
    fib: array [n] of long;
    fib[0] := 1;
    fib[1] := 1;
    
    i: integer := 2;
    while (i < n) do begin
        fib[i] := fib[i - 1] + fib[i - 2];
        write(fib[i]);
        write("\n");
        i := i + 1;
    end
end
"""

test21 = """
comb: array [100, 100] of integer;
function main(): integer begin    
    n: integer := 1;
    k: integer := 1;
    while (n < 30) do begin
        k := 1;
        while (k <= n) do begin
            if (k == 1) then begin
                comb[n, k] := n;
            end else begin
                if (n == k) then begin
                    comb[n, k] := 1;
                end else begin
                    comb[n, k] := comb[n - 1, k] + comb[n - 1, k - 1]; 
                end  
            end
            
            write(n);
            write(", ");
            write(k);
            write(": ");
            write(comb[n, k]);
            write("\n");
            
            k := k + 1;
        end
        n := n + 1;
    end
end
"""

test22 = """
glob_c1: array [100] of character;
glob_c2: array [100] of character;
str: string;
function main(): integer 
begin
    c: array [100] of character;
    c2: array [100] of character;
    str := "fkjh fhghkbkhb bg";
    //write(str);
    glob_c1 := str;
    glob_c2 := glob_c1;
    write(glob_c2[0]);
    write('\n');
    c := str;
    glob_c2 := c;
    write(glob_c2[0]);
    write('\n');
    glob_c1 := str;
    c := glob_c1;
    write(c[0]);
    write('\n');
    c2 := str;
    c := c2;
    write(c[0]);
end
"""

test23 = """
dp: array [10000] of long;

function fib(n: integer): long begin
    if (n = 1 or n = 2) then begin
        temp: long := 1;
        return temp;
    end
    if (~dp[n]) then begin
        dp[n] := fib(n - 1) + fib(n - 2);
        return dp[n];
    end else begin
        return dp[n];
    end
end

function main(): integer begin
    i: integer := 0;

    while (i < 10000) do begin
        dp[i] := 0;
        i := i + 1;
    end

    n: integer;
    read(n);
    write(fib(n));
end
"""

test24 = """
global: array [10] of integer;

procedure print_arr(n: array [22] of character)
begin
    i: integer := 0;
    while i < 22 do
    begin
        write("n[");
        write(i);
        write("] = ");
        write(n[i]);
        write('\n');
        i := i+1;
    end
end

procedure init_arr(n: array [22] of character)
begin
    n := "SALAM!SALAMATI GOGOLO?";
end

function main(): integer begin
    local: array [22] of character;
    init_arr(local);
    print_arr(local);
end
"""

test25 = """
function main(): integer begin
    write(strlen("salam"));
    s: string := "salam";
    n: integer := strlen(s);
    write(n);
end
"""

test26 = """
procedure sort(n: integer; a: array [n] of integer) begin
    i: integer := 0;
    j: integer := 0;

    while j < n do begin
        i := 0;
        while i < n - 1 do begin
            if a[i] > a[i + 1] then begin
                (a[i], a[i + 1]) := (a[i + 1], a[i]);
            end
            i := i + 1;
        end
        j := j + 1;
    end
end

function main(): integer begin
    n: integer := 10;
    a: array [n] of integer;
    a[0] := 10;
    a[1] := -2;
    a[2] := 3;
    a[3] := 5;
    a[4] := -4;
    a[5] := 7;
    a[6] := 6;
    a[7] := 9;
    a[8] := 4;
    a[9] := -10;

    sort(n, a);

    i: integer := 0;
    while i < n do begin
        write(a[i]);
        write("\n");
        i := i + 1;
    end
end
"""

test27 = """
procedure sort(n: integer; a: array [n] of character) begin
    i: integer := 0;
    j: integer := 0;

    while j < n do begin
        i := 0;
        while i < n - 1 do begin
            if a[i] > a[i + 1] then begin
                (a[i], a[i + 1]) := (a[i + 1], a[i]);
            end
            i := i + 1;
        end
        j := j + 1;
    end
end

function main(): integer begin
    s: string := "hello 567 world! 123";
    n: integer := strlen(s);
    a: array [n] of character;
    a := s;
    
    sort(n, a);

    i: integer := 0;
    while i < n do begin
        write(a[i]);
        write("\n");
        i := i + 1;
    end
end
"""

test28 = """
procedure print_matrix(n: integer; m: integer; o: integer; a: array [n, m, o] of integer) begin
    i: integer := 0;
    j: integer := 0;
    k: integer := 0;
    
    while i < n do begin
        j := 0;
        while j < m do begin
            k := 0;
            while k < o do begin
                write(a[i, j, k]);
                write("\t");
                k := k + 1;
            end
            write("\n");
            j := j + 1;
        end
        write("\n--------------------------------------------\n");
        i := i + 1;
    end
end

procedure assign_value(n: integer; m: integer; o: integer; a: array [n, m, o] of integer) begin
    i: integer := 0;
    j: integer := 0;
    k: integer := 0;
    
    while i < n do begin
        j := 0;
        while j < m do begin
            k := 0;
            while k < o do begin
                a[i, j, k] := i + j + k;
                k := k + 1;
            end
            j := j + 1;
        end
        i := i + 1;
    end
end

function main(): integer begin
    n: integer := 2;
    m: integer := 10;
    o: integer := 20;
    a: array [n, m, o] of integer;
    
    assign_value(n, m, o, a);
    print_matrix(n, m, o, a);
    
end
"""

official_test_1 = """
function main() : integer
begin
    write("hello world !") ;
    return 0 ;
end 
"""

official_test_2 = """
function main() : integer
begin
    a : integer := 2 ;
    b : integer := 3 ;
    c : real ; 
    c := b / a; 
    if c <> 1 then
    begin 
        write("not equal ! ") ;
    end 
    
    return 0 ;
end 
"""

official_test_3 = """

procedure print(input : integer)
begin
    write("the number is : ") ;
    write(input) ;
    write("\n") ;
end

function main() : integer
begin
    index : integer := 0 ;

    while index <> 20 do 
    begin
        print(index) ;
        index := index + 1 ;
    end 

    return 0 ;
end 

"""

official_test_4 = """

function product(a : integer ; b : integer) : integer
begin
    result : integer := a * b ;
    return result ;
end

procedure print(input : integer)
begin
    write("the number is : ") ;
    write(input) ;
    write("\n") ;
end


// this is a comment 
<-- hi 
i am a comment -->

function main() : integer
begin
    
    arr : array [10] of integer ;
    index : integer := 0 ;

    while index < 10 do 
    begin
        arr[index] := index;
        arr[index] := product(index, arr[index]) ;
        print(arr[index]) ;
        index := index + 1;
    end 

    

    return 0 ;
end 

"""

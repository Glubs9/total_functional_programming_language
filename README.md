# total_functional_programming_language

# Installation
This is written in python and does not need any external libraries or installations.
To run the program, make sure you have python downloaded and installed. Then download the repo.
To run any code you write, put in python Main.py [file_name].

# Tutorial
[Language Design Doc](https://docs.google.com/document/d/1VaQIqCRbHQcMX1CR2NVf0SVfpH9rvEA5TUewIfpVD3I/edit?usp=sharing) <br>
#### data type
This language uses unary successor arithmetic (akin to mu-recursive functions). 0 is the base case
and every number is defined as the successor of 0. Successor is written s[0].                 

#### basic functions
Entry starts at a main function called main.           
To define a primitive function the name of the function followed by parenthesis and it's arguments
are written, after this an equals sign is written and the function definition is written.  I.e: test(a,b ) = a;
The function definition can be made of a function call or a variable or a literal. With the
arguments to each function being recursively defined (another function call, variable or literal).       
You can also pattern match on function arguments with successor calls, i.e: minusone(s[a]) = a;     
You can also define a function multiple times, where it will call the highest succeeded matching
definition, ala ml. (see definitions in stdlib.tfpl for examples).     

#### non-primitive functions
You can also define non-primitive functions by using curly braces {}. These functions are also
called with curly braces. Non-primitive functions are defined identically to primitive functions except using parentheses () and matches one of the following cases.   (note: this is a reproduction of the normal definition. also note: Oftentimes people allow composition and other functions to be inlined, this is not true in my language)     
1. constant 0 function. A function that returns 0.    
2. successor function. A function that constructs the successor of a natural number. called with square brackets.     
3. projection function. A functino that takes some arguments and returns only one of them. i.e: f(a,b,c) = b; note: this is not defined in stdlib, but can be defined manually.     
4. composition h(x1,...,xm) = f(g1(x1,...,xm),...,gk(x1,...,xm)); (for any functions, that aren't recursive. Where h and g have the same arity and f has k arity)     
5. primitive recursion has exactly two cases     
	a. h(0,x1,...xm) = f(x1,...,xm); (f != h)     
	b. h(s[y],x1,...,xm) = g(y,h(y,x1,...,xm),x1,...,xm); (g != h)    
         
You can call a non-primitive function within a primitive function even though, conceptually, this
would create a non-primitive function. This is worked around by the program splitting into two
branches, one where the non-primitive call immediately returns the bottom value (!) and another
where the non-primtive call executes as normal. If the normal execution branch finishes before the
bottom value branch finishes, the bottom value branch is deleted and as are all branches it created.
In practice this does not come up much with purely unary arithmetic. As more functionality is added
this will become more important. Also note: you cannot pattern match bottom in primitive recursive functions.
![graph not found](not_program.png)

#### examples
If you would like further examples please refer to stdlib.tfpl.     
An example of a main function is in test.tfpl.    

#### STDLIB
this is a list of function within the standard library.    
<ol>
	<li> print(a) (prints and returns whatever is passed to it) </li>
	<li> s[a] (returns the successor of the given argument)</li>
	<li> plus(a, b) (performs addition on a and b)</li>
	<li> multiply(a, b) (performs multiplication on a and b)</li>
	<li> power(a, b) (performs power on a and b, a^b)</li>
	<li> pred(a) (returns the predecessor of the given function, note: pred(0) = 0)</li>
	<li> minus(a, b) (returns a-b note: this uses pred so any answer lower than 0 will be 0)</li>
	<li> ack{a, b} (returns the ackerrman function, this is not too useful but is a good example of a non-primitive function)</li>
</ol>


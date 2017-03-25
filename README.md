# Plankalkul

And implementation of plankalkul for CS Cannon.
This is mostly based on http://www.cs.ru.nl/bachelorscripties/2010/Bram_Bruines___0213837___Plankalkul.pdf, with some
liberties taken, for example I got rid of the 2d notation because of how awful indexing with variables was, now I can nest statements.
I feel justified in this because wikipedia did a similar thing.


## Language Description
The original language didn't really have functions, it was designed to just run the top level program. For ease I allowed this
to be arbitrarily named, so a file starts with `Name(varsIn) => varsOut`.
Then there are statements surrounded by `{}` in place of the 2d original format. Statements can be an `expr -> expr` which is an if statement, `expr => var` which is an assignment,
or a loop, `W1(expr) => var` or `W`, just `W` is a while loop that terminates if the statement following it is not true. `W1` is a for loop that either goes from 0 to expr or over each element in expr depending on the type of expr. A variable is named `V#`, `R#`, or `Z#`, and while these should have different behaviors they're all general. Variables are structured as such: `Name[Array Access:type]`. The Array Access is optional, and type is `i` or `b` with optional `m*n*lowerword*` preceeding it as dimension. Then there are number constants and `#t` and `#f` for booleans.

## Code Apology
So this code, mostly the execution part, is fairly hacked together. It's written in python. The parser is a pretty standard recursive decent parser. Execution follows the object oriented model where each object parsed can be called on some memory and it returns a memory and a value. This was poorly planned so it is not nearly as clean as the parser.

## Analysis of language
The original form of the language (which can be seen in 01/2.planOld) is 2D and really ungainly. A recursive decent parser could be easily adapted for this, but array accessing is rather ugly and hard to do in ascii so I flattened the language. Because of how I implemented it, it is similar to c, but memory is totally abstracted away. It is fundamentally a memory changing language. The biggest noticeable absence is named functions and recursion. Overall it's an interesting language, but there are not many new concepts to be gleaned.

## Writing a program
`runPlan.py sourceFile "[inputs, seperated, by, commas]"`

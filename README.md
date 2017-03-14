# Plankalkul

And implementation of plankalkul for CS Cannon.
This is mostly based on http://www.cs.ru.nl/bachelorscripties/2010/Bram_Bruines___0213837___Plankalkul.pdf, with some
liberties taken, for example I got rid of the 2d notation because of how awful indexing with variables was, now I can nest statements.
I feel justified in this because wikipedia did a similar thing.


## Language Description
The original language didn't really have functions, it was designed to just run the top level program. For ease I allowed this
to be arbitrarily named, so a file starts with `Name(varsIn) => varsOut`. 
TODO

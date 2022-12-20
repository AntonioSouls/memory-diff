# memory-diff

## About The Project
` memory-diff ` is a library that was created with the aim of making the difference between two files containing large data (XLIFF format). This should help cookingbot only download data other than what it already has, in order to make training more efficient.

## How it works
` memory-diff ` create an object ` diff ` that takes three path as parameters (are the paths of the two files to compare and the path of the diff_file in which we save the differences) and, each file, is opened and saved into a list of *<tu> block* in which each element is a *<tu> block* of the tmx file. Scrolling through the two lists that are created, each *<tu> block* is transormed into a *TU object* and, thanks to the equals method, we are able to compare every single *TU object* of the new file with every *TU object* of the old file and, like this, know the differences between the first two files and saving that differences into a third list which will be saved into the third TMX file.
So, the third TMX file, contains only blocks that were modified or added but keeps the XLIFF's intestation


## Autors
This library was created by me (`Antonio Lanza`) thanks also to the kind help of `Samir Salman`
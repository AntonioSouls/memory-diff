# memory-diff

## About The Project
` memory-diff ` is a library that was created with the aim of making the difference between two files containing large data (XLIFF format). This should help cookingbot only download data other than what it already has, in order to make training more efficient.

## How it works
` memory-diff ` create an object ` diff ` that takes three path as parameters (are the paths of the two files to compare and the path of the diff_file in which we save the differences) and, each file, is opened and saved into a list of String in which each element is a line of the file. Scrolling through the two lists that are created,we are able to know the differences between the first two files and saving that differences into a third list which will be saved into the third file


## Autors
This library was created by me (`Antonio Lanza`) thanks also to the kind help of `Samir Salman`
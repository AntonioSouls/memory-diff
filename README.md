# memory-diff

## About The Project
` memory-diff ` is a library that was created with the aim of making the difference between two files containing large data (XLIFF format). This should help cookingbot only download data other than what it already has, in order to make training more efficient.

## How it works
` memory-diff ` create an object ` diff ` that takes two path as parameters (are the paths of the two files to compare) and, each file, is opened and saved into a list of String in which each element is a line of the file. Scrolling through the two lists that are created,we are able to know the difference between two files and upgrade one (the older one) with the content of the other one (the newest one), however without modifing that lines that weren't changed between two files

## Autors
This library was created by me (Antonio Lanza) thanks also to the kind help of Samir Salman
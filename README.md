# Memory-Diff

## About The Project
` memory-diff ` is a library that was created with the aim of making the difference between two datasets:
- A generic dataset
- An updated version of the same dataset
This should help to see if there have been any changes between the old version and the new version of the same dataset and, in our use case, this is convenient to allow Cooking Bot to train only on the changes and not also on data that it has already analyzed

## How it works
` memory-diff ` create an object ` DatasetDiff ` that takes four paths as parameters (are the paths of two datasets to compare, the path of the dataset in which we save the files containing the differences between the two previous datasets and the path of folder in which we save the statistics about the project's executions). ` DatasetDiff ` read all files in the new dataset and, for each file, see if it exists in the old dataset. If it doesn't exist, it means that it is a file containing new data, so it is added to the dataset containing the differences. If, however, it exists, then ` DatasetDiff ` compare this file with the old version of itself using the ` Diff ` class and, if there are any differences, creates a diff file containing the differences between the two parsed files and save this diff file into the dataset containing the differences.
So, following this, we will have a third dataset containing only the differences between the first two and cookingbot can only retrain on new data.
The `Diff`, taken the two files, opens them and saves (in a dictionary associated with the file) all *Tranlation Units* of that file. Each Translation Unit has an id, so in the dictionary we put all the ids associated with the corresponding Translation Unit (If the translation unit doesn't have an id, we hash that unit and use the hash as the id). After that, by comparing the two dictionaries, we can understand with a low computational cost what the differences are


## First Steps
Install the *setup.py* before using it. It contains all the useful libraries
- *Required Python ≥ 3*


## How use this library
Create a Python script to *import DatasetDiff from memory_diff.dataset_diff*. In the script create a method in which to write the path where the new dataset is instantiated, the path where the old dataset is instantiated, the path where you want to save the result of the ` memory-diff ` and, finally, the path where to save the  ` statistics `. At this point, create the *DatasetDiff* object passing it the paths just mentioned as parameters and, subsequently, invoke the *starting_diff_on_dataset()* method of this *DatasetDiff* object


## Autors
[![](https://github.com/AntonioSouls.png?size=50)](https://github.com/AntonioSouls)
[![](https://github.com/samirsalman.png?size=50)](https://github.com/samirsalman)
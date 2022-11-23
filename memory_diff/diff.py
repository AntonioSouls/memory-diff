#Classe Diff che modella un ogetto che permette di fare la differenza tra due file e salvi la differenza su un altro file

from difflib import ndiff


class Diff:
    def __init__(self) -> None:
        pass

    def diff_function(self, file1, file2):
        file_diff = ndiff(file1,file2)

    def saving_diff(self, diff_file):
        pass 
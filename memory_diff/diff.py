from difflib import ndiff

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:
    # CLASS CONSTRUCTOR: the object takes two files as parameters, where the first one we insert is the "new" one, the second one is the "old" one
    # I use the convenction that the new one that's what i have to compare with, so:
    #       - if diff returns ' ' it means that the analyzed line is the same in both files; 
    #       - if diff returns '+' it means that the analyzed line exist only in the right file of the diff (in our example it will be the old one). So, we have to remove that line from the old one;
    #       - if diff returns '-' it means that the analyzed line exist only in the left file of the diff (in our example it will be the new one). So, we have to add that line on the old one;
    #       - if diff returns ('-', '?', '+') it means that the analyzed line had some difference in the middle, so we will thake that line from the new file and save it in the old one
    #         removing the line that was already there
    
    def __init__(self,file_new: str, file_old:str, file_diff:str) -> None: 
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.lista_file_new = None
        self.lista_file_old = None
        self.lista_file_diff = []

    def diff_function(self):                                      # Doing diff and create a list wich tell the differences between two files, but don't create a diff file
        file_object_new = open(self.file_new, 'r')
        file_object_old = open(self.file_old, 'r')
        self.lista_file_new = file_object_new.readlines()
        self.lista_file_old = file_object_old.readlines()
        diff_result = list(ndiff(self.lista_file_new,self.lista_file_old))
        file_object_new.close()
        file_object_old.close()
        return diff_result

    def saving_diff(self):                                         #Fa' la diff invocando la funzione di sopra, e poi sfrutta questa diff per creare un file_diff in cui sono contenute soltanto le modifiche
        diff_result = self.diff_function()
        print(diff_result)

        elem:str = None
        riga = 0
        index_diff_result = 0
        while index_diff_result < len(diff_result):
            stringa = diff_result[index_diff_result]
            stringa_successiva = diff_result[index_diff_result + 1]
            if stringa[0] != ' ':
                if stringa[0] == '+' and stringa_successiva[0] == '-':
                    elem = self.lista_file_new[riga]
                    index_diff_result = index_diff_result + 2
                else:
                    if stringa[0] == '+' and stringa_successiva[0] != '-':
                        elem = ''
                        index_diff_result = index_diff_result +1
                    else:
                        if stringa[0] == '-' and stringa_successiva[0] == '+':
                            elem = self.lista_file_new[riga]
                            index_diff_result = index_diff_result + 2
                        else:
                            if stringa[0] == '-' and stringa_successiva[0] != '+':
                                if stringa_successiva[0] == '-':
                                    elem = self.lista_file_new[riga]
                                    index_diff_result = index_diff_result +1
                                else:
                                    elem = self.lista_file_new[riga]
                                    index_diff_result = index_diff_result + 3
            else:
                elem = ''
                index_diff_result = index_diff_result + 1
            self.lista_file_diff.insert(riga,elem)
            print(self.lista_file_diff)
            riga = riga +1
        file_object_diff = open(self.file_diff,'w')
        file_object_diff.writelines(self.lista_file_diff)
        file_object_diff.close()
        return                                                 
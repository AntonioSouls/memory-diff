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
    
    def __init__(self,file_new: str, file_old:str) -> None: 
        self.file_new = file_new
        self.file_old = file_old
        self.lista_file_new = None
        self.lista_file_old = None

    def diff_function(self):                                      # Fa' semplicemente la diff senza apportare modifiche
        file_object_new = open(self.file_new, 'r')
        file_object_old = open(self.file_old, 'r')
        self.lista_file_new = file_object_new.readlines()
        self.lista_file_old = file_object_old.readlines()
        diff_result = list(ndiff(self.lista_file_new,self.lista_file_old))
        file_object_new.close()
        file_object_old.close()
        return diff_result

    def saving_diff(self):                                         #Fa' la diff invocando la funzione di sopra, e poi sfrutta questa diff per modificare i file
        diff_result = self.diff_function()
        print(diff_result)
        # # for x in diff_result:                                      #controllo riga per riga cosa è cambiato e, in base al controllo che faccio, modifico la lista corrispondente al vecchio file
        # #     if x[0] != ' ':                                             
        # #         if x[0] == '+':
        # #             self.lista_file_old.pop(diff_result.index(x))
        # #         else:
        # #             if x[0] == '-':
        # #                 self.lista_file_old.insert(diff_result.index(x), self.lista_file_new[diff_result.index(x)])
        # #             else:
        # #                 self.lista_file_old.pop(diff_result.index(x))
        # #                 self.lista_file_old.insert(diff_result.index(x), self.lista_file_new[diff_result.index(x)])
        
        # object_file_old = open(self.file_old, 'w')                            #apro il vecchio file per riscriverci dentro la lista modificata
        # object_file_old.writelines(self.lista_file_old)                       #La scrivo
        # object_file_old.close()                                                #chiudo il file e lo restituisco
        # return self.file_old  
        return                                                  
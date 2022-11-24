from difflib import ndiff

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:
    ## ---- DA TRADURRE IN INGLESE QUESTA DESCRIZIONE ----------
    # COSTRUTTORE DELLA CLASSE: stiamo dicendo che l'ogetto prende come parametri due file, dove il primo che inseriamo è quello "Nuovo", il secondo è il "Vecchio"
    # Uso la convenzione che quello nuovo è quello con cui fare il confronto, dunque:
    #       - se la diff mi ritorna ' ' vuol dire che la riga analizzata è uguale nei due file; 
    #       - se ritorna '+' la linea esiste solo nel file che passiamo a destra nella diff (che a noi sarà quello vecchio). Dunque, va rimossa da lì;
    #       - se ritorna '-' la linea esiste solo nel file che passiamo a sinistra nella diff (che a noi sarà quello nuovo). Dunque, va aggiunta nel file di destra (quello vecchio);
    #       - se ritorna ('-', '?', '+') vuol dire che la linea analizzata possiede delle differenze nel mezzo, dunque dovremo prendere quella linea dal file nuovo e salvarla in quello vecchio
    #         rimuovendo quella che già c'era
    
    def __init__(self,file_new: str, file_old:str) -> None: 
        self.file_new = file_new
        self.file_old = file_old
        self.lista_file_new = None
        self.lista_file_old = None

    def diff_function(self):                                      # Fa' semplicemente la diff senza apportare modifiche
        object_file_new = open(self.file_new, 'r')
        object_file_old = open(self.file_old, 'r')
        self.lista_file_new = object_file_new.readlines()
        self.lista_file_old = object_file_old.readlines()
        diff_result = list(ndiff(self.lista_file_new.splitlines(),self.lista_file_old.splitlines()))
        return diff_result

    def saving_diff(self):                                      #Fa' la diff invocando la funzione di sopra, e poi sfrutta questa diff per modificare i file
        diff_result = self.diff_function()
        for x in diff_result:
            if x != ' ':
                if x == '+':
                    print("Fai qualcosa")
                else:
                    if x == '-':
                        print("Fai altro")
                    else:
                        print("Fai altro ancora")
        return None
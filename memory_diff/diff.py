from difflib import ndiff

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:
    # COSTRUTTORE DELLA CLASSE: stiamo dicendo che l'ogetto prende come parametri due file, dove il primo che inseriamo è quello che va a "Destra", il secondo va a "Sinistra"
    # Uso la convenzione che quello di destra è quello con cui fare il confronto, dunque:
    #       - se la diff mi ritorna ' ' vuol dire che la riga analizzata è uguale nei due file; 
    #       - se ritorna '+' la linea esiste solo nel file di destra (cioè è stata aggiunta e la dovremo importare anche in quello di sinistra);
    #       - se ritorna '-' la linea esiste solo nel file di sinistra (cioè è stata rimossa e la dovremo rimuovere dal file di sinistra);
    #       - se ritorna ('-', '?', '+') vuol dire che la linea analizzata possiede delle differenze nel mezzo, dunque dovremo prendere quella linea dal file di destra e salvarla uguale nel file di sinistra
    
    def __init__(self,file1, file2) -> None: 
        self.fileDx = file1
        self.fileSx = file2

    def diff_function(self):
        diff_result = list(ndiff(self.fileSx.splitlines(),self.fileDx.splitlines()))
        return diff_result

    def saving_diff(self):
        pass 
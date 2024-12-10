import numpy as np

class Game :
    def __init__(self):
        self.plateau = Plateau()
        self.player1 = input("Nom Joueur 1 \n")
        self.player2 = input("Nom Joueur 2 \n")
    
       
    def get_plateau(self):
        return self.plateau
        
        

class Plateau:
    def __init__(self, plato=None):
        if plato == None:
            self.plato = np.zeros((15, 15), dtype=int)
        else:
            self.plato = plato

    def __str__(self):
        rep = ""
        for ligne in self.plato:
            rep += str(ligne) + "\n"
        return rep

def main():
    game = Game()
    


if __name__ == "__main__":
    main()


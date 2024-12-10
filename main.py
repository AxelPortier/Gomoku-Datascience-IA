import numpy as np

class Game :
    def __init__(self):
        self.plateau = Plateau()
     
    def get_plateau(self):
        return self.plateau.plateau
    
    def set_plateau(self,pos,val):
        self.plateau.plateau[pos[0],pos[1]] = val
    
        
        

class Plateau:
    def __init__(self, plateau=None):
        if plateau == None:
            self.plateau = np.zeros((15, 15), dtype=int)
        else:
            self.plateau = plateau

    def __str__(self):
        rep = ""
        for ligne in self.plateau:
            rep += str(ligne) + "\n"
        return rep

def main():
    game = Game()
    print(game.get_plateau()[0,0])
    game.set_plateau([0,0],1)
    print(game.get_plateau()[0,0])

    


if __name__ == "__main__":
    main()


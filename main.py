import numpy as np

dico={lettre:digit for lettre,digit in zip("ABCDEFGHIJKLMNO",[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])}
print(dico)

class Game :
    def __init__(self):
        self.plateau = Plateau()
     
    def get_plateau(self):
        return self.plateau.plateau
    
    def set_plateau(self,pos,val):
        self.plateau.plateau[pos[0],pos[1]] = val
        self.player1 = input("Nom Joueur 1 \n")
        self.player2 = input("Nom Joueur 2 \n")


    def get_plateau(self):
        return self.plateau


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



def Result(plato,joueur,position):  # renvoie le nouveau plato modifié
    if plato[position]!=0:
        raise Exception("Position déjà occupée!")
    else:
        new_plato = plato.copy()
        new_plato[position[0],position[1]] = joueur
        return new_plato

def Action(plato):  # retourne liste [(x,y)...] de position possible
    return [(i,j) for i in range(15) for j in range(15) if plato[i,j]==0]




if __name__ == "__main__":
    main()


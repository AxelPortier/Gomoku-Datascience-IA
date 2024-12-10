import numpy as np

class Game :
    def __init__(self):
        self.plateau = Plateau()
        self.init()
    
    def get_plateau(self):
        return self.plateau.plateau
    
    def set_plateau(self,pos,val):
        self.plateau.plateau[pos[0],pos[1]] = val
    
    def init(self):
        print("Bienvenue, vous voilà dans la variante du Gomoku.")
        print("Veuillez choisir quel mode de jeu vous voulez jouer parmi :\n    -Joueur VS Joueur (JJ)\n    -Joueur VS Ordinateur (JO)")
        mode = input("Entrez jj ou jo : \n")
        if (mode.upper() == "JJ"):
            print("\n\nVous avez sélectioner le mode : Joueur VS Joueur")
            print("Veuiller selectioner le Joueur 1")
        elif (mode.upper() == "JO"):
            print("\n\nVous avez sélectioner le mode : Joueur VS Ordinateur")
            print("Veuiller selectioner la priorite de Jeu parmis :\n    -Je commence\n    -Je seconde")
            prio = input()
        else :
            raise Exception("Mode de jeu non existant")
    
    def turn(self):
        pass
    
    def Result(self,joueur,pos):  # renvoie le nouveau plato modifié
        if (self.get_plateau()[pos[0],pos[1]]!=0):
            raise Exception("Position déjà occupée!")
        else:
            new_plato = self.get_plateau().copy()
            new_plato[pos[0],pos[1]] = joueur
            return new_plato


class Plateau:
    def __init__(self, plateau=None):
        self.dico_ligne = {digit:lettre for lettre,digit in zip("ABCDEFGHIJKLMNO",[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])}
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


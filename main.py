import numpy as np

class Game :
    def __init__(self):
        self.plateau = Plateau()
        self.Init()
    
    def Init(self):
        #Menu de Départ
        print("Bienvenue, vous voilà dans la variante du Gomoku.")
        print("Veuillez choisir quel mode de jeu vous voulez jouer parmi :\n    -Joueur VS Joueur (JJ)\n    -Joueur VS Ordinateur (JO)")
        mode = input("Entrez jj ou jo : \n")
        #Joueur VS Joueur
        if (mode.upper() == "JJ"):
            print("\n\nVous avez sélectioner le mode : Joueur VS Joueur")
            print("Veuiller selectioner le Joueur 1")
            self.main_Game()
        #Joueur VS Ordinateur
        elif (mode.upper() == "JO"):
            print("\n\nVous avez sélectioner le mode : Joueur VS Ordinateur")
            print("Veuiller selectioner la priorite de Jeu parmis :\n    -Je commence\n    -Je seconde")
            prio_input = input()
            if(prio_input == "Je commence"):
                self.main_Game()
            elif (prio_input == "Je seconde"):
                self.main_Game(1)
            else :
                raise Exception("Priorite Incorrecte")
        else :
            raise Exception("Mode de jeu non existant")
    
    def main_Game(self,prio=0):
        alternance_Joueur = 1
        while True :
            if (self.Condwin() !=False):
                break
        #self.GameOver(self.Condwin())
            
            
    
    def Turn(self,joueur):
        pass
    
    def Action(self):  # retourne liste [(x,y)...] de position possible
        return [(i,j) for i in range(15) for j in range(15) if self.plateau.get_plateau()[i,j]==0]
    
    def Result(self,joueur,pos):  # renvoie le nouveau plato modifié
        if self.plateau.get_plateau()[pos[0],pos[1]] != 0:
            raise Exception("Position déjà occupée!")
        else:
            self.plateau.set_plateau(pos,joueur)

    def Condwin(self):
        if self.winligne== False:
            return self.winligne
        elif self.wincolo== False:
            return self.wincolo
        elif self.windiag== False:
            return self.windiag

    def winligne(self):
        val = 0 # valeur actuel 
        compt = 0 # compteur de val à la suite
        for elem in self.plateau.get_plateau(): 
            for x in elem:
                if x!=val: # si l'element est differnet du precedent, on echange
                    val==x
                    compt=0 # et on reset le compteur
                if val==x:
                    compt+=1 #+1 si c'est les memes
                if compt ==5:
                    return val # si compteur 5, c'est win


    def wincolo(self):
        val = 0
        compt = 0
        for i in range(15):
            for j in range(15):
                x = self.plateau.get_plateau()[i][j]
                if x!=val:
                    val==x
                    compt=0
                if val==x:
                    compt+=1
                if compt ==5:
                    return val

    def windiag(self):
        return 0

class Plateau:
    def __init__(self, plateau=None):
        self.dico_ligne = {digit:lettre for lettre,digit in zip("ABCDEFGHIJKLMNO",[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])}
        if plateau == None:
            self.plateau = np.zeros((15, 15), dtype=int)
        else:
            self.plateau = plateau

    def get_plateau(self):
        return self.plateau
    
    def set_plateau(self,pos,val):
        self.plateau[pos[0],pos[1]] = val
    
    def __str__(self):  #Affiche dans la console le plateau
        cellule= {0: " ", 1: "X", 2: "O"}
        rep = ""
        for ligne in self.plateau:
            rep += "+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            for cell in ligne:
                rep+=f"| {cellule[cell]} "
            rep += "|\n"
        rep += "+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n"
        return rep
      
def main():
    game = Game()

if __name__ == "__main__":
    main()

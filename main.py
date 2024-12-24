import numpy as np
from scipy.signal import convolve2d
import os

class Game :
    def __init__(self):
        #Plateau de notre Jeu
        self.plateau = Plateau()
        
        # Nombre de symbole alligné pour la victoire
        self.longueur_victoire = 5
        
        # Création des masques pour les directions horizontale, verticale et diagonales
        mask_horizontal = np.ones((1, self.longueur_victoire), dtype=int)
        mask_vertical = np.ones((self.longueur_victoire, 1), dtype=int)
        mask_diagonale_descendante = np.eye(self.longueur_victoire, dtype=int)
        mask_diagonale_montante = np.fliplr(mask_diagonale_descendante)
        
        #Liste comprenant tout nos masque
        self.masks = [mask_horizontal, mask_vertical, mask_diagonale_descendante, mask_diagonale_montante]
        
        self.dico_ligne = {digit:lettre for lettre,digit in zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"ABCDEFGHIJKLMNO")}

        
        self.Init_Game()
        
    def Init_Game(self):
        
        #Clear console
        os.system('cls')
        
        print("Bienvenue, vous voilà dans une variante du Gomoku :\n")
        
        # Var pour quitter le jeu
        quitting = False
        while not quitting:  # Boucle jusqu'à une entrée valide du mode de jeu
            
            print("Veuillez sélectionner le mode de jeu :\n    -Joueur VS Joueur (jj)\n    -Joueur VS Ordinateur (jo)")
            
            #Input de notre utilisateur pour le mode
            mode_input = input("Entrez jj ou jo (quit pour arrêter le jeu) : \n").lower()
            
            if mode_input == "jj":
                self.mode = 1
                break
            elif mode_input == "jo":
                self.mode = 2
                while not quitting : # Boucle jusqu'à une entrée valide de la priorite de jeu
                    
                    print("\nVeuillez sélectionner la priorité de jeu :\n    -Je commence (j1)\n    -Je seconde (j2)")
                    
                    #Input de notre utilisateur pour la prio
                    prio = input("Entrez j1 ou j2 : \n").lower()
                    
                    if prio == "j1":
                        self.is_playing = 1
                        break
                    elif prio == "j2":
                        self.is_playing = 2
                        break
                    elif prio == "quit":
                        quitting = True
                        break
                    else:
                        #os.system('cls')
                        print("Mode de jeu non existant. Veuillez réessayer.\n")
                break
            
            elif mode_input =="quit" or quitting:
                break
            else:
                #os.system('cls')
                print("Mode de jeu non existant. Veuillez réessayer.\n")
        self.Play()
    
    def Play(self):  
        nb_turn = 1
        joueur = 1
        if (self.mode == 2 and self.is_playing == 2) :  # premier coup de l'ia forcément au milieu
            self.plateau.set_position((7,7),self.is_playing)
        while self.check_winner() == 0 :
            self.Turn(joueur,nb_turn)
            joueur += 1
            if (joueur>2) : joueur -= 2
            nb_turn += 1
            #if(nb_turn>100) : break #Enlever quand on peut jouer les joueurs
        
        self.GameOver(joueur)
    
    def result(self,board, joueur, position): # retourne board modifié à la case position par 1 ou 2 SANS MODIF self.plateau !!!!
        if board[position] != 0:
            raise Exception("Position déjà occupée!")
        new_board=board.copy()
        new_board[position[0],position[1]] = joueur
        return new_board
    
    def actions(self,board): # liste des positions non disponibles
        return [(i,j) for i in range(15) for j in range(15) if board[i,j]==0]
    
    def minimax(self,board, joueur):
        if joueur == 1:  # Joueur maximisant 
            best_value = float('-inf')
            best_action = None
            for action in self.actions(board):
                new_board = self.result(board,joueur,action)
                value = self.min_value(new_board, 2)  # L'adversaire joue ensuite
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_action
        else:  # Joueur minimisant 
            best_value = float('inf')
            best_action = None
            for action in self.actions(board):
                new_board = self.result(board, joueur, action)
                value = self.max_value(new_board, 1)  # L'adversaire joue ensuite
                if value < best_value:
                    best_value = value
                    best_action = action
            return best_action
    
    def max_value(self,board, joueur):
        if self.check_winner()!=0 :
            return self.check_winner()    
        v = float('-inf')
        for action in self.actions(board):
            new_board = self.result(board, joueur, action)
            v = max(v, self.min_value(new_board, 3 - joueur))
        return v
    
    
    def min_value(self,board,joueur):
        if self.check_winner()!=0 :
            return self.check_winner()        
        v = float('inf')
        for action in self.actions(board):
            new_board = self.result(board,joueur, action)
            v = min(v, self.max_value(new_board, 3 - joueur))
        return v

    def Turn(self,joueur,nb_Turn):
        dic={2:"à l'IA",1:"au joueur"}
        #JJ
        if (self.mode == 1):
            #os.system('cls')
            print("Tour : ",nb_Turn,"\n",self.plateau,"\nC'est au Joueur ",joueur," de jouer")
            actions_possible = [(i,j) for i in range(15) for j in range(15) if self.plateau.get_plateau()[i,j]==0]
            while True :
                ligne,colonne = str(input("\nrentrer la ligne (A B C D E F G H I J K L M N O P) : ")).upper(),int(input("rentrer la colonne ( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15) : "))
                ligne = self.dico_ligne[ligne]
                if (ligne,colonne) in actions_possible:
                    self.plateau.set_position([ligne,colonne-1],joueur)
                    break
                else :
                    #os.system('cls')
                    print("Position déjà occupé ou inexistante")
                    
        #JO
        else :
            print("Tour : ",nb_Turn,"\n",self.plateau,"\nC'est",dic[joueur],"de jouer")
            if (joueur==2):    # Si c'est le tour de l'IA
                self.plateau.set_position(self.minimax(self.plateau.get_plateau(),joueur),joueur)
            else :  # Si c'est le tour du joueur                
                actions_possible = [(i,j) for i in range(15) for j in range(15) if self.plateau.get_plateau()[i,j]==0]
                while True :
                    ligne,colonne = str(input("\nrentrer la ligne (A B C D E F G H I J K L M N O P) : ")).upper(),int(input("rentrer la colonne (1 2 3 4 5 6 7 8 9 10 11 12 13 14 15) : "))
                    if ligne not in "ABCDEFGHIJKLMNOP":
                        print("Position inexistante. Réessayez")
                    else:
                        ligne = self.dico_ligne[ligne]
                        if (ligne,colonne) in actions_possible:
                            self.plateau.set_position([ligne,colonne-1],joueur)
                            break
                        else :
                            print("Position déjà occupé. Réessayez")
            #os.system('cls')

    def GameOver(self,joueur):
        print("Game over")
    
    def check_winner(self):
        # Convolutions pour détecter les alignements
        for mask in self.masks:
            conv_result = convolve2d(self.plateau.get_plateau(), mask, mode="valid")
            # Vérification pour le joueur 1 (réel) et joueur 2 (imaginaire)
            if np.any(np.real(conv_result) == self.longueur_victoire):
                return 1  # Joueur 1 gagne
            if np.any(np.imag(conv_result) == self.longueur_victoire):
                return 2  # Joueur 2 gagne
        return 0 # Aucun gagnant

class Plateau:

    def __init__(self, plateau=None):                
        if plateau == None:
            self.plateau = np.zeros((15,15),dtype=complex)
            self.plateau[self.plateau == 2] = 1j
        else:
            self.plateau = plateau

    def get_plateau(self):
        return self.plateau
    
    def set_position(self,pos,val):
        if (val == 2) : 
            val = 1j
        self.plateau[pos[0],pos[1]] = val  

    def __str__(self):  # Affiche dans la console le plateau
        cellule = {0: " ", 1: "X", 1j: "O"}
        rep = "    "  # Espacement initial pour aligner les chiffres avec les colonnes
        
        # Ajout des indices des colonnes, alignés avec les cases
        for i in range(len(self.plateau[0])):
            rep += f" {i+1:<3}"  # Chaque indice occupe 3 caractères pour s'aligner
        
        rep += "\n"  # Retour à la ligne pour le début du plateau
        # Construction du tableau
        i = 0
        string="ABCDEFGHIJKLMNO"
        for ligne in self.plateau:
            # Ligne de séparation entre les cases
            rep += "    +" + "---+" * len(ligne) + "\n"
            # Contenu de la ligne
            rep += f"{string[i]}   "  # Ajout de l'indice de la ligne
            for cell in ligne:
                rep += f"| {cellule[cell]} "  # Ajout du contenu de chaque case
            rep += "|\n"
            i += 1
    
        # Dernière ligne de séparation
        rep += "    +" + "---+" * len(self.plateau[0]) + "\n"
        return rep 

def main():
    game = Game()

if __name__ == "__main__":
    main()


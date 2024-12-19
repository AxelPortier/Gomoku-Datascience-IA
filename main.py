
import timeit
import numpy as np
from scipy.signal import convolve2d

class Game :
    def __init__(self):
        self.plateau = Plateau()
        self.Init()
    
    def Init(self):
        print("Bienvenue, vous voilà dans la variante du Gomoku.")
        print("Veuillez choisir quel mode de jeu vous voulez jouer parmi :\n    -Joueur VS Joueur (JJ)\n    -Joueur VS Ordinateur (JO)")
        mode = input("Entrez jj ou jo : \n")
        if (mode.upper() == "JJ"):
            print("\n\nVous avez sélectioner le mode : Joueur VS Joueur")
            print("Veuiller selectioner le Joueur 1")
        elif (mode.upper() == "JO"):
            print("\n\nVous avez sélectioner le mode : Joueur VS Ordinateur")
            print("Veuiller selectioner la priorite de Jeu parmis :\n    -Je commence\n    -Je seconde")
            prio = input("Entrez j1 ou j2 : \n")
        else :
            raise Exception("Mode de jeu non existant")
    
    def Turn(self):
        return 
    
    def Action(self):  # retourne liste [(x,y)...] de position possible
        return [(i,j) for i in range(15) for j in range(15) if self.plateau.get_plateau()[i,j]==0]
    
    def Result(self,joueur,pos):  # renvoie le nouveau plato modifié
        if self.plateau.get_plateau()[pos[0],pos[1]] != 0:
            raise Exception("Position déjà occupée!")
        else:
            self.plateau.set_plateau(pos,joueur)

    def play(self):  
        print(self.plateau)
        is_playing=1
        while check_winner(self.plateau)==0:
            if is_playing==1:
                while True:
                    try:
                        l,c=int(input("\nrentrer la ligne (A B C D E F G H I J K L M N O P) : ")),int(input("rentrer la colonne (0 1 2 3 4 5 6 7 8 9 10 11 12 13 14) : "))
                        if (l,c) in self.Action(self.plateau):
                            board = Result(self.plateau, is_playing, (l, c))
                            break                    
                    except Exception as e:
                        print(f"\nErreur : {e}. \nVeuillez réessayer.\n")
                print(self.plateau)
                print(f"Vous avez joué : {(l,c)}\n")
                if check_winner(board)!=0:
                    break
                is_playing=2
            else:
                position_ordi=MiniMax(self.plateau,is_playing)
                board=Result(self.plateau,is_playing,position_ordi)
                print(f"Joueur 2 (Ordinateur) joue : {position_ordi}")
                is_playing=1
                print(self.plateau)
        winner = check_winner(self.plateau)
        if winner == 0:
            print("Match nul !")
        else:
            print(f"Le joueur {winner} a gagné !")
        return 


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


    def __str__(self):  # Affiche dans la console le plateau
        cellule = {0: " ", 1: "X", 2: "O"}
        rep = "    "  # Espacement initial pour aligner les chiffres avec les colonnes
        
        # Ajout des indices des colonnes, alignés avec les cases
        for i in range(len(self.plateau[0])):
            rep += f" {i:<3}"  # Chaque indice occupe 3 caractères pour s'aligner
        
        rep += "\n"  # Retour à la ligne pour le début du plateau
        # Construction du tableau
        i = 0
        for ligne in self.plateau:
            # Ligne de séparation entre les cases
            rep += "    +" + "---+" * len(ligne) + "\n"
            # Contenu de la ligne
            rep += f"{self.dico_ligne[i]}   "  # Ajout de l'indice de la ligne
            for cell in ligne:
                rep += f"| {cellule[cell]} "  # Ajout du contenu de chaque case
            rep += "|\n"
            i += 1
    
        # Dernière ligne de séparation
        rep += "    +" + "---+" * len(self.plateau[0]) + "\n"
        return rep 
    
         
def main():
    game = Game()

def MiniMax():
    pass

def Result(plato,joueur,position):  # renvoie le nouveau plato modifié
    if plato[position]!=0:
        raise Exception("Position déjà occupée!")
    else:
        new_plato = plato.copy()
        new_plato[position[0],position[1]] = joueur
        return new_plato

def Action(plato):  # retourne liste [(x,y)...] de position possible
    return [(i,j) for i in range(15) for j in range(15) if plato[i,j]==0]


m = 5  # Longueur de la victoire
n = 15

repeats = 500
grids = 100

# Création des masques pour les directions horizontale, verticale et diagonales
mask_h = np.ones((1, m), dtype=int)  # Horizontal
mask_v = np.ones((m, 1), dtype=int)  # Vertical
mask_d1 = np.eye(m, dtype=int)       # Diagonale descendante
mask_d2 = np.fliplr(mask_d1)         # Diagonale montante

masks = [mask_h, mask_v, mask_d1, mask_d2]

def check_winner(grid):
    
    def check_line(start_x, start_y, dx, dy):
        """Vérifie si une ligne de longueur m existe à partir d'une position donnée (start_x, start_y) dans une direction donnée (dx, dy)."""
        player = grid[start_x,start_y]
        if player == 0:
            return False  # Aucun joueur ici
        
        count = 0
        x, y = start_x, start_y
        
        while 0 <= x < n and 0 <= y < n and grid[x,y] == player:
            count += 1
            if count == m:
                return player
            x += dx
            y += dy
        
        return False
    
    # Parcours de chaque case de la grille
    for i in range(n):
        for j in range(n):
            if grid[i,j] != 0:  # Vérifie uniquement les cases non vides
                # Vérifie dans les directions : droite, bas, diagonale descendante, diagonale montante
                if (check_line(i, j, 0, 1) or  # Horizontal (droite)
                    check_line(i, j, 1, 0) or  # Vertical (bas)
                    check_line(i, j, 1, 1) or  # Diagonale descendante
                    check_line(i, j, -1, 1)):  # Diagonale montante
                    return grid[i,j]  # Retourne le joueur gagnant (1 ou 2)
    
    return 0  # Aucun gagnant



def check_winner_matrix(grid):
    for player in [1, 2]:
        player_grid = (grid == player).astype(int)

        # Convolutions pour détecter les alignements
        if (np.max(convolve2d(player_grid, mask_h, mode="valid")) == m or
            np.max(convolve2d(player_grid, mask_v, mode="valid")) == m or
            np.max(convolve2d(player_grid, mask_d1, mode="valid")) == m or
            np.max(convolve2d(player_grid, mask_d2, mode="valid")) == m):
            return player  # Retourne le gagnant

    return 0  # Aucun gagnant

def check_winner_complex(grid):
    #grid = convert_grid_complex(grid)

    # Convolutions pour détecter les alignements
    for mask in masks:
        conv_result = convolve2d(grid, mask, mode="valid")
        # Vérification pour le joueur 1 (réel) et joueur 2 (imaginaire)
        if np.any(np.real(conv_result) == m):
            return 1  # Joueur 1 gagne
        if np.any(np.imag(conv_result) == m):
            return 2  # Joueur 2 gagne

    return 0  # Aucun gagnant

def convert_grid_complex(grid):
    gridc = np.array(grid, dtype=complex)
    gridc[gridc == 2] = 1j
    return gridc

def test_round():
    grid = np.random.choice([0,0, 1, 2], size=(n, n))
    gridc = convert_grid_complex(grid)

    # Vérif resultat
    expected = check_winner(grid)
    result_matrix = check_winner_matrix(grid)
    result_complex = check_winner_complex(gridc)
    if result_matrix != expected | result_complex != expected:
        print(f"error {expected} / {result_matrix} / {result_complex}")
        print(grid)

    # chronometrage de repeats execution
    return [
        timeit.timeit(lambda:check_winner(grid), number=repeats),
        timeit.timeit(lambda:check_winner_matrix(grid), number=repeats),
        timeit.timeit(lambda:check_winner_complex(gridc), number=repeats)
    ]


result = np.zeros(3)
for _ in range(grids):
    result += test_round()
 #Programme de test
print(f"Standard {result[0]:.6f}s")
print(f"Matrix {result[1]:.6f}s")
print(f"Complexe {result[2]:.6f}s")



            
        





if __name__ == "__main__":
    main()


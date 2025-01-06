import numpy as np
from scipy.signal import convolve2d
import time

class Game :
    #Initialisation de la class
    def __init__(self):
        #Constantes du jeu
        self.taille_plateau = 15
        self.longueur_victoire = 5
        self.centre = (self.taille_plateau // 2, self.taille_plateau // 2)

        #Modes de jeu
        self.mode_jj  = 1
        self.mode_jo  = 2
        
        #Identifiants des joueurs
        self.joueur_1 = 1
        self.joueur_2 = 2
        
        #Initialisation du plateau
        self.plateau = Plateau(self.taille_plateau)
        
        #Création des masques pour la détection de victoire
        masque_horizontal = np.ones((1, self.longueur_victoire))
        masque_vertical = np.ones((self.longueur_victoire, 1))
        masque_diagonal = np.eye(self.longueur_victoire)
        masque_antidiagonal = np.fliplr(masque_diagonal)
        self.masques = [masque_horizontal, masque_vertical, masque_diagonal, masque_antidiagonal]
        
        #Démarrage du jeu
        self.Init_Game()
        
    #Initialise et démarre une nouvelle partie
    def Init_Game(self):
        print("Bienvenue dans le jeu de Gomoku !\n")
        
        while True:
            print("Veuillez sélectionner le mode de jeu :")
            print("    -Joueur VS Joueur (jj)")
            print("    -Joueur VS Ordinateur (jo)")
            
            mode_input = input("Entrez jj ou jo (quit pour arrêter le jeu) : \n").lower()
            
            if mode_input == "quit":
                return
                
            if mode_input == "jj":
                self.mode = self.mode_jj
                break
                
            if mode_input == "jo":
                self.mode = self.mode_jo
                while True:
                    print("\nVeuillez sélectionner la priorité de jeu :")
                    print("    -Je commence (j1)")
                    print("    -Je seconde (j2)")
                    
                    prio_temp = input("Entrez j1 ou j2 : \n").lower()
                    
                    if prio_temp == "j1":
                        prio = self.joueur_1
                        break
                    elif prio_temp == "j2":
                        prio = self.joueur_2
                        break
                    elif prio_temp == "quit":
                        return
                        
                    print("Choix non valide. Veuillez réessayer.\n")
                self.who_is_playing = prio
                break
                
            print("Mode de jeu non existant. Veuillez réessayer.\n")
        self.Play()
    
    #Gestion de la partie en cours
    def Play(self):
        nb_turn = 1
        joueur = 2 if self.mode == self.mode_jo and self.who_is_playing == self.joueur_2 else 1
        taille_plateau_total = self.taille_plateau * self.taille_plateau

        
        while nb_turn <= taille_plateau_total:
            #Vérification victoire avant le tour
            if self.check_winner():
                break
                
            #Tour du joueur actuel
            self.Turn(joueur, nb_turn)
            
            #Update des variables
            joueur = 3 - joueur  #Alternance 1-2
            nb_turn += 1
        
        winner = self.check_winner()
        self.GameOver(winner)
   
    #Gère la fin de la partie
    def GameOver(self, winner):
        print(self.plateau)
        if winner == 0:
            print("Match nul !")
        else:
            print(f"Le joueur {winner} a gagné !")
   
    #Check les conditions de victoire
    def check_winner(self):
        # Convolutions pour détecter les alignements
        for mask in self.masques:
            conv_result = convolve2d(self.plateau.get_plateau(), mask, mode="valid")
            # Vérification pour le joueur 1 (réel) et joueur 2 (imaginaire)
            if np.any(np.real(conv_result) == self.longueur_victoire):
                return 1  # Joueur 1 gagne
            if np.any(np.imag(conv_result) == self.longueur_victoire):
                return 2  # Joueur 2 gagne
        return 0 # Aucun gagnant
    
    #Gestion d'un tour de jeu
    def Turn(self, joueur, nb_Turn):
        action_messages = {
            (self.mode_jj, 1): "C'est au Joueur 1 de jouer",
            (self.mode_jj, 2): "C'est au Joueur 2 de jouer",
            (self.mode_jo, 1): "C'est à vous de jouer",
            (self.mode_jo, 2): "C'est à l'IA de jouer"
        }
        
        print(f"Tour : {nb_Turn-1}")
        print(self.plateau)
        print(action_messages[(self.mode, joueur)])
        
        if joueur == 2 and self.mode == self.mode_jo:
            position = self.minimax(self.plateau.get_plateau(), joueur, nb_Turn)
        else:
            position = self.get_player_move(nb_Turn)
            
        self.plateau.set_position(position, joueur)
    
    # Récupère et valide le coup du joueur
    def get_player_move(self, nb_Turn):
        actions_possibles = self.actions(self.plateau.get_plateau(), nb_Turn)
        if nb_Turn == 1:
            print(f"Vous ne pouvez jouer qu'au centre : {((self.taille_plateau // 2) + 1, (self.taille_plateau // 2) + 1)}")
            return self.centre
        elif nb_Turn == 3:
            print("Vous pouvez jouer dans les cases situées en dehors du carré central 7x7, \nc'est-à-dire sur les lignes et colonnes avant la ligne E ou après la ligne J, \nainsi que sur les colonnes avant la colonne 5 ou après la colonne 10.")
        
        while True:
            try:
                ligne_input = input("Entrer la ligne (A à O) : ").upper()
                if len(ligne_input)!=1 or ligne_input < 'A' or ligne_input > 'O':
                    raise ValueError("Ligne invalide. Veuillez entrer une lettre entre A et O.")
                
                colonne_input = input("Entrer la colonne (1 à 15) : ")
                colonne = int(colonne_input) - 1
                
                ligne = ord(ligne_input) - ord('A')
                
                if (ligne, colonne) not in actions_possibles:
                    raise ValueError("Position invalide ou déjà occupée. Réessayez.")
                    
                return (ligne, colonne)
                
            except (ValueError, IndexError):
                print("Position invalide ou déjà occupée. Réessayez.")
    
    # Fonction qui retourne un board modifié à la case position par 1 ou 1j SANS MODIF self.plateau !!!!
    def result(self,board, joueur, position):
        new_board = board.copy()
        val = 1j if joueur == 2 else joueur
        new_board[position[0], position[1]] = val
        return new_board
    
    # Fonction qui retourne les actions possibles changer -3 par 3 quand on joue en 15*15
    def actions(self,board,nb_Turn ):
        actions_possibles=[(i,j) for i in range(self.taille_plateau) for j in range(self.taille_plateau) if board[i,j]==0.+0.j]
        if nb_Turn==1:
            actions_possibles=[self.centre]
        elif nb_Turn==3:
            actions_possibles=[(i,j) for i in range(4,11) for j in range(4,11)]
            actions_possibles=[(i, j) for i in range(15) for j in range(15) if (i, j) not in actions_possibles and board[i,j]==0]
        return  actions_possibles
    
      
    #Retourne le meilleur coup selon l'algorithme minimax avec élagage
    def minimax(self, board, joueur, nb_Turn, depth=15):
        start_time = time.time()
        alpha = float('-inf')
        beta = float('inf')
        
        #Récupère et ordonne les coups
        moves = self.order_moves(board, self.actions(board,nb_Turn), joueur)
        best_move = moves[0]
        
        try:
            for move in moves:
                #Vérifie le temps
                if time.time() - start_time > 4.5:
                    return best_move
                    
                new_board = self.result(board, joueur, move)
                value = self.min_value(new_board, 3-joueur, nb_Turn, depth-1, alpha, beta, start_time)
                
                if value > alpha:
                    alpha = value
                    best_move = move
                    
        except TimeoutError:
            return best_move
            
        return best_move
    
    def max_value(self, board, joueur, nb_Turn, depth, alpha, beta, start_time):
        if time.time() - start_time > 4.5:
            return self.evaluate_board(board, joueur)
            
        if depth == 0 or self.check_winner():
            return self.evaluate_board(board, joueur)
            
        v = float('-inf')
        moves = self.actions(board, nb_Turn)
        
        for move in self.order_moves(board, moves, joueur):
            new_board = self.result(board, joueur, move)
            v = max(v, self.min_value(new_board, 3-joueur, nb_Turn, depth-1, alpha, beta, start_time))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, board, joueur, nb_Turn, depth, alpha, beta, start_time):
        if time.time() - start_time > 4.5:
            return self.evaluate_board(board, joueur)
            
        if depth == 0 or self.check_winner():
            return self.evaluate_board(board, joueur)
            
        v = float('inf')
        moves = self.actions(board, nb_Turn)
        
        for move in self.order_moves(board, moves, joueur):
            new_board = self.result(board, joueur, move)
            v = min(v, self.max_value(new_board, 3-joueur, nb_Turn, depth-1, alpha, beta, start_time))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    #Ordonne les coups selon leur score
    def order_moves(self, board, moves, joueur):
        move_scores = []
        for move in moves:
            new_board = self.result(board, joueur, move)
            score = self.evaluate_board(new_board, joueur)
            move_scores.append((move, score))
        return [m for m, s in sorted(move_scores, key=lambda x: x[1], reverse=True)]
    
    #Évalue le plateau pour un joueur donné
    def evaluate_board(self, board, joueur):
        score = 0
        
        #Détection des patterns avec poids optimisés
        for mask in self.masques:
            conv_result = convolve2d(board, mask, mode="valid")
            my_align = np.real(conv_result) if joueur == 1 else np.imag(conv_result)
            opp_align = np.imag(conv_result) if joueur == 1 else np.real(conv_result)
            
            #Attaque
            score += np.sum(my_align == 4) * 1000   #Quatre alignés 
            score += np.sum(my_align == 3) * 100    #Trois alignés ouverts
            score += np.sum(my_align == 2) * 10     #Deux alignés
            
            #Défense (plus prioritaire)
            score -= np.sum(opp_align == 2) * 50  #Bloquer quatre
            score -= np.sum(opp_align == 3) * 2000   #Bloquer trois ouvert
        
        return score



class Plateau:

    def __init__(self, taille=15):                
        self.plateau = np.zeros((taille, taille), dtype=complex)

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


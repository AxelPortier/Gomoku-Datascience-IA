import numpy as np


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


class Pos(Plateau):
    def __init__(self, x, y, plato=None):
        Plateau.__init__(self, plato)
        if self.plato[x,y] == 0:
            self.x = x
            self.y = y
        else:
            print("Erreur de coordonnées")

    def __str__(self):
        return f"x = {self.x} et  y = {self.y}"


def let(joueur):
    if joueur == 0:
        return 'X'
    elif joueur == 1:
        return 'O'
    else:
        return 'Joueur invalide'


def coup(pos, joueur):
    pos.plato[pos.x,pos.y] = let(joueur)
    return pos.plato


def gagne(plato):
    x = True

    return x

plat=Plateau()
pos1=Pos(1,1)
print(pos1)

print("jerrican de caca")
print("En s'en fout")

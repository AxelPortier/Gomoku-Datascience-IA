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

plat=Plateau()
print(plat)


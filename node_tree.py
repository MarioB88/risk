from math import sqrt, log
import random as r

class Node_Tree:
    def __init__(self, accion = None, parent = None):
        self.accion = accion
        self.parent = parent
        self.nvisited = 0
        self.reward = 0
        self.children = {}
        self.ucb = 0                                # formula = recompensa_media + 2* raiz_cuadrada(ln(numero de simulaciones totales)/(numero de veces que se ha visitado el nodo))

    def calculo_ucb(self, simulaciones):
        reward_medio = self.reward / self.nvisited                  
        if self.nvisited==0:
            return 0
        else:
            return reward_medio + 2* sqrt(log(simulaciones) / self.nvisited)

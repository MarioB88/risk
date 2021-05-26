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
                     
        if self.nvisited==0:
            self.ucb = float('inf')
        else:  
            self.ucb = self.reward + 2* sqrt(log(simulaciones) / self.nvisited)      
        return self.ucb

    def __str__(self):
        if self.accion is None:
            cadena = "Nodo con la accion None. Veces visitado " + str(self.nvisited) + " y valor de ucb de " + str(self.ucb)
        else:
            id_n_ataque, id_objetivo = self.accion
            cadena = "Nodo con la accion " + str(id_n_ataque) + " " + str(id_objetivo) + ". Veces visitado " + str(self.nvisited) + ", puntuacion de " + str(self.reward) +" y valor de ucb de " + str(self.ucb)
        return cadena
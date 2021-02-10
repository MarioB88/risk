import random as r
import time
import copy
from math import sqrt, log
from node_tree import Node_Tree
#from player import Player

class McstAgent:
    def __init__(self, state, player):
        self.root = Node_Tree()
        self.root_state = copy.deepcopy(state)
        self.tiempo_busqueda = 0
        self.rollouts = 0
        self.player = player

    def expand(self, parent, state):
        
        if state.winner()[0] == True:
            return False
        
        for n_ataque, objetivos in list(state.acciones_posibles().items()):

            for o in objetivos:
                node = Node_Tree((n_ataque, o), parent)
                parent.children.setdefault((n_ataque,o), node)

        return True
    
    def select_node(self):
        node = self.root
        state = copy.deepcopy(self.root_state)
        while len(node.children) != 0 :
            children = node.children.values()
            ucbs = [c.ucb for c in children]
            maximo = max(ucbs)
            nodo_maximo = [c for c in children if c.ucb == maximo]
            node = r.choice(nodo_maximo)
            print("Realizo una accion para pasar al siguiente hijo")
            state.jugada(node.accion)

            if node.nvisited == 0:
                return node, state
        
        if self.expand(node, state):                                        # Devuelve True si se puede expandir y False si no
            node = r.choice(list(node.children.values()))
            print("Realizo una accion para escoger uno de los hijos")
            state.jugada(node.accion)
        return node, state

    def busqueda(self, limite_tiempo):

        inicio = time.perf_counter()
        n_rollout = 0

        while (time.perf_counter() - inicio) < limite_tiempo:
            print("NUEVO ROLLOUT")
            node, state = self.select_node()
            winner = self.roll_out(state)
            self.backup(node, winner)
            n_rollout += 1
        
        self.tiempo_busqueda = time.perf_counter() - inicio
        print("\nTiempo de busqueda: " + str(self.tiempo_busqueda))
        self.rollouts = n_rollout
        print("Numero de rollouts" + str(self.rollouts))

    def roll_out(self, state):

        acciones=[]

        while state.winner()[0] == False:
            print("Turno es de: " + str(state.turn))
            for n_ataque, objetivos in list(state.acciones_posibles().items()):
                for o in objetivos:
                    acciones.append((n_ataque, o))
            if len(acciones) == 0:
                accion = None
            else:
                accion = r.choice(acciones)
            state.jugada(accion)
            acciones = []
        return state.winner()

    def backup(self, node, winner):
        
        puntuacion = 0

        if self.player._num == winner[1]._num:
            puntuacion = 1
        else:
            puntuacion = -1

        while node is not None:
            node.nvisited += 1
            node.reward += puntuacion
            node = node.parent

    def mejor_jugada(self):                                                         # Escoge el nodo que mas puntuacion tiene, o lo que es lo mismo, el que mas se ha simulado
        max_N = max(self.root.children.values(), key = lambda n: n.nvisited).nvisited
        max_repetidos = [n for n in self.root.children.values() if n.nvisited == max_N]
        nodo_elegido = r.choice(max_repetidos)
        return nodo_elegido.accion

# en el estado se crea un riskmap que ese es el estado inicial. A partir de ahi se va desarrollando.
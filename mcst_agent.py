import random as r
import time
import copy
import sys
from math import sqrt, log
from node_tree import Node_Tree
from operator import itemgetter
#from player import Player

umbral = 0.20

class McstAgent:
    def __init__(self, state, player):
        self.root = Node_Tree()
        self.root_state = copy.deepcopy(state)
        self.tiempo_busqueda = 0
        self.rollouts = 0
        self.player = copy.deepcopy(player)

    def expand(self, parent, state):
        
        if state.winner()[0] == True:
            return False
        
        for n_ataque, objetivos in list(state.acciones_posibles().items()):

            for o in objetivos:
                node = Node_Tree((n_ataque._idN, o._idN), parent)
                parent.children.setdefault((n_ataque._idN,o._idN), node)
        
        node = Node_Tree((0,0), parent)
        parent.children.setdefault((0,0), node)

        return True
    
    def select_node(self):
        
        global umbral
        node = self.root
        state = copy.deepcopy(self.root_state)
        while len(node.children) != 0 :
            children = node.children.values()
            list_children = list(children)
            ucbs = [(c.ucb, c.nvisited) for c in children]
            minimo_visitado = min(ucbs, key=itemgetter(1))[1]
            if minimo_visitado == 0:
                no_visitados = [c for c in children if c.nvisited == minimo_visitado]
                node = r.choice(no_visitados)
                while True:
                    try:
                        state.jugada(node.accion)
                        break
                    except KeyError:
                        node = r.choice(no_visitados)
                        continue
                return node, state
            else:
                if r.random() < umbral:
                    node = r.choice(list_children)
                    while True:
                        try:
                            state.jugada(node.accion)
                            break
                        except KeyError:
                            node = r.choice(list_children)
                            continue
                    return node, state
                maximo = max(ucbs, key=itemgetter(0))[0]
                nodo_maximo = [c for c in children if c.ucb == maximo]
                node = r.choice(nodo_maximo)
                while True:
                    try:
                        state.jugada(node.accion)
                        break
                    except KeyError:
                        node = r.choice(list_children)
                        continue
        
        if self.expand(node, state):                                        # Devuelve True si se puede expandir y False si no
            node = r.choice(list(node.children.values()))
            while True:
                try:
                    state.jugada(node.accion)
                    break
                except KeyError:
                    list(node.children.values()).remove(node)
                    node = r.choice(list(node.children.values()))
                    continue
        return node, state

    def tipo_busqueda(self, limite_tiempo = 0, max_rollouts = 0):

        if limite_tiempo != 0:
            self.busqueda_tiempo(limite_tiempo)
        elif max_rollouts != 0:
            self.busqueda_rollouts(max_rollouts)
        else:
            print("Fallo en los argumentos")

    def busqueda_tiempo(self, limite_tiempo):

        inicio = time.perf_counter()
        n_rollout = 0

        while (time.perf_counter() - inicio) < limite_tiempo:
            node, state = self.select_node()
            winner = self.roll_out(state)
            n_rollout += 1
            self.backup(node, winner, n_rollout)                                                                       ############ DA NEGATIVO WTF ##############
        
        self.tiempo_busqueda = time.perf_counter() - inicio
        self.rollouts = n_rollout
        print(self.print_tree())
        print("\nNumero de rollouts: " + str(self.rollouts))
        print("\nTiempo de busqueda: " + str(self.tiempo_busqueda))

    def busqueda_rollouts(self, max_rollouts):

        inicio = time.perf_counter()
        n_rollout = 0

        while n_rollout < max_rollouts:
            node, state = self.select_node()
            winner = self.roll_out(state)
            n_rollout += 1
            self.backup(node, winner, n_rollout)                                                                       ############ DA NEGATIVO WTF ##############
        
        self.tiempo_busqueda = time.perf_counter() - inicio
        self.rollouts = n_rollout
        print(self.print_tree())
        print("\nNumero de rollouts: " + str(self.rollouts))
        print("\nTiempo de busqueda: " + str(self.tiempo_busqueda))


    def roll_out(self, state):

        acciones=[]                                                                  # Este simboliza la acción de no atacar

        while state.winner()[0] == False:
            for n_ataque, objetivos in list(state.acciones_posibles().items()):                     # OPTIMIZAR
                for o in objetivos:
                    acciones.append((n_ataque._idN, o._idN))
            if len(acciones) == 0:
                accion = None
            else:
                accion = r.choice(acciones)
            state.jugada(accion)
            acciones = []
        return state.winner()

    def backup(self, node, winner, n_rollout):
        
        puntuacion = 0

        if self.player._num == winner[1]._num:
            puntuacion = 1
        else:
            puntuacion = -1

        while node is not None:
            node.nvisited += 1
            node.reward += puntuacion
            node.calculo_ucb(n_rollout)
            node = node.parent

    def mejor_jugada(self):                                                         # Escoge el nodo que mas puntuacion tiene, o lo que es lo mismo, el que mas se ha simulado
        max_ucb = max(self.root.children.values(), key = lambda n: n.ucb).ucb
        max_repetidos = [n for n in self.root.children.values() if n.ucb == max_ucb]
        nodo_elegido = r.choice(max_repetidos)
        return nodo_elegido.accion

    def print_tree(self, tree_nodes = None, cadena = "", nivel = 0):
        if tree_nodes is None:
            cadena = str(self.root) + "\n"
            if len(self.root.children) != 0:
                cadena = self.print_tree(tree_nodes = self.root.children, cadena = cadena, nivel = copy.copy(nivel) + 1)
        else:
            for tn in tree_nodes.values():
                for i in range(0,nivel):
                    cadena += "\t"
                cadena += str(tn) + "\n"
                if len(tn.children) !=0:
                    cadena = self.print_tree(tree_nodes = tn.children, cadena = cadena, nivel = copy.copy(nivel) + 1)
        return cadena

    def update(self, state, player):
        self.root_state = copy.deepcopy(state)
        self.player = player
        acciones_posibles = list(state.acciones_posibles().items())
        aux = []
        aux.append((0,0))
        for n_ataque, objetivos in acciones_posibles:
            for o in objetivos:
                aux.append((n_ataque._idN, o._idN))
        root_children = list(self.root.children.keys())

        for a in aux:
            if a not in root_children:
                node = Node_Tree(a, self.root_state)
                self.root_state.children.setdefault(a, node)
        
        for c in root_children:
            if c not in aux:
                del self.root.children[c]



# en el estado se crea un riskmap que ese es el estado inicial. A partir de ahi se va desarrollando.
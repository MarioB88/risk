import random as r
import time
from math import sqrt, log
from node_tree import Node_Tree
from player import Player

class mctsAgent:
    def __init__(self, state):
        self.root = Node_Tree()
        self.state = state
        self.node_count = 0
        self.rollouts = 0

    def expand(self, parent, state):
        children = []
        
        if state.isfinished() == True:
            return False
        
        for a in state.acciones():
            node = Node(a,parent)
            children.append(node)
            parent.children.setdefault(a, node)

        return True
    
    def select_node():
        node = self.root
        state = state.copy()
        while len(node.children) != 0 :
            children = node.children.values()
            ucbs = [c.ucb for c in children]
            maximo = max(ucbs)
            nodo_maximo = [c for c in children if c.ucb == maximo]
            node = r.choice(nodo_maximo)
            state.jugada(node.accion)

            if node.N == 0:
                return node, state
        
        if self.expand(node, state):                                        # Devuelve True si se puede expandir y False si no
            node = choice(list(nodes.children.values()))
            state.jugada(node.accion)
        return node, state

    def busqueda(self, limite_tiempo):

        inicio = time.clock()

        while (time.clock() - inicio) < limite_tiempo:
            pass



# en el estado se crea un riskmap que ese es el estado inicial. A partir de ahi se va desarrollando.
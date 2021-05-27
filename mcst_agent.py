import random as r
import time
import copy
from node_tree import Node_Tree

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
    
    def select_node(self, simulaciones):
        
        global umbral
        node = self.root
        state = copy.deepcopy(self.root_state)
        while len(node.children) != 0 :
            children = node.children.values()
            list_children = list(children)
            node = max(list_children, key = lambda x: x.calculo_ucb(simulaciones))
            while True:
                try:
                    state.jugada(node.accion)
                    break
                except KeyError:
                    list_children.remove(node)
                    node = max(list_children, key = lambda x: x.calculo_ucb(simulaciones))
                    continue
            if node.nvisited == 0:
                return node, state

        if self.expand(node, state):                                        # Devuelve True si se puede expandir y False si no
            list_children = list(node.children.values())
            node = r.choice(list_children)
            while True:
                try:
                    state.jugada(node.accion)
                    break
                except KeyError:
                    list_children.remove(node)
                    node = r.choice(list_children)
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
            node, state = self.select_node(n_rollout)
            winner = self.roll_out(state)
            n_rollout += 1
            self.backup(node, winner, n_rollout)                                                                       ############ DA NEGATIVO WTF ##############
        
        self.tiempo_busqueda = time.perf_counter() - inicio
        self.rollouts = n_rollout
        #print(self.print_tree())
        print(self.print_primeros_hijos())
        print("\nNumero de rollouts: " + str(self.rollouts))
        print("\nTiempo de busqueda: " + str(self.tiempo_busqueda))

    def busqueda_rollouts(self, max_rollouts):

        inicio = time.perf_counter()
        n_rollout = 0

        while n_rollout < max_rollouts:
            node, state = self.select_node(n_rollout)
            winner = self.roll_out(state)
            n_rollout += 1
            self.backup(node, winner, n_rollout)
        
        self.tiempo_busqueda = time.perf_counter() - inicio
        self.rollouts = n_rollout
        #print(self.print_tree())
        print(self.print_primeros_hijos())
        print("\nNumero de rollouts: " + str(self.rollouts))
        print("\nTiempo de busqueda: " + str(self.tiempo_busqueda))


    def roll_out(self, state):
        
        while state.winner()[0] == False:
            n_ataque, n_objetivo = state.accion_aleatoria()
            if n_ataque == 0:
                state.jugada(None)
            else:
                state.jugada((n_ataque, n_objetivo))
                
        return state.winner()

    def backup(self, node, winner, n_rollout):
        
        puntuacion = 0
        total = 0

        if self.player._num == winner[1]._num:
            puntuacion = 1
        else:
            puntuacion = -1

        node.nvisited += 1
        node.reward += puntuacion
        node.calculo_ucb(n_rollout)
        node = node.parent
        while node is not None:
            node.nvisited += 1
            children = list(node.children.values())
            for n in children:
                total += n.reward
            node.reward = total/len(children)
            node.calculo_ucb(n_rollout)
            node = node.parent

    def best_move(self):                                                                             # Escoge el nodo que mas se ha simulado
        max_nvisited = max(self.root.children.values(), key = lambda n: n.nvisited).nvisited
        max_repetidos = [n for n in self.root.children.values() if n.nvisited == max_nvisited]
        nodo_elegido = r.choice(max_repetidos)
        return nodo_elegido.accion

    def print_tree(self, tree_nodes = None, cadena = "", nivel = 0):
        if tree_nodes is None:
            cadena = str(self.root) + "\n"
            if len(self.root.children) != 0:
                cadena = self.print_tree(tree_nodes = self.root.children, cadena = cadena, nivel = copy.copy(nivel) + 1)
        else:
            for tn in tree_nodes.values():
                for _ in range(0,nivel):
                    cadena += "\t"
                cadena += str(tn) + "\n"
                if len(tn.children) !=0:
                    cadena = self.print_tree(tree_nodes = tn.children, cadena = cadena, nivel = copy.copy(nivel) + 1)
        return cadena
    
    def print_primeros_hijos(self):
        cadena = str(self.root) + "\n"
        for c in list(self.root.children.values()):
            cadena += "\t" + str(c) + "\n"
        return cadena

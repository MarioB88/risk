import random as r
from nodes import Node

class Player:
    def __init__(self, num, nodesHolded, nsoldiers):
        self._num = num
        self._nodesHolded = nodesHolded.copy()
        self._nsoldiers = nsoldiers

    #DEFINIMOS SETTERS

    def set_num(self, num):
        self._num = num

    def set_nodesHolded(self, nodesHolded):
        self._nodesHolded = nodesHolded.copy()
    
    def set_nsoldiers(self, nsoldiers):
        self._nsoldiers = nsoldiers

    #DEFINIMOS GETTERS

    def get_num(self):
        return self._num

    def get_nodesHolded(self):
        return self._nodesHolded
    
    def get_nsoldiers(self):
        return self._nsoldiers

    # Funciones para hacer más sencilla la lectura de código

    def get_randomNode(self):
        list_keys = list(self._nodesHolded.keys())
        k = r.choice(list_keys)
        return self._nodesHolded.get(k)

    def add_nodeHolded(self, idNode, node):
        self._nodesHolded.setdefault(idNode, node)

    def del_node(self, idNode):
        node = self._nodesHolded.pop(idNode)
        if node.get_player() == 1:
            node.set_player(2)
        else:
            node.set_player(1)

    def addn_soldiers(self, n):
        self._nsoldiers += n
        return self._nsoldiers

    def substractn_soldiers(self, n):
        self._nsoldiers -= n
        return self._nsoldiers


    # Funciones del agente

    def player_turn(self, p_other, riskMap):

        self.put_soldiers_in_territory()
        
        n_attack = self.get_randomNode()
        neighbours = n_attack.get_neighbours()
        while len(neighbours) != 0:
            n_target = neighbours.pop(r.randint(0, (len(neighbours)-1)))
            if n_target.get_player() != self.get_num():
                self.attack(n_attack, n_target, riskMap, p_other)
                break

                
    def attack(self, attack, target, riskMap, p_other):

        att_soldiers = attack.get_soldiers()
        tar_soldiers = target.get_soldiers()
        
        if att_soldiers > tar_soldiers:
            attack.set_player(self.get_num())
            self.add_nodeHolded(target.get_idN(), target)
            target.set_soldiers(attack.get_soldiers()-1)
            attack.set_soldiers(1)
            p_other.del_node(target.get_idN())
            print("Ataque realizado con éxito, tus soldados han vencido a la defensa\n")
        else:
            attack.set_soldiers(1)
            print("Fallo en el ataque, todos tus soldados han caído en combate excepto uno\n")

    def put_soldiers_in_territory(self):

        while self.get_nsoldiers() != 0:
            self.get_randomNode().add_soldiers(1)
            self.substractn_soldiers(1)
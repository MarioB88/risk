import copy

class Node:
    def __init__(self, idN, player, soldiers, neighbours, heuristica = 0):
        self._idN = idN
        self._player = player
        self._soldiers = soldiers
        self._neighbours = neighbours[:]
        self._heuristica = heuristica
        self._bsr=0

    #DEFINIMOS SETTERS

    def set_idN(self, idN):
        self._idN = idN

    def set_player(self, player):
        self._player = player
    
    def set_soldiers(self, soldiers):
        self._soldiers = soldiers
    
    def set_neighbours(self, neighbours):
        self._neighbours = neighbours[:]

    def set_heuristica(self, heuristica):
        self._heuristica = heuristica
    
    #DEFINIMOS GETTERS

    def get_idN(self):
        return self._idN
        
    def get_player(self):
        return self._player
    
    def get_soldiers(self):
        return self._soldiers
    
    def get_neighbours(self):
        n_copy = self._neighbours[:]
        return n_copy

    def get_heuristica(self):
        return self._heuristica


    
    def add_neighbour(self, neigh):
        self._neighbours.append(neigh)

    def add_soldiers(self, n):
        self._soldiers += n

    def get_enemy_neigh(self):
        enemies = list(filter(lambda x: x._player._num != self._player._num, self._neighbours))
        return enemies

    def create_heuristica(self):
        bst = 0
        suma_bsr = 0
        solo_neutros = True
        nsoldados = self.get_soldiers()                                                           # Soldados del territorio aliado

        enemigos = self.get_enemy_neigh()
        if len(enemigos) == 0:
            solo_neutros = False
        for e in enemigos:
            if e.get_player()._num != 0:
                solo_neutros = False
            bst += e.get_soldiers()
        
        if bst != 0:
            self._bsr = nsoldados/bst
        else:
            if not solo_neutros:
                self._bsr = 0
            else:
                self._heuristica = 1                                                  
                return

        if self._player._num != 0:
            if len(self._player.get_nodesHolded().values()) == 1:
                self._heuristica = 1
            else:
                for v in self._player.get_nodesHolded().values():
                    suma_bsr += v._bsr
                    if suma_bsr != 0:
                        nbsr = self._bsr/suma_bsr                                                           # BSR normalizada
                        self._heuristica = nbsr
                    else:
                        self._heuristica = 0
        
        else:
            self._heuristica = 0


       
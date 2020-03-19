class Node:
    def __init__(self, idN, player, soldiers, neighbours):
        self._idN = idN
        self._player = player
        self._soldiers = soldiers
        self._neighbours = neighbours[:]

    #DEFINIMOS SETTERS

    def set_idN(self, idN):
        self._idN = idN

    def set_player(self, player):
        self._player = player
    
    def set_soldiers(self, soldiers):
        self._soldiers = soldiers
    
    def set_neighbours(self, neighbours):
        self._neighbours = neighbours[:]
    
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


    
    def add_neighbour(self, neigh):
        self._neighbours.append(neigh)

    def add_soldiers(self, n):
        self._soldiers += n


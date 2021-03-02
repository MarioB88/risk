class State:
    def __init__(self, total_map, player, p_other):
        self.total_map = total_map
        self.acciones = {}
        self.player = player
        self.p_other = p_other
        self.turn = 0

    def set_acciones(self, acciones):
        self.acciones = acciones.copy()
        return self.acciones

    def acciones_posibles(self):
        self.acciones = {}
        player = None
        if self.turn == 0:
            player = self.player
        else:
            player = self.p_other
        territorios = list(player.get_nodesHolded().keys())
        posible_ataque = list(filter(lambda x: self.total_map.get(x)._soldiers > 1 and self.total_map.get(x)._heuristica > 0, territorios))
        #posible_ataque = list(filter(lambda x: self.total_map.get(x)._heuristica > 0, aux)) 

        for id_terr in posible_ataque:
            terr = self.total_map.get(id_terr)
            self.acciones.setdefault(terr, terr.get_enemy_neigh())

        return self.acciones

    def jugada(self, accion):                       
        player = None
        p_other = None

        if self.turn == 0:
            player = self.player
            p_other = self.p_other
        else:
            player = self.p_other
            p_other = self.player
        
        if accion is not None:
            id_n_ataque, id_objetivo = accion
            player.tira_dados(self.total_map.get(id_n_ataque), self.total_map.get(id_objetivo), p_other, self.total_map)

        player.reordenacion(self.total_map)
        player.sold_continentes()                                       ######## HACERLO COMO EN UNA PARTIDA REAL ATACAR HASTA QUE SE DECIDA NO ATACAR MAS #########
        player.put_soldiers_in_territory(self.total_map)
        player.actualizar_heur(self.total_map)

        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def winner(self):

        if len(self.player.get_nodesHolded().keys()) == 0:
            winner = (True, self.player)
        elif len(self.p_other.get_nodesHolded().keys()) == 0:
            winner = (True, self.p_other)
        else:
            winner = (False, None)

        return winner
        

    
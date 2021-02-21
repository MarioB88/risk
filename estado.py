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
        territorios = list(player.get_nodesHolded().values())
        ids = list(player.get_nodesHolded().keys())
        heuristicas = [t._heuristica for t in territorios]
        heuristicas = list(zip(ids, heuristicas))
        posible_ataque = list(filter(lambda x: x[1] != 0, heuristicas))

        for id_terr, _ in posible_ataque:
            territorio = self.total_map.get(id_terr)
            self.acciones.setdefault(territorio, territorio.get_enemy_neigh())

        return self.acciones

    def jugada(self, accion):                       
        player = None
        p_other = None

        if accion is not None:
            id_n_ataque, id_objetivo = accion
            if self.turn == 0:
                player = self.player
                p_other = self.p_other
            else:
                player = self.p_other
                p_other = self.player

            player.tira_dados(self.total_map.get(id_n_ataque), self.total_map.get(id_objetivo), p_other, self.total_map)
            player.reordenacion()
            player.sold_continentes()
            player.put_soldiers_in_territory(self.total_map)
            player.actualizar_heur()

        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def winner(self):

        if len(self.player.get_nodesHolded().keys()) == 0 or len(self.p_other.get_nodesHolded().keys()) == 0:
            print("GANADOR JUGADOR: " + str(self.player._num))
            winner = (True, self.player)
        else:
            winner = (False, None)

        return winner
        
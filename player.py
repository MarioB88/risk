import random as r
import operator
import networkx as nx
import copy
import time
from estado import State
from mcst_agent import McstAgent
from node_tree import Node_Tree
from nodes import Node

class Player:
    def __init__(self, num, nodesHolded, nsoldiers, riskMap, list_cont):
        self._num = num
        self._nodesHolded = nodesHolded.copy()
        self._nsoldiers = nsoldiers
        self._riskMap = riskMap
        self._list_cont = list_cont

    #DEFINIMOS SETTERS

    def set_num(self, num):
        self._num = num

    def set_nodesHolded(self, nodesHolded):
        self._nodesHolded = nodesHolded.copy()
    
    def set_nsoldiers(self, nsoldiers):
        self._nsoldiers = nsoldiers

    def set_riskMap(self, riskMap):
        self._riskMap = riskMap

    #DEFINIMOS GETTERS

    def get_num(self):
        return self._num

    def get_nodesHolded(self):
        return self._nodesHolded
    
    def get_nsoldiers(self):
        return self._nsoldiers

    def get_riskMap(self):
        return self._riskMap

    # Funciones para hacer más sencilla la lectura de código

    def get_randomNode(self):
        list_keys = list(self._nodesHolded.keys())
        k = r.choice(list_keys)
        return self._nodesHolded.get(k)

    def add_nodeHolded(self, idNode, node):
        self._nodesHolded.setdefault(idNode, node)

    def del_node(self, idNodeTarget, total_map):
        nodeTarget = total_map.get(idNodeTarget)
        if nodeTarget._player._num != 0:
            nodeTarget = self._nodesHolded.pop(idNodeTarget)

    def addn_soldiers(self, n):
        self._nsoldiers += n
        return self._nsoldiers

    def substractn_soldiers(self, n):
        if self._nsoldiers > 0:
            self._nsoldiers -= n
        else:
            return self._nsoldiers
        return self._nsoldiers


    # Funciones del agente

    def attack_IA(self, p_other, total_map):                                                                      

        copy_player = copy.deepcopy(self)
        state = State(copy.deepcopy(total_map), copy_player, copy.deepcopy(p_other))                                            
        mcst = McstAgent(state, copy_player)
        #mcst.tipo_busqueda(limite_tiempo = 30)
        print("Nueva busqueda ...")
        mcst.tipo_busqueda(max_rollouts= 1000)
        mejor_accion = mcst.mejor_jugada()
        n_ataque, objetivo = mejor_accion
        print("La mejor accion seleccionada ha sido: Atacar desde " + str(n_ataque) + " hacia " + str(objetivo))
        if n_ataque != 0:
            print("El ataque con " + str(total_map.get(n_ataque)._soldiers) + " soldados y la defensa con " + str(total_map.get(objetivo)._soldiers))
        self.tira_dados(total_map.get(n_ataque), total_map.get(objetivo), p_other, total_map)
        time.sleep(1)

        while n_ataque != 0:
            copy_player = copy.deepcopy(self)
            state=State(copy.deepcopy(total_map), copy_player, copy.deepcopy(p_other))
            mcst = McstAgent(state, copy_player)
            #mcst.update(state, copy_player)
            #mcst.tipo_busqueda(limite_tiempo = 20)
            print("Nueva busqueda ...")
            mcst.tipo_busqueda(max_rollouts=1000)
            mejor_accion = mcst.mejor_jugada()
            n_ataque, objetivo = mejor_accion
            print("La mejor accion seleccionada ha sido: Atacar desde " + str(n_ataque) + " hacia " + str(objetivo))
            if n_ataque != 0:
                print("El ataque con " + str(total_map.get(n_ataque)._soldiers) + " soldados y la defensa con " + str(total_map.get(objetivo)._soldiers))
            self.tira_dados(total_map.get(n_ataque), total_map.get(objetivo), p_other, total_map)                               
            time.sleep(1)
        print("Fin del turno")
        self.actualizar_heur(total_map)

        """         for v in self._nodesHolded.values():
            v.create_heuristica()
        
        territorios = list(self.get_nodesHolded().values())
        aux = territorios.copy()
        ids = list(self.get_nodesHolded().keys())
        heuristicas = [x.get_heuristica() for x in aux]
        heuristicas = list(zip(ids, heuristicas))

        id_nodo, _ = max(heuristicas, key = operator.itemgetter(1))
        n_attack = total_map.get(id_nodo)
        ids = []
        sold_defensa = []

        neighbours = n_attack.get_neighbours()
        for n in neighbours:
            if n.get_player() == self:
                continue
            elif n.get_player() == None:
                n.set_soldiers(n_attack.get_soldiers()-1)
                n_attack.set_soldiers(1)
                self.add_nodeHolded(n.get_idN(), n)
                n.set_player(self)
                print("Territorio neutro conquistado")
                
            else:
                ids.append(n.get_idN())
                sold_defensa.append(n.get_soldiers())

        sold_vecinos = list(zip(ids, sold_defensa))
        if sold_vecinos:
            id_nodo, _ = min(sold_vecinos, key = operator.itemgetter(1))
            n_target = total_map.get(id_nodo)
            self.tira_dados(n_attack, n_target, p_other)

        else:
            print("No hay enemigo al que atacar")
        """

    def attack_human(self, p_other, total_map, n_ataque, objetivo):
        enemigos = total_map.get(n_ataque).get_enemy_neighbours()
        aux=[]
        for e in enemigos:
            aux.append(e._idN)
        if n_ataque not in list(self.get_nodesHolded().keys()):
            print("Selecciona un territorio que sea tuyo.")
        elif objetivo not in list(p_other.get_nodesHolded().keys()):
            print("Ataca a un territorio que no sea tuyo.")
        elif objetivo not in aux:
            print("Ataca a un objetivo que sea tu vecino")
        else:
            self.tira_dados2(total_map.get(n_ataque), total_map.get(objetivo), p_other, total_map)
            self.actualizar_heur(total_map)

    def tira_dados2(self, attack, target, p_other, total_map):

        if attack == 0 or attack is None:
            print("Acción de no atacar seleccionada")
            return

        if target.get_player()._num == 0:
            if attack.get_soldiers()-1 != 0:
                target.set_soldiers(attack.get_soldiers()-1)
            else:
                target.set_soldiers(1)
            attack.set_soldiers(1)
            self.add_nodeHolded(target.get_idN(), target)
            target.set_player(self)
            print("Territorio neutro conquistado")

        elif self.tirar_dado(attack, target):
            if attack.get_soldiers() >= target.get_soldiers():
                self.add_nodeHolded(target.get_idN(), target)
                target.set_soldiers(attack.get_soldiers()-1)
                if target.get_soldiers() == 0:
                    target.set_soldiers(1)
                attack.set_soldiers(1)
                target.set_player(self)
                p_other.del_node(target.get_idN(), total_map)
                print("Ataque desde nodo: " + str(attack.get_idN()) + " realizado con éxito, tus soldados han vencido a la defensa del nodo: " + str(target.get_idN()) + "\n")
            else:
                target.set_soldiers(abs(attack.get_soldiers()-target.get_soldiers()))
                if target.get_soldiers() == 0:
                    target.set_soldiers(1)
                print("Ataque desde nodo: " + str(attack.get_idN()) + " realizado con éxito, pero no has logrado conquistar el nodo: " + str(target.get_idN()) + "\n")
        else:
            diff = attack.get_soldiers()-target.get_soldiers()
            if diff > 0:
                attack.set_soldiers(attack.get_soldiers()-target.get_soldiers())
            else:
                attack.set_soldiers(1)
            print("Fallo en el ataque desde nodo: " + str(attack.get_idN()) + ", tus soldados han caido en combate\n")
    
    def tira_dados(self, attack, target, p_other, total_map):

        if attack == 0 or attack is None:
            #print("Acción de no atacar seleccionada")
            return

        if target.get_player()._num == 0:
            if attack.get_soldiers()-1 != 0:
                target.set_soldiers(attack.get_soldiers()-1)
            else:
                target.set_soldiers(1)
            attack.set_soldiers(1)
            self.add_nodeHolded(target.get_idN(), target)
            target.set_player(self)
            #print("Territorio neutro conquistado")

        elif self.tirar_dado(attack, target):
            if attack.get_soldiers() >= target.get_soldiers():
                self.add_nodeHolded(target.get_idN(), target)
                target.set_soldiers(attack.get_soldiers()-1)
                if target.get_soldiers() == 0:
                    target.set_soldiers(1)
                attack.set_soldiers(1)
                target.set_player(self)
                p_other.del_node(target.get_idN(), total_map)
                #print("Ataque desde nodo: " + str(attack.get_idN()) + " realizado con éxito, tus soldados han vencido a la defensa del nodo: " + str(target.get_idN()) + "\n")
            else:
                target.set_soldiers(abs(attack.get_soldiers()-target.get_soldiers()))
                if target.get_soldiers() == 0:
                    target.set_soldiers(1)
                #print("Ataque desde nodo: " + str(attack.get_idN()) + " realizado con éxito, pero no has logrado conquistar el nodo: " + str(target.get_idN()) + "\n")
        else:
            diff = attack.get_soldiers()-target.get_soldiers()
            if diff > 0:
                attack.set_soldiers(attack.get_soldiers()-target.get_soldiers())
            else:
                attack.set_soldiers(1)
            #print("Fallo en el ataque desde nodo: " + str(attack.get_idN()) + ", tus soldados han caido en combate\n")

    def put_soldiers_in_territory(self, total_map):                                        

        ids_territorios = list(self.get_nodesHolded().keys())
        menor_umbral = list(filter(lambda i: total_map.get(i)._heuristica > 0, ids_territorios))
        longitud = len(menor_umbral)
        
        if longitud != 0:
            media_soldados = (self.get_nsoldiers() // longitud)
            for id_nodo in menor_umbral:
                nodo = total_map.get(id_nodo)
                nodo.add_soldiers(media_soldados)
                self.substractn_soldiers(media_soldados)
                nodo.create_heuristica()
        else:
            longitud_aux = len(ids_territorios)
            media_soldados = (self.get_nsoldiers() // longitud_aux)
            for id_nodo in ids_territorios:
                nodo = total_map.get(id_nodo)
                nodo.add_soldiers(media_soldados)
                self.substractn_soldiers(media_soldados)
                nodo.create_heuristica()

        """         if menor_umbral:
            id_nodo, _ = r.choice(menor_umbral)
            nodo = self.get_nodesHolded().get(id_nodo)
            
        else:
            id_nodo, _ = max(heuristicas, key = operator.itemgetter(1))
            nodo = total_map.get(id_nodo)
        
        id_nodo, _ = max(heuristicas, key = operator.itemgetter(1)) 
        nodo = total_map.get(id_nodo)
        nodo.add_soldiers(1)
        self.substractn_soldiers(1)
        nodo.create_heuristica()
        return nodo """


    def tirar_dado(self, nodoAtaque, nodoDefensa):                                      # Si devuelve True el ataque se ha realizado con exito, y False si ha fallado el ataque

        soldAtaque = nodoAtaque.get_soldiers()
        soldDefensa = nodoDefensa.get_soldiers()
        maximoAtt = 0
        maximoDef = 0

        if soldAtaque == 0:
            maximoAtt = 0        
        elif soldAtaque <= 3:
            for _ in range(soldAtaque):
                dadoAtaque = r.randint(1, 6)
                if dadoAtaque > maximoAtt:
                    maximoAtt = dadoAtaque
        else:
            for _ in range(3):
                dadoAtaque = r.randint(1, 6)
                if dadoAtaque > maximoAtt:
                    maximoAtt = dadoAtaque
        
        if soldDefensa == 0:
            maximoDef = 0        
        elif soldDefensa <= 2:
            for _ in range(soldDefensa):
                dadoDefensa = r.randint(1, 6)
                if dadoDefensa > maximoDef:
                    maximoDef = dadoDefensa
        else:
            for _ in range(2):
                dadoDefensa = r.randint(1, 6)
                if dadoDefensa > maximoDef:
                    maximoDef = dadoDefensa

        #print("El ataque desde el nodo " + str(nodoAtaque.get_idN()) + " con " + str(nodoAtaque.get_soldiers()) + " y heuristica:" + str(nodoAtaque._heuristica) + " tiro el dado y obtuvo: " + str(maximoAtt))
        #print("La defensa desde el nodo " + str(nodoDefensa.get_idN()) + " con " + str(nodoDefensa.get_soldiers()) + " y heuristica:" + str(nodoDefensa._heuristica) +" tiro el dado y obtuvo: " + str(maximoDef))

        return maximoAtt > maximoDef
 

    def inicializar_sold_terr(self, total_map):
        
        territorios = list(total_map.keys())
        aux = territorios.copy()
        
        id_nodo = r.choice(aux)
        nodo = total_map.get(id_nodo)

        while (nodo.get_player()._num != self._num) and (nodo.get_player()._num != 0):
            aux.remove(id_nodo)
            id_nodo = r.choice(aux)
            nodo = total_map.get(id_nodo)
        
        nodo.add_soldiers(1)
        self.substractn_soldiers(1)
        nodo.set_player(self)
        self.add_nodeHolded(id_nodo , nodo)
        nodo.create_heuristica()

    def reordenacion(self, total_map):
        isPath = 0
        ids_territorios = list(self.get_nodesHolded().keys())
        id_max_heur = max([(i, total_map.get(i)._heuristica) for i in ids_territorios], key = operator.itemgetter(1))[0]                         ####### ENCONTRAR EL NODO CON MAYOR HEURISTICA ########
        umbral = list(filter(lambda i: total_map.get(i)._heuristica == 0 and total_map.get(i)._soldiers > 1, ids_territorios))

        if umbral:
            for id_nodo in umbral:
                isPath = nx.has_path(self._riskMap, id_nodo, id_max_heur)
                if not isPath:
                    continue
                else:
                    #print("Se han trasladado " + str(total_map.get(id_nodo).get_soldiers()-1) + " soldados desde el nodo " + str(id_nodo) + " hasta el nodo " + str(id_max_heur))
                    total_map.get(id_max_heur).add_soldiers(total_map.get(id_nodo).get_soldiers()-1)
                    total_map.get(id_nodo).set_soldiers(1)
                    continue
            
        #print("Fin de la reordenacion")


    def sold_continentes(self):
        ids = list(self.get_nodesHolded().keys())
        cont_completos = 0
        for cont in self._list_cont:
            if set(cont) <= set(ids):
                cont_completos += 1
        #print(cont_completos)
        sold_nuevos = 10 + (5*cont_completos)
        #print("Se añaden " + str(sold_nuevos) + " soldados nuevos.")

        self.addn_soldiers(sold_nuevos)

    def actualizar_heur(self, total_map):
        territorios = list(total_map.values())
        for t in territorios:
            t.create_heuristica()




        # ATAQUE ATACAR AL QUE MAS PROB DE GANAR TENGAS (CALCULAR PROB)
        # ESCRIBE EL REPORT PUTO TONTO Y DENTRO DE POCO A SER POSIBLE QUE PARECES SUBNORMAL

        ##### IMPORTANTE. LA REWARD PUEDE SER EN FUNCION DE LOS SOLDADOS QUE GANO Y DE LOS TERRITOIOS QUE TENGA. POR EJEMPLO SI GANO 10 SOLDADOS Y TENGO 7 TERRITORIOS DESPUES DE HACER UNA ACCION PUES LA REWARD SERIA ALGO COMO 10 + 13.
        ##### PERO SI HAGO OTRA ACCION QUE HACE QUE TENGA UN TERRITORIO MAS PERO QUE GANE MAS SOLDADOS EN EL SIGUIENTE TURNO SERIA POR EJEMPLO 15 (SOLDADOS QUE GANO PORQUE HE CONQUISTADO UN CONTINENTE) + 8 (TERRITORIOS QUE TENGO)
        ##### DE IGUAL MANERA SI PIERDO.
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
        return self._nsoldiers

    # Funciones del agente

    def attack_IA(self, p_other, total_map, tipo, limite):                                                                      

        copy_player = copy.deepcopy(self)
        state = State(copy.deepcopy(total_map), copy_player, copy.deepcopy(p_other))                                            
        mcst = McstAgent(state, copy_player)
        print("Nueva busqueda ...")
        if tipo == "1":
            mcst.tipo_busqueda(limite_tiempo = limite)
        else:
            mcst.tipo_busqueda(max_rollouts= limite)
        mejor_accion = mcst.best_move()
        n_ataque, objetivo = mejor_accion
        print("La mejor accion seleccionada ha sido: Atacar desde " + str(n_ataque) + " hacia " + str(objetivo))
        if n_ataque != 0:
            print("El ataque con " + str(total_map.get(n_ataque)._soldiers) + " soldados y la defensa con " + str(total_map.get(objetivo)._soldiers))
        self.tira_dados2(total_map.get(n_ataque), total_map.get(objetivo), p_other, total_map)
        time.sleep(1)

        while n_ataque != 0 and len(p_other.get_nodesHolded()) != 0:
            copy_player = copy.deepcopy(self)
            state=State(copy.deepcopy(total_map), copy_player, copy.deepcopy(p_other))
            mcst = McstAgent(state, copy_player)
            print("Nueva busqueda ...")
            if tipo == "1":
                mcst.tipo_busqueda(limite_tiempo = limite)
            else:
                mcst.tipo_busqueda(max_rollouts= limite)
            mejor_accion = mcst.best_move()
            n_ataque, objetivo = mejor_accion
            print("La mejor accion seleccionada ha sido: Atacar desde " + str(n_ataque) + " hacia " + str(objetivo))
            if n_ataque != 0:
                print("El ataque con " + str(total_map.get(n_ataque)._soldiers) + " soldados y la defensa con " + str(total_map.get(objetivo)._soldiers))
            self.tira_dados2(total_map.get(n_ataque), total_map.get(objetivo), p_other, total_map)                               
            time.sleep(1)
        print("Fin del turno")
        self.actualizar_heur()

    def attack_human(self, p_other, total_map, n_ataque, objetivo):
        enemigos = total_map.get(n_ataque).get_enemy_neigh()
        aux=[]
        for e in enemigos:
            aux.append(e._idN)
        if n_ataque not in list(self.get_nodesHolded().keys()):
            print("Selecciona un territorio que sea tuyo.")
        elif total_map.get(objetivo)._player._num == self._num:
            print("Ataca a un territorio que no sea tuyo.")
        elif objetivo not in aux:
            print("Ataca a un objetivo que sea tu vecino")
        else:
            self.tira_dados2(total_map.get(n_ataque), total_map.get(objetivo), p_other, total_map)
            self.actualizar_heur()

    def tira_dados2(self, attack, target, p_other, total_map):

        if attack == 0 or attack is None:
            print("Acción de no atacar seleccionada")
            return

        if attack.get_soldiers() == 1:
            print("No puedes atacar con un soldado.")
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
            return

        if attack.get_soldiers() == 1:
            return

        if target.get_player()._num == 0:
            if attack.get_soldiers()-1 != 0:
                target.set_soldiers(attack.get_soldiers()-1)
            else:
                target.set_soldiers(1)
            attack.set_soldiers(1)
            self.add_nodeHolded(target.get_idN(), target)
            target.set_player(self)
            target.create_heuristica()

        elif self.tirar_dado(attack, target):
            if attack.get_soldiers() >= target.get_soldiers():
                self.add_nodeHolded(target.get_idN(), target)
                target.set_soldiers(attack.get_soldiers()-1)
                if target.get_soldiers() == 0:
                    target.set_soldiers(1)
                attack.set_soldiers(1)
                target.set_player(self)
                p_other.del_node(target.get_idN(), total_map)
                target.create_heuristica()
            else:
                target.set_soldiers(abs(attack.get_soldiers()-target.get_soldiers()))
                if target.get_soldiers() == 0:
                    target.set_soldiers(1)
                
        else:
            diff = attack.get_soldiers()-target.get_soldiers()
            if diff > 0:
                attack.set_soldiers(attack.get_soldiers()-target.get_soldiers())
            else:
                attack.set_soldiers(1)
            

    def put_soldiers_in_territory(self, total_map, proporcional = True):                                        

        if proporcional:
            ids_territorios = list(self.get_nodesHolded().keys())
            menor_umbral = list(filter(lambda i: total_map.get(i)._heuristica > 0, ids_territorios))
            longitud = len(menor_umbral)
            longitud_aux = len(ids_territorios)
            
            if longitud != 0:
                media_soldados = (self.get_nsoldiers() // longitud)
                for id_nodo in menor_umbral:
                    nodo = total_map.get(id_nodo)
                    nodo.add_soldiers(media_soldados)
                    self.substractn_soldiers(media_soldados)
                    nodo.create_heuristica()
            elif longitud_aux != 0:                
                media_soldados = (self.get_nsoldiers() // longitud_aux)
                for id_nodo in ids_territorios:
                    nodo = total_map.get(id_nodo)
                    nodo.add_soldiers(media_soldados)
                    self.substractn_soldiers(media_soldados)
                    nodo.create_heuristica()
            else:
                return
        else:
            territorios = self.get_nodesHolded().values()
            for t in territorios:
                nsoldados = t.get_heuristica() * self.get_nsoldiers()
                t.add_soldiers(nsoldados)
                self.substractn_soldiers(nsoldados)
                t.create_heuristica()

    def put_soldiers_human(self, total_map, id_territorio, nsoldados):
        if id_territorio not in list(self.get_nodesHolded().keys()):
            print("Por favor selecciona un territorio que sea tuyo.")
        elif nsoldados > self.get_nsoldiers():
            print("No puedes asignar mas soldados de los que tienes")
        elif nsoldados < 0:
            print("No puedes asignar un número negativo de soldados")
        else:
            terr = total_map.get(id_territorio)
            terr.add_soldiers(nsoldados)
            self.substractn_soldiers(nsoldados)


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


    def reordenacion(self, total_map):
        isPath = 0
        ids_territorios = list(self.get_nodesHolded().keys())
        if len(ids_territorios) == 0:
            return
        else:
            id_max_heur = max([(i, total_map.get(i)._heuristica) for i in ids_territorios], key = operator.itemgetter(1))[0]                         ####### ENCONTRAR EL NODO CON MAYOR HEURISTICA ########
            umbral = list(filter(lambda i: total_map.get(i)._heuristica == 0 and total_map.get(i)._soldiers > 1, ids_territorios))

            if umbral:
                for id_nodo in umbral:
                    isPath = nx.has_path(self._riskMap, id_nodo, id_max_heur)
                    if not isPath:
                        continue
                    else:
                        total_map.get(id_max_heur).add_soldiers(total_map.get(id_nodo).get_soldiers()-1)
                        total_map.get(id_nodo).set_soldiers(1)
                        continue
    

    def reordenacion_human(self, total_map, inicial, nsoldados, objetivo):

        if inicial not in list(self.get_nodesHolded().keys()) or objetivo not in list(self.get_nodesHolded().keys()):
            print("Por favor selecciona territorios que sean tuyos.")
        elif nsoldados > total_map.get(inicial).get_soldiers():
            print("El número de soldados seleccionados supera el número de soldados que existen en el territorio inicial.")
        elif nsoldados < 0:
            print("No puedes trasladar un número negativo de soldados.")
        elif not nx.has_path(self._riskMap, inicial, objetivo):
            print("No hay ningún camino disponible entre los dos nodos, por lo que no se pueden trasladar.")
        else:
            total_map.get(objetivo).add_soldiers(nsoldados)
            total_map.get(inicial).substract_soldiers(nsoldados)


    def sold_continentes(self):
        ids = list(self.get_nodesHolded().keys())
        cont_completos = 0
        for cont in self._list_cont:
            if cont <= set(ids):
                cont_completos += 1
        #print(cont_completos)
        sold_nuevos = 10 + (5*cont_completos)
        #print("Se añaden " + str(sold_nuevos) + " soldados nuevos.")

        self.addn_soldiers(sold_nuevos)


    def actualizar_heur(self):
        territorios = list(self._nodesHolded.values())
        for t in territorios:
            t.create_heuristica()

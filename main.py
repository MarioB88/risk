import networkx as nx 
import matplotlib.pyplot as plt
import random as r
import threading
import time
from nodes import Node
from player import Player

def draw_graph(player1, player2, update=False):
    global riskMap
    
    # El grafo representa el continente de África en esta foto: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Risk_Game_Map_2004_Edition.png"
    
    riskMap.add_nodes_from(range(1,7))
    riskMap.add_edges_from([(5,3), (5,2), (5,1), (3,2), (2,1), (2,6), (2,4), (6,1), (6,4)])

    pos = nx.spring_layout(riskMap)

    nx.draw_networkx_nodes(riskMap, pos, nodelist= player1.get_nodesHolded().keys(), node_color="r", alpha = 0.8)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= player2.get_nodesHolded().keys(), node_color="y", alpha = 0.8)
    nx.draw_networkx_edges(riskMap, pos)
    nx.draw_networkx_labels(riskMap, pos)

    if update:
        plt.draw()
    else:
        plt.show()


def set_neighbours(riskMap, total_map):

    for n, e in riskMap.edges():
        total_map.get(n).add_neighbour(total_map.get(e))
        total_map.get(e).add_neighbour(total_map.get(n))


def set_soldiers(player1, player2):

    while player1.get_nsoldiers() != 0:
        player1.get_randomNode().add_soldiers(1)
        player2.get_randomNode().add_soldiers(1)
        player1.substractn_soldiers(1)
        player2.substractn_soldiers(1)


if __name__ == '__main__':

    global riskMap
    riskMap=nx.Graph()

    counterOnes = 0
    counterTwos = 0
    nodesPlayer1 = {}
    nodesPlayer2={}
    total_map={}

    for i in range (1,7):
        numRand = r.randint(1,2)
        if numRand == 1:
            counterOnes += 1
        else:
            counterTwos += 1
        
        if counterOnes > 3:
            node = Node(i, 2, 0, [])
            nodesPlayer2.setdefault(i, node)
            total_map.setdefault(i, node)
            continue

        elif counterTwos > 3:
            node = Node(i, 1, 0, [])
            nodesPlayer1.setdefault(i, node)
            total_map.setdefault(i, node)
            continue

        else:
            node = Node(i, numRand, 0, [])
            total_map.setdefault(i, node)
            if numRand == 1:
                nodesPlayer1.setdefault(i, node)
            else:
                nodesPlayer2.setdefault(i, node)
            continue

    player1 = Player(1, nodesPlayer1, 10)
    player2 = Player(2, nodesPlayer2, 10)

    draw_graph(player1, player2)
    set_neighbours(riskMap, total_map)

    set_soldiers(player1, player2)

    binary = True      # Esta variable llevará de qué jugador es el turno, si es 0 sera del primero y si es uno del segundo.

    while (len(player1.get_nodesHolded()) != 0)  and (len(player2.get_nodesHolded()) != 0):
        if binary == True:
            player1.set_nsoldiers(len(player1.get_nodesHolded()))
            player1.player_turn(player2, riskMap)
            binary = False
        else:
            player2.set_nsoldiers(len(player2.get_nodesHolded()))
            player2.player_turn(player1, riskMap)
            binary = True
        
        draw_graph(player1, player2)
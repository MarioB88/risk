import networkx as nx 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as r
import tkinter as tk
from nodes import Node
from player import Player

max_territorios = 18
europa = [11,12,13,14,15,16,17]
africa = [1,2,3,4,5,6]
sudamerica = [7,8,9,10]

def draw_graph(player1, player2, total_map):
    global riskMap
    # El grafo representa el continente de África en esta foto: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Risk_Game_Map_2004_Edition.png"

    player1_nodes = list(player1.get_nodesHolded().keys())
    player2_nodes = list(player2.get_nodesHolded().keys())
    total_nodes = list(total_map.keys())
    aux = list(set(player1_nodes) | set(player2_nodes))
    noplayer_nodes = list(set(aux) ^ set(total_nodes))
    
    root = tk.Tk()
    root.wm_title("Risk (continente África en forma de grafo)")
    root.wm_protocol('WM_DELETE_WINDOW', root.destroy)

    f = plt.figure(figsize=(5,4))
    plt.axis('off')

    pos = nx.spring_layout(riskMap)

    nx.draw_networkx_nodes(riskMap, pos, nodelist= player1_nodes, node_color="r", alpha = 0.8)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= player2_nodes, node_color="y", alpha = 0.8)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= noplayer_nodes, node_color="b", alpha = 0.8)
    nx.draw_networkx_edges(riskMap, pos)
    nx.draw_networkx_labels(riskMap, pos)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    tk.Button(root, text="Next turn", command = lambda:[root.withdraw(), root.quit()]).pack()
    tk.mainloop()


def set_neighbours(riskMap, total_map):

    for n, e in riskMap.edges():
        total_map.get(n).add_neighbour(total_map.get(e))
        total_map.get(e).add_neighbour(total_map.get(n))


def initialize():
    global riskMap
    global total_map
    global europa
    global africa
    global sudamerica
    global list_cont

    list_cont = []
    list_cont.append(europa)
    list_cont.append(africa)
    list_cont.append(sudamerica)

    riskMap=nx.Graph()
    riskMap.add_nodes_from(range(1, max_territorios))
    riskMap.add_edges_from([(5,3), (5,2), (5,1), (3,2), (2,1), (2,6), (2,4), (6,1), (6,4), (5,8), (7,8), (7,9), (8,9), (8,10), (9,10), (5,17), (5,15), (3,15), (17,11), (17,13), (17,15), (13,16), (13,14), (13,15), (13,11), (15,16), (16,14), (11,12), (11,14), (12,14)])
    total_map={}

    player_None = Player(0,{},0,{},[])

    for i in range(1, max_territorios):
        node = Node(i, player_None, 0, [])
        total_map.setdefault(i, node)
    set_neighbours(riskMap, total_map)

    player1 = Player(1, {}, 10, riskMap, list_cont)
    player2 = Player(2, {}, 10, riskMap, list_cont)


    for n in total_map.values():
        n.create_heuristica()

    while(player1.get_nsoldiers() > 0) or (player2.get_nsoldiers() > 0):
        player1.inicializar_sold_terr(total_map)                            
        player2.inicializar_sold_terr(total_map)
        print(player1.get_nsoldiers())
        print(player2.get_nsoldiers())

    
    draw_graph(player1, player2, total_map)

    return player1, player2

if __name__ == '__main__':

    global total_map
    global riskMap
    global list_cont

    player1, player2 = initialize()

    binary = True      # Esta variable llevará de qué jugador es el turno, si es 0 sera del primero y si es uno del segundo.

    while (len(player1.get_nodesHolded()) != 0)  and (len(player2.get_nodesHolded()) != 0):
        num_cont = 0
        sold_nuevos = 0
        if binary == True:
            player1.sold_continentes()
            player1.put_soldiers_in_territory(total_map)
            player1.attack(player2, total_map)
            player1.reordenacion(total_map)
            binary = False
        else:
            player2.sold_continentes()
            player2.put_soldiers_in_territory(total_map)
            player2.attack(player1, total_map)
            player2.reordenacion(total_map)
            binary = True
        
        draw_graph(player1, player2, total_map)
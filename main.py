import networkx as nx 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as r
import tkinter as tk
from nodes import Node
from player import Player

max_territorios = 18
europa = {11,12,13,14,15,16,17}
africa = {1,2,3,4,5,6}
sudamerica = {7,8,9,10}
# norteamerica = [18,19,20,21,22,23,24,25,26]
# asia = [27,28,29,30,31,32,33,34,35,36,37,38]
# australia = [39,40,41,42] 

def draw_graph_IA(player1, player2, total_map):
    global riskMap
    global europa
    global africa
    global sudamerica
    # El grafo representa el continente de África en esta foto: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Risk_Game_Map_2004_Edition.png"

    player1_nodes = list(player1.get_nodesHolded().keys())
    player2_nodes = list(player2.get_nodesHolded().keys())
    total_nodes = list(total_map.keys())
    aux = list(set(player1_nodes) | set(player2_nodes))
    noplayer_nodes = list(set(aux) ^ set(total_nodes))
    
    root = tk.Tk()
    root.wm_title("Risk (mapa reducido)")
    root.wm_protocol('WM_DELETE_WINDOW', root.destroy)

    f = plt.figure(figsize=(8,8))
    plt.axis('off')

    pos = nx.spring_layout(riskMap, k = 0.3, seed = 888)
    labels = {}
    for n in total_nodes:
        string = "ID " + str(n) + "=" + str(total_map.get(n).get_soldiers())
        labels.setdefault(n, string)

    nx.draw_networkx_nodes(riskMap, pos, nodelist= player1_nodes, node_color="#F50707", node_size = 500,alpha = 0.7)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= player2_nodes, node_color="#07F507", node_size = 500,alpha = 0.7)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= noplayer_nodes, node_color="#6E7A6E", node_size = 500, alpha = 0.7)
    nx.draw_networkx_edges(riskMap, pos, edge_color = "#8B938B", alpha = 0.5)
    nx.draw_networkx_labels(riskMap, pos, labels, font_size = 10)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row= 0, column=0)

    tk.Button(root, text="Next turn", command = lambda:[root.withdraw(), root.quit()]).grid(row=1, column = 0)
    tk.mainloop()

def draw_graph_human_attack(player1, player2, total_map):
    global riskMap
    # El grafo representa el continente de África en esta foto: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Risk_Game_Map_2004_Edition.png"
    
    root = tk.Tk()
    root.wm_title("Risk (continente África en forma de grafo)")
    root.wm_protocol('WM_DELETE_WINDOW', root.destroy)

    f = crear_dibujo_grafo(player1, player2, total_map)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    lab_ataque = tk.Label(root, text="ID del territorio de ataque")
    lab_ataque.grid(row = 0, column = 1)
    entr_ataque = tk.Entry(root)
    entr_ataque.grid(row = 0, column = 2)
    lab_objetivo = tk.Label(root, text="ID del territorio objetivo")
    lab_objetivo.grid(row = 0, column = 3)
    entr_objetivo = tk.Entry(root)
    entr_objetivo.grid(row = 0, column = 4)
    lab_continentes = tk.Label(root, text = "Europa: " + str(europa) + "\nAfrica = " + str(africa) + "\nSudamerica = " + str(sudamerica))
    lab_continentes.grid(row=1, column=0)

    btn_atacar = tk.Button(root, text = "Atacar", command = lambda: leer_ataque(entr_ataque, entr_objetivo, player1, player2, total_map, canvas, root))
    btn_atacar.grid(row=1, column=1)
    btn_terminar = tk.Button(root, text="Siguiente acción", command = lambda:[root.withdraw(), root.quit()])
    btn_terminar.grid(row=1, column=2)
    root.update()
    tk.mainloop()
    
def draw_graph_human_putsoldiers(player1, player2, total_map):
    global riskMap
    global europa
    global africa
    global sudamerica
    # El grafo representa el continente de África en esta foto: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Risk_Game_Map_2004_Edition.png"
    
    root = tk.Tk()
    root.wm_title("Risk (continente África en forma de grafo)")
    root.wm_protocol('WM_DELETE_WINDOW', root.destroy)

    f = crear_dibujo_grafo(player1, player2, total_map)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    lab_territorio = tk.Label(root, text="ID donde posicionar soldados")
    lab_territorio.grid(row = 0, column = 1)
    entr_territorio = tk.Entry(root)
    entr_territorio.grid(row = 0, column = 2)
    lab_numero = tk.Label(root, text="Número de soldados que colocar")
    lab_numero.grid(row = 0, column = 3)
    entr_numero = tk.Entry(root)
    entr_numero.grid(row = 0, column = 4)
    lab_nsoldados = tk.Label(root, text= "Tus soldados: " + str(player1.get_nsoldiers()))
    lab_nsoldados.grid(row = 0, column = 5)
    lab_continentes = tk.Label(root, text = "Europa: " + str(europa) + "\nAfrica = " + str(africa) + "\nSudamerica = " + str(sudamerica))
    lab_continentes.grid(row=1, column=0)

    btn_atacar = tk.Button(root, text = "Colocar", command = lambda: colocar_territorios(entr_territorio, entr_numero, player1, player2, total_map, lab_nsoldados, canvas, root))
    btn_atacar.grid(row=1, column=1)
    btn_terminar = tk.Button(root, text="Siguiente acción", command = lambda:[root.withdraw(), root.quit()])
    btn_terminar.grid(row=1, column=2)
    root.update()
    tk.mainloop()

def draw_graph_human_reordenacion(player1, player2, total_map):
    global riskMap
    # El grafo representa el continente de África en esta foto: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Risk_Game_Map_2004_Edition.png"
    
    root = tk.Tk()
    root.wm_title("Risk (continente África en forma de grafo)")
    root.wm_protocol('WM_DELETE_WINDOW', root.destroy)

    f = crear_dibujo_grafo(player1, player2, total_map)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    lab_inicial = tk.Label(root, text="ID de origen")
    lab_inicial.grid(row = 0, column = 1)
    entr_inicial = tk.Entry(root)
    entr_inicial.grid(row = 0, column = 2)
    lab_numero = tk.Label(root, text="Número de soldados que mover")
    lab_numero.grid(row = 0, column = 3)
    entr_numero = tk.Entry(root)
    entr_numero.grid(row = 0, column = 4)
    lab_objetivo = tk.Label(root, text="ID objetivo")
    lab_objetivo.grid(row = 0, column = 5)
    entr_objetivo = tk.Entry(root)
    entr_objetivo.grid(row = 0, column = 6)
    lab_continentes = tk.Label(root, text = "Europa: " + str(europa) + "\nAfrica = " + str(africa) + "\nSudamerica = " + str(sudamerica))
    lab_continentes.grid(row=1, column=0)

    btn_atacar = tk.Button(root, text = "Trasladar", command = lambda: reordenar_soldados(entr_inicial, entr_numero, entr_objetivo, player1, player2, total_map, canvas, root))
    btn_atacar.grid(row=1, column=1)
    btn_terminar = tk.Button(root, text="Terminar turno", command = lambda:[root.withdraw(), root.quit()])
    btn_terminar.grid(row=1, column=2)
    root.update()
    tk.mainloop()

def colocar_territorios(entr_territorio, entr_numero, player_humano, player_IA, total_map, lab_nsoldados, canvas, root):
    try:
        territorio = int(entr_territorio.get())
        soldados = int(entr_numero.get())
    except:
        print("Fallo en la lectura de id o de soldados, por favor asegurate de insertar números")

    player_humano.put_soldiers_human(total_map, territorio, soldados)
    plt.clf()
    f = crear_dibujo_grafo(player_humano, player_IA, total_map)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
    lab_nsoldados.config(text="Número de soldados que dispones: " + str(player1.get_nsoldiers()))
    root.update()

def reordenar_soldados(entr_inicial, entr_numero, entr_objetivo, player_humano, player_IA, total_map, canvas, root):
    try:
        inicial = int(entr_inicial.get())
        soldados = int(entr_numero.get())
        objetivo = int(entr_objetivo.get())
    except:
        print("Fallo en la lectura de id o de soldados, por favor asegurate de insertar números")

    player_humano.reordenacion_human(total_map, inicial, soldados, objetivo)
    plt.clf()
    f = crear_dibujo_grafo(player_humano, player_IA, total_map)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
    root.update()

def leer_ataque(entr_ataque, entr_objetivo, player_humano, player_IA, total_map, canvas, root):
    try:
        n_ataque = int(entr_ataque.get())
        objetivo = int(entr_objetivo.get())
    except:
        print("Fallo en la lectura de ids, por favor asegurate de insertar números")

    player_humano.attack_human(player_IA, total_map, n_ataque, objetivo)
    plt.clf()
    f = crear_dibujo_grafo(player_humano, player_IA, total_map)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
    root.update()

def crear_dibujo_grafo(player1, player2, total_map):
    player1_nodes = list(player1.get_nodesHolded().keys())
    player2_nodes = list(player2.get_nodesHolded().keys())
    total_nodes = list(total_map.keys())
    aux = list(set(player1_nodes) | set(player2_nodes))
    noplayer_nodes = list(set(aux) ^ set(total_nodes))
    
    f = plt.figure(figsize=(6,6))
    plt.axis('off')

    pos = nx.spring_layout(riskMap, seed = 888)
    labels = {}
    for n in total_nodes:
        string = "ID" + str(n) + "=" + str(total_map.get(n).get_soldiers())
        labels.setdefault(n, string)

    nx.draw_networkx_nodes(riskMap, pos, nodelist= player1_nodes, node_color="#F50707", node_size = 500,alpha = 0.7)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= player2_nodes, node_color="#07F507", node_size = 500,alpha = 0.7)
    nx.draw_networkx_nodes(riskMap, pos, nodelist= noplayer_nodes, node_color="#6E7A6E", node_size = 500, alpha = 0.7)
    nx.draw_networkx_edges(riskMap, pos, edge_color = "#8B938B", alpha = 0.5)
    nx.draw_networkx_labels(riskMap, pos, labels)

    return f

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
    # global norteamerica
    # global asia
    # global australia
    global list_cont

    list_cont = []
    list_cont.append(europa)
    list_cont.append(africa)
    list_cont.append(sudamerica)
    # list_cont.append(norteamerica)
    # list_cont.append(asia)
    # list_cont.append(australia)

    riskMap=nx.Graph()
    riskMap.add_nodes_from(range(1, max_territorios))
    riskMap.add_edges_from([(5,3), (5,2), (5,1), (3,2), (2,1), (2,6), (2,4), (6,1), (6,4), (5,8), (7,8), (7,9), (8,9), (8,10), (9,10), (5,17), (5,15), (3,15),
    (17,11), (17,13), (17,15), (13,16), (13,14), (13,15), (13,11), (15,16), (16,14), (11,12), (11,14), (12,14)])
    
    # , (10,20), (20,21), (20,26), (26,24), (26,19), (26,21), (21,24), (21,25),
    # (19,18), (19,24), (19,23), (18,23), (23,24), (23,22), (24,25), (25,22), (22,12), (27,16), (27,37), (27,33), (27,29), (27,28), (28,29), (28,34), (28,35), (28,37), (28,36), (29,33), (29,35),
    # (37,16), (37,36), (36,38), (36,30), (34,30), (34,31), (34,32), (32,31), (32,38), (38,30), (30,32), (39,42), (39,41), (42,41), (41,40), (40,35), (22,12)])

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

    player1.actualizar_heur()
    player2.actualizar_heur()
    
    draw_graph_IA(player1, player2, total_map)

    return player1, player2

if __name__ == '__main__':

    global total_map
    global riskMap

    n = 0
    errores = 0
    vict_player1 = 0
    vict_player2 = 0
    player1, player2 = initialize()

    binary = True      # Esta variable llevará de qué jugador es el turno, si es 0 sera del primero y si es uno del segundo.
    print("Escriba 1 si quieres establecer un limite de tiempo o 2 si quieres establecer un limite de simulaciones.")
    tipo = input()
    if tipo == "1":
        print("Escriba los segundos maximos de busqueda. Como orientacion en 30 segundos se realizan ~5000 simulaciones.")
    elif tipo == "2":
        print("Escriba las simulaciones maximas de busqueda. Como orientacion en 30 segundos se realizan ~5000 simulaciones.")
    else:
        print("Por favor escriba un 1 o un 2")
    
    limite = input()
    while True:
        try:
            limite = int(limite)
            print("Empieza la partida")
            break
        except:
            print("Por favor escriba un numero entero.")
            limite = input()
        
    while (len(player1.get_nodesHolded()) != 0)  and (len(player2.get_nodesHolded()) != 0):
        num_cont = 0
        sold_nuevos = 0
        if binary == True:
            player1.sold_continentes()
            draw_graph_human_putsoldiers(player1, player2, total_map)
            draw_graph_human_attack(player1, player2, total_map)
            draw_graph_human_reordenacion(player1, player2, total_map)
            binary = False

        else:
            player2.sold_continentes()
            player2.put_soldiers_in_territory(total_map)
            player2.attack_IA(player1, total_map, tipo, limite)
            player2.reordenacion(total_map)
            binary = True
    
        draw_graph_IA(player1, player2, total_map)
        
import random as r
import time
from math import sqrt, log
from node_tree import Node_Tree

class mctsAgent:
    def __init__(self):
        self.root = Node_Tree()

# en el estado se crea un riskmap que ese es el estado inicial. A partir de ahi se va desarrollando.
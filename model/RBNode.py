from model.Node import Node
RED = "RED"
BLACK = "BLACK"

class RBNode(Node):
    def __init__(self, key, data):
        super().__init__(key, data)
        
        self.color = RED #Un nodo recien creado es rojo.
        self.parent = None

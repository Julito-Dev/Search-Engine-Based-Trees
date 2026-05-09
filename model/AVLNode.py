from Node import Node

class AVLNode(Node):
    def __init__(self, key, data):
        super().__init__(key, data)
        
        self.height = 1 #Un nodo recien creado es una hoja, y su altura es 1
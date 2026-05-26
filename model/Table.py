from AVLTree import AVLTree
from RBTree import RBTree

class Table:
    def __init__(self, name, treeType = "AVL"):   #AVL por defecto
        """Crea una tabla que es respaldada por un arbol binario balanceado

        Args:
            name (String): Nombre de la tabla
            treeType (str): "AVL" o "RB". por defecto "AVL"
        """
        if treeType not in ("AVL","RB"):
            raise ValueError("El tipo de arbol debe ser 'AVL' o 'RB'")
        
        self.name = name
        self.treeType = treeType
        self._tree = AVLTree() if treeType == "AVL" else RBTree()

        
    def insert_row(self, key, data):
        """Inserta una fila en la tabla

        Args:
            key (Any): Clave Primaria ID
            data (dict): datos de la fila
        """
        self._tree.insert(key, data)
        
    def delete_row(self, key):
        """Elimina una fila por su ID

        Args:
            key (Any): ID del nodo a eliminar
        """
        self._tree.delete(key)
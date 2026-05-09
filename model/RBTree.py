from BST import BST
from RBNode import RBNode, RED, BLACK

class RBTree(BST):
    def __init__(self):
        self.NIL = RBNode(None, None)  # Nodo Hoja (Siempre negro)
        self.NIL.color = BLACK
        super().__init__(root=self.NIL)  # Árbol vacío apunta a NIL

    # ── Helpers ────────────────────────────────────────

    def _is_nil(self, node):
        """Verifica si un nodo es el nodo hoja NIL."""
        return node == self.NIL

    def _get_uncle(self, node):
        """Retorna el tio del nodo (hermano del padre)."""
        grandparent = node.parent.parent

        if node.parent == grandparent.left:
            return grandparent.right
        return grandparent.left

    # ── Rotaciones ─────────────────────────────────────

    def rotate_left(self, node):
        """Rota el subárbol a la izquierda.

        Args:
            node (RBNode): El nodo a rotar
        """
        new_root = node.right
        subtree = new_root.left

        # Rotación
        new_root.left = node
        node.right = subtree

        # Actualizar padres
        new_root.parent = node.parent
        node.parent = new_root

        if not self._is_nil(subtree):
            subtree.parent = node

        # Reconectar con el resto del árbol
        if new_root.parent is None:
            self.root = new_root
        elif node == new_root.parent.left:
            new_root.parent.left = new_root
        else:
            new_root.parent.right = new_root

    def rotate_right(self, node):
        """Rota el subárbol a la derecha.

        Args:
            node (RBNode): El nodo a rotar
        """
        new_root = node.left
        subtree = new_root.right

        # Rotación
        new_root.right = node
        node.left = subtree

        # Actualizar padres
        new_root.parent = node.parent
        node.parent = new_root

        if not self._is_nil(subtree):
            subtree.parent = node

        # Reconectar con el resto del árbol
        if new_root.parent is None:
            self.root = new_root
        elif node == new_root.parent.right:
            new_root.parent.right = new_root
        else:
            new_root.parent.left = new_root
    
    
    def insert(self, key, data):
        new_node = RBNode(key, data)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        
        #PASO 1 - Encontrar la posicion correcta
        parent = None
        current = self.root
        
        while not self._is_nil(current):
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                current.data = data  #Clave duplicada, solo actualiza la data
                return
        
        #Paso 2 - Conectar el nuevo nodo
        new_node.parent = parent
        if parent is None:
            self.root = new_node  #Arbol vacio
        elif key< parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        #PASO 3 - Si es la raiz, colorear de negro
        if new_node.parent is None:
            new_node.color = BLACK
            return
        
        #PASO 4 - Si no existe el abuelo, no existe ninguna violacion
        if new_node.parent.parent is None:
            return
        
        #PASO 5 - Ajustar el arbol
        self.fix_insert(new_node)
    
    def fix_insert(self, node):
        
        while node.parent and node.parent.parent == RED:
            uncle = self._get_uncle(node)
            
            
            #Para el lado izquierdo
            if node.parent == node.parent.parent.left:
                
                #Caso 1 - Tio rojo
                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent    # Sube al abuelo
            
                else:
                    #Caso 2 - rotacion izq-der, rotar para alinear
                    
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    
                    #Caso 3 - Nodos alineados, rotar y recolorear
                    
                    node.parent.color = BLACK
                    node.parent.paren.color = RED
                    self.rotate_right(node.parent.parent)  # Rotacion por el abuelo
                    
            #Lado derecho (Espejo)
            else:
                
                #Caso 1 - tio rojo 
                if uncle.color == RED:
                    node.parent = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent  # Sube al abuelo
                
                else:
                    #Caso 2
                    
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    
                    #Caso 3 
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.rotate_left(node.parent.parent) #Rotacion por el abuelo
        
        self.root.color = BLACK   #Raiz siempre negra                
    
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        
        v.parent = u.parent
    
    def _get_min_node(self, node):
        """Retorna el nodo con la clave minima del subárbol.

        Args:
            node (RBNode): Raiz del subárbol

        Returns:
            RBNode: El nodo con la clave minima
        """
        while not self._is_nil(node.left):
            node = node.left
        return node
    
    def delete(self, key):
        
        node = self._search_iterative(self.root, key)
        
        if self._is_nil(node) or node is None:
            return    #La clave no existe
        
        self._delete_node(self, node)
    
    def _delete_node(self, node):
        
        original_color = node.color
        fix_node = None
        
        #CASO 1 sin hijo izquierdo
        if self._is_nil(node.left):
            fix_node = node.right
            self._transplant(node, node.right)
        
        #CASO 2 sin hijo derecho
        elif self._is_nil(node.right):
            fix_node = node.left
            self._transplant(node, node.left)
        
        #CASO 3 dos hijos
        else:
            sucesor = self._get_min_node(node.right)
            original_color = sucesor.color
            fix_node = sucesor.right
            
            if sucesor.parent == node:
                fix_node.parent = sucesor
            else:
                self._transplant(sucesor, sucesor.right)
                sucesor.right = node.right
                sucesor.right.parent = sucesor
            
            self._transplant(node, sucesor)
            sucesor.left = node.left
            sucesor.left.parent = sucesor
            sucesor.color = node.color
        
        if original_color == BLACK:
            self.fix_delete(fix_node)  #Solo ajustar si se elimino un nodo negro
    
    def fix_delete(self, node):
        
        while node != self.root and node.color == BLACK:
            
            #Por la izquierda
            if node == node.parent.left:
                sibling = node.parent.right
                
                #Caso 1 Hermano rojo
                if sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.rotate_left(node.parent)
                    sibling = node.parent.right
                
                #Caso 2 hermano negro, sobrinos negros
                if sibling.left.color == BLACK and sibling.right.color == BLACK:
                    sibling.color = RED
                    node = node.parent   #SUBE EL PROBLEMA
                
                else:
                    if sibling.right.color ==BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self.rotate_right(sibling)
                        sibling = node.parent.right
                    
                    #CASO 4 hijo lejano rojo
                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.right.color = BLACK
                    self.rotate_left(node.parent)
                    node = self.root  #RESUELTO
                    
            
            #POR LA DERECHA (ESPEJO)
            else:
                sibling = node.parent.left
                
                #CASO 1 hermano rojo
                if sibling.color == RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self.rotate_right(node.parent)
                    sibling = node.parent.left
                
                #CASO 2 Hermano negro y sobrinos negros
                if sibling.right.color == BLACK and sibling.left.color == BLACK:
                    sibling.color = RED
                    node = node.parent   #Sube el problema
                
                else:
                    #CASO 3 hijo lejano negro, hijo cercano rojo 
                    if sibling.left.color == BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED  
                        self.rotate_left(sibling)
                        sibling = node.parent.left
                    
                    #CASO 4 hijo lejano rojo
                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.left.color = BLACK
                    self.rotate_right(node.parent)
                    node = self.root  #RESUELTO
                    
        node.color = BLACK   #  EL NODO FINAL SIEMPRE QUEDA NEGRO
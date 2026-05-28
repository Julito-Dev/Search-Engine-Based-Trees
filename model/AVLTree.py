from model.BST import BST
from model.AVLNode import AVLNode

class AVLTree(BST):
    def __init__(self):
        super().__init__(root=None)  # El árbol empieza vacío
    
    # ── Helpers de altura ──────────────────────────────
    
    def _get_height(self, node):
        """Retorna la altura del nodo, o 0 si es None."""
        if node is None:
            return 0
        return node.height
    
    def _update_height(self, node):
        """Recalcula la altura del nodo según sus hijos."""
        node.height = 1 + max(
            self._get_height(node.left),
            self._get_height(node.right)
        )
    
    def _get_balance(self, node):
        """Diferencia de altura izquierda - derecha.
           Si > 1 o < -1, el nodo está desbalanceado.
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def rotate_left(self, node):
        """Rota el subárbol a la izquierda.
    
        Args:
            node (AVLNode): El nodo desbalanceado (X en el diagrama)
        
        Returns:
            AVLNode: La nueva raíz del subárbol (Y en el diagrama)
        """
        new_root = node.right   # Y sube
        subtree  = new_root.left  # B se mueve

        # Rotación
        new_root.left = node    # X baja
        node.right = subtree    # B queda entre X e Y

        # Alturas — primero X (ahora es hijo), luego Y (ahora es padre)
        self._update_height(node)
        self._update_height(new_root)

        return new_root


    def rotate_right(self, node):
        """Rota el subárbol a la derecha.
        
        Args:
            node (AVLNode): El nodo desbalanceado (Y en el diagrama)
        
        Returns:
            AVLNode: La nueva raíz del subárbol (X en el diagrama)
        """
        new_root = node.left    # X sube
        subtree  = new_root.right  # B se mueve

        # Rotación
        new_root.right = node   # Y baja
        node.left = subtree     # B queda entre X e Y

        # Alturas — primero Y (ahora es hijo), luego X (ahora es padre)
        self._update_height(node)
        self._update_height(new_root)

        return new_root
    
    def rebalance(self, node):
        """Detecta el desbalance y aplica la rotacion correcta.

        Args:
            node (AVLNode): El nodo a revisar

        Returns:
            AVLNode: La nueva raiz del subárbol, ya balanceada
        """
        self._update_height(node)
        balance = self._get_balance(node)

        # CASO 1 — Left Left
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # CASO 2 — Left Right
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # CASO 3 — Right Right
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # CASO 4 — Right Left
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node  # Ya estaba balanceado, no hace nada
    
    def insert(self, key, data):
        """Inserta un nodo y rebalancea el árbol.

        Args:
            key (Any): La clave unica del nodo
            data (dict): La informacion del nodo
        """
        self.root = self._insert_recursive(self.root, key, data)
        self._notify() #NOTIFICA 


    def _insert_recursive(self, node, key, data):
        """Inserta recursivamente y rebalancea al regresar.

        Args:
            node (AVLNode): Nodo actual
            key (Any): Clave a insertar
            data (dict): Datos a insertar

        Returns:
            AVLNode: Raiz del subárbol ya balanceado
        """
        # PASO 1 — insert normal de BST
        if node is None:
            return AVLNode(key, data)  # Encontró el lugar, crea el nodo

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, data)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, data)
        else:
            node.data = data  # Clave duplicada — actualiza el data
            return node

        # PASO 2 — al regresar, rebalancea este nodo
        return self.rebalance(node)
    
    
    def _get_min_node(self, node):
        """Retorna el nodo con la clave minima del subárbol.
        Es el nodo más a la izquierda posible.
        
        Args:
            node (AVLNode): Raiz del subárbol
        
        Returns:
            AVLNode: El nodo con la clave minima
        """
        while node.left is not None:
            node = node.left
        return node
    
    def delete(self, key):
        """Elimina un nodo y rebalancea el arbol

        Args:
            key (Any): La clave unica del nodo a eliminar
        """
        self.root = self._delete_recursive(self.root, key)
        self._notify() #NOTIFICA
        
    
    def _delete_recursive(self, node, key):
        """Elimina recursivamente y rebalancea al retornar

        Args:
            node (AVLNode): Nodo actual
            key (Any): Clave a eliminar
        """
        # Clave no encontrada
        if node is None:
            return None
        
        # PASO 1 bajar hasta encontrar el nodo
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
            
        else:
            # CASO 1 El nodo a eliminar tiene 1 o 0 hijos
            if node.left is None:
                return node.right
            
            if node.right is None:
                return node.left
            
            #Caso 2 El nodo a eliminar tiene dos hijos
            sucesor = self._get_min_node(node.right) #Menor a la derecha
            node.key = sucesor.key  #Copia key 
            node.data = sucesor.data #Copia data
            node.right = self._delete_recursive(     #Elimina el sucesor
                node.right,
                sucesor.key
            )
            
        # PASO 2 Rebalancear
        return self.rebalance(node) 
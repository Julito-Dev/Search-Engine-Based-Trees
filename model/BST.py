from abc import ABC, abstractmethod

class BST(ABC):
    def __init__(self, root):
        self.root = root
    
    
    @abstractmethod
    def insert(self, key, data):
        """Permite a las hijas insertar un nodo bajo sus propias reglas.

        Args:
            key (Any): La clave unica del nodo
            data (dict): La informacion completa tiene estructura de diccionario  " Key : info " 
        """
        pass
    
    @abstractmethod
    def delete(self, key):
        """Permite a las hijas eliminar un nodo bajo sus propias reglas

        Args:
            key (Any): La clave unica del nodo
        """
        pass
    
    
    def search(self, key):
        """Busca un nodo especifico por su clave

        Args:
            key (Any): La clave unica del nodo

        Returns:
            node: Devuelve el nodo con la clave especificada
        """
        return self._search_iterative(
            self.root,
            key
        )
    
    
    
    def _search_recursive(self, node, key):
        """Busqueda recursiva (Se llama a si misma)
          Por si decidimos cambiar el tipo de busqueda.
            Si el arbol es muy profundo, puede fallar
        Args:
            node (Node): Un nodo de las clases AVLTree o RBTree 
            key (Any): La clave unica del nodo

        Returns:
            node: Retorna el nodo encontrado.
            None: Si la clave no existe en el arbol
        """
        if node is None:
            return None
        
        if key == node.key:
            return node
        
        if key < node.key:
            return self._search_recursive(
                node.left,
                key
            )
        
        return self._search_recursive(
            node.right,
            key
        )
        
    def _search_iterative(self, node, key):
        """Busqueda iterativa
           Es mucho mas eficiente en python

        Args:
            node (Node): Un nodo de las clases AVLTree o RBTree
            key (Any): La clave unica del nodo

        Returns:
            node: Nodo encontrado.
            None: Si la clave no existe en el arbol
        """
        
        while node is not None and node.key is not None:  #Si node es None, el puntero salio del arbol sin encontrar nada   /////////////// Frena en NIL
            
            if key == node.key:
                return node   # Si encontro la key, entonces retorna el nodo
            
            node = node.left if key < node.key else node.right  #Reemplaza por su hijo izquierdo o derecho segun la operacion
        return None  #La clave no existe en el arbol
    
    
    def inorder(self):
        """El metodo publico que usaran los hijos para ordenar los nodos

        Returns:
            List: Result es la lista final de los nodos que componen el arbol hasta el momento
        """
        result =[]
        
        self._inorder(
            self.root,
            result
        )   
        
        return result
    
    def _inorder(self, node, result):
        """Recorre todo el arbol y recolecta todos los nodos
           en orden ascendente de sus claves.

        Args:
            node (Node): Es un atributo propio de la recursion
            result (list): Una lista que sirve como acumuladora de los nodos ordenados ascendentemente
        """
        if node is not None and node.key is not None:   #IGNORA NIL
            self._inorder(
                node.left,
                result
            )

            result.append(
                (node.key, node.data)
            )

            self._inorder(
                node.right,
                result
            )
            
    def range_search(self, min_key, max_key):
        """Retorna todos los nodos cuya clave esta entre
           min_key < x < max_key

        Args:
            min_key (Any): Clave minima del rango
            max_key (Any): Clave maxima del rango
        """

        result = []
        self.range_recursive(self.root, min_key, max_key, result)
        return result

    def _range_recursive(self, node, min_key, max_key, result):
        """Recorre el arbol recolectando los nodos dentro del rango.

        Args:
            node (Node): Nodo actual
            min_key (Any): Clave Minima
            max_key (Any): Clave Maxima
            result (list): Acumulador de resultados
        """
        if node is None or node.key is None:
            return
        
        
        if min_key < node.key:
            self._range_recursive(node.left, min_key, max_key, result)
        
        
        if min_key <= node.key <= max_key:
            result.append((node.key, node.data))
        
        if max_key > node.key:
            self._range_recursive(node.right, min_key, max_key, result)
            

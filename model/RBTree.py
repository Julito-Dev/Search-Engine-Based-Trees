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
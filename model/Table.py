from AVLTree import AVLTree
from RBTree import RBTree


class Table:

    # ── Construccion ──────────────────────────────────────────────────────────

    def __init__(self, tree):
        """Initializes the table from an AVL or Red-Black tree.

        Args:
            tree (AVLTree | RBTree): The tree whose data will be represented.

        Raises:
            TypeError: If tree is not an instance of AVLTree or RBTree.
        """
        if not isinstance(tree, (AVLTree, RBTree)):
            raise TypeError("tree must be an instance of AVLTree or RBTree")

        self._tree = tree
        self._type = "AVL" if isinstance(tree, AVLTree) else "Red-Black"

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def tree_type(self):
        """str: Tree type ('AVL' or 'Red-Black')."""
        return self._type

    @property
    def node_count(self):
        """int: Number of nodes in the tree."""
        return len(self._tree.inorder())

    @property
    def height(self):
        """int: Height of the tree calculated from the root."""
        return self._compute_height(self._tree.root)

    @property
    def min_key(self):
        """Any | None: Minimum key in the tree (None if empty)."""
        inorder = self._tree.inorder()
        return inorder[0][0] if inorder else None

    @property
    def max_key(self):
        """Any | None: Maximum key in the tree (None if empty)."""
        inorder = self._tree.inorder()
        return inorder[-1][0] if inorder else None
    

    # ── Métodos auxiliares ───────────────────────────────────────────────────
    def _compute_height(self, node):
        """Recursively computes the height of a subtree."""
        if node is None:
            return 0
        if hasattr(node, "height"):          # AVLNode almacena la altura
            return node.height
        if hasattr(node, "key") and node.key is None:
            return 0                          
        return 1 + max(
            self._compute_height(node.left),
            self._compute_height(node.right),
        )
 
    def _balance_factor(self, node):
        """Returns the balance factor of an AVLNode (left height - right height)."""
        if node is None:
            return 0
        lh = node.left.height  if (node.left  and hasattr(node.left,  "height")) else 0
        rh = node.right.height if (node.right and hasattr(node.right, "height")) else 0
        return lh - rh
 
    def _is_nil(self, node):
        """Returns True if the node is the NIL sentinel of an RBTree."""
        return node is not None and getattr(node, "key", "sentinel") is None
 
    def _key_str(self, node):
        """Converts a child node reference to a readable string."""
        if node is None or self._is_nil(node):
            return "NIL"
        return str(node.key)
 
   # ── Extraccion de filas ───────────────────────────────────────────────────────
 
    def rows(self):
        """Extracts all rows from the tree in ascending key order.
 
        Returns:
            list[dict]: Each dict holds one node's information.
                        Common keys : 'key', 'data', 'left', 'right', 'inorder_pos'.
                        AVL adds    : 'height', 'balance'.
                        RB  adds    : 'color',  'parent'.
        """
        inorder = self._tree.inorder()   # [(key, data), …] ordenando ascendentemente
 
        result = []
        for pos, (key, data) in enumerate(inorder, start=1):
            node = self._tree.search(key)
            if node is None:
                continue
 
            row = {
                "key":        key,
                "data":       data,
                "left":       self._key_str(node.left),
                "right":      self._key_str(node.right),
                "inorder_pos": pos,
            }
 
            if self._type == "AVL":
                row["height"]  = getattr(node, "height", None)
                row["balance"] = self._balance_factor(node)
 
            else:  # Red-Black
                parent = getattr(node, "parent", None)
                row["color"]  = getattr(node, "color", None)
                row["parent"] = (
                    None if (parent is None or self._is_nil(parent))
                    else parent.key
                )
 
            result.append(row)
 
        return result
 
 
    # ── Summary ──────────────────────────────────────────────────────────────
 
    def summary(self):
        """Returns a dictionary with the tree's global metrics.
 
        Returns:
            dict: {'tree_type', 'node_count', 'height', 'min_key', 'max_key'}
        """
        return {
            "tree_type":  self.tree_type,
            "node_count": self.node_count,
            "height":     self.height,
            "min_key":    self.min_key,
            "max_key":    self.max_key,
        }
 
    # ── Search ───────────────────────────────────────────────────────────────
 
    def find(self, key):
        """Finds a node by key and returns its row as a dictionary.
 
        Args:
            key (Any): The key to search for.
 
        Returns:
            dict | None: The node's row, or None if not found.
        """
        for row in self.rows():
            if row["key"] == key:
                return row
        return None
 
    # ── Dunder ───────────────────────────────────────────────────────────────
 
    def __repr__(self):
        s = self.summary()
        return (
            f"Table(tree_type={s['tree_type']!r}, "
            f"node_count={s['node_count']}, "
            f"height={s['height']})"
        )
   
  
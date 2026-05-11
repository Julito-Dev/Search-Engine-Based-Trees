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

   
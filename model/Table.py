from AVLTree import AVLTree
from RBTree import RBTree
import json
import os
class Table:
    DATA_DIR = "data" #Carpeta donde viven los JSON
    def __init__(self, name, treeType = "AVL", load=False):   #AVL por defecto
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

        os.makedirs(self.DATA_DIR, exist_ok=True)   #Crea /data si no existia
    
    
    # PERSISTENCIA
    
    def _filepath(self):
        """Ruta del archivo JSON de esta tabla
        """
        return os.path.join(self.DATA_DIR, f"{self.name}.json")
    
    def _save(self):
        """Serializa la tabla completa a JSON
        """
        payload = {
            "table_name": self.name,
            "tree_type": self.treeType,
            "rows": [
                {"key": key, "data": data}
                for key, data in self._tree.inorder()
            ]
        }
    
    def _load(self):
        """Reconstruye ek arbol desde el archivo JSON
        """
        path = self._filepath()
        if not os.path.exists(path):
            return
        
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        for row in payload["rows"]:
            self._tree.insert(row["key"], row["data"])
    
    def _deleteFile(self):
        """Elimina el JSON al hacer droptable
        """
        path = self._filepath()
        if os.path.exists(path):
            os.remove(path)
            
        
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
        
    def update_row(self, key, data):
        """Actualiza los datos de una fila.
            Si la clave no existe, la inserta.

        Args:
            key (Any): La clave primaria del nodo a actualizar
            data (dict): Nuevos datos
        """
        self._tree.insert(key, data)
    
    def find(self, key):
        """Busca una fila por su ID

        Args:
            key (Any): La clave primaria ID
        """
        
        nodo = self._tree.search(key)
        if nodo is None:
            return None
        return {"key": nodo.key, "data": nodo.data}

    def get_all_rows(self):
        """Retorna todas las filas ordenadas de mayor a menor ID
        """
        return [
            {"key": key, "data": data}
            for key, data in self._tree.inorder()
        ]
    
    def summary(self):
        """Returns a dictionary with the tree's global metrics.
 
        Returns:
            dict: {'tree_type', 'node_count', 'height', 'min_key', 'max_key'}
        """
        all_rows = self.get_all_rows()
        return {
            "name": self.name,
            "tree_type":  self.treeType,
            "node_count": len(all_rows),
            "min_key":    all_rows[0]["key"] if all_rows else None ,
            "max_key":   all_rows[-1]["key"] if all_rows else None,
        }
    
    def __repr__(self):
        s = self.summary()
        return (
            f"Table(name = {s['name']!r}), "
            f"Tree_type={s['tree_type']!r}, "
            f"node_count={s['node_count']})"
        )
        
    def select_where(self, filtro):
        """Retorna las filas que cumplan el filtro.

        Args:
            filtro (callable): Lambda que recibe data y retorna bool.
                            ej: lambda data: data["edad"] > 25
        Returns:
            list[dict]: Filas que cumplen el filtro.
        """
        return [
            row for row in self.get_all_rows()
            if filtro(row["data"])
        ]
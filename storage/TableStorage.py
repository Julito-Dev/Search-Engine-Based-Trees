import json
import os

class TableStorage:
    def __init__(self, table_name, data_dir="data"):
        self.table_name = table_name
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    
    def filepath(self):
        """Ruta del JSON
        """

        return os.path.join(self.data_dir, f"{self.table_name}.json")
    
    
    def save(self, tree, treeType):
        """Serializa un arbol completo a JSON

        Args:
            tree (AVL , RB): El arbol a serializar
            treeType (String): "AVL" o "RB"
    
        """
        
        payload = {
            "table_name": self.table_name,
            "tree_type": treeType,
            "rows": [
                {"key": key, "data":data}
                for key, data in tree.inorder()
            ]
        }
        with open(self.filepath(), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        
    
    def load(self):
        """Lee el JSON y retorna las filas
        """
        path= self.filepath()
        if not os.path.exists(path):
            return None
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def delete(self):
        """Elimina el archivo JSON
        """
        path = self.filepath()
        if os.path.exists(path):
            os.remove(path)
        
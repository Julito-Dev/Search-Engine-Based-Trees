from model.AVLTree import AVLTree
from model.RBTree import RBTree
from storage.TableStorage import TableStorage
class Table:
    DATA_DIR = "data" #Carpeta donde viven los JSON
    def __init__(self, name, treeType = "AVL", schema = None, load=False):   #AVL por defecto
        """Crea una tabla que es respaldada por un arbol binario balanceado

        Args:
            name (String): Nombre de la tabla
            treeType (str): "AVL" o "RB". por defecto "AVL"
        """
        if treeType not in ("AVL","RB"):
            raise ValueError("El tipo de arbol debe ser 'AVL' o 'RB'")
        
        self.name = name
        self.treeType = treeType
        self.schema = schema  # Si es None, significa que no hay validacion
        self._tree = AVLTree() if treeType == "AVL" else RBTree()

        self._storage = TableStorage(name, self.DATA_DIR)
        if load:
            self._load()
    
    #SCHEMAS
    
    def _validate(self, data):
        """Si el Schema existe, entonces lo valida

        Args:
            data (dict): Datos que se van a validad

        Raises:
            ValueError: Si un campo fata, sobra o tiene un tipo de dato incorrecto
        """
        if self.schema is None:
            return #Acepta cualquier dict

        #Campos extra
        extra = set(data.keys()) - set(self.schema.keys())
        if extra:
            raise ValueError(f"Campos no permitidos: {extra}")
        
        #Campos obligatorios que faltan
        missing = set(self.schema.keys()) - set(data.keys())
        if missing:
            raise ValueError(f"Campos obligaotorios faltantes: {missing}")
        
        #Validar tipos
        for field, expected_type in self.schema.items():
            value = data[field]
            if not isinstance(value,expected_type):
                raise ValueError(
                    f"Campo '{field}' debe ser {expected_type.__name__}, "
                    f"se recibio {type(value).__name__}"
                )
    
    # PERSISTENCIA
        
    def _load(self):
        """Reconstruye el arbol desde el archivo JSON
        """
        payload = self._storage.load()
        if payload is None:
            return
        for row in payload["rows"]:
            self._tree.insert(row["key"], row["data"])
    
    def _deleteFile(self):
        """Elimina el JSON al hacer droptable
        """
        self._storage.delete()
            
        
    def insert_row(self, key, data):
        """Inserta una fila en la tabla
            Implementamos atomicidad (Si falla, revertimos el guardado)

        Args:
            key (Any): Clave Primaria ID
            data (dict): datos de la fila
        """
        try:
            self._tree.insert(key, data)
            self._storage.save(self._tree, self.treeType)
        except Exception as e:
            self._tree.delete(key) # REVERSION
            raise RuntimeError(f"Error, Insercion fallida, operacion reveritda {e}")
        
    def delete_row(self, key):
        """Elimina una fila por su ID
            Implementamos atomicidad, revierte si el guardado falla
        Args:
            key (Any): ID del nodo a eliminar
        """
        backup = self._tree.search(key)
        if backup is None:
            return
        
        backup_data = backup.data
        
        try:
            self._tree.delete(key)
            self._storage.save(self._tree, self.treeType)
        except Exception as e:
            self._tree.insert(key, backup_data) #REVERSION
            raise RuntimeError(f"DELETE fallid, operacion revertida: {e}")
   
        
    def update_row(self, key, data):
        """Actualiza los datos de una fila.
            Si la clave no existe, la inserta.
            Implementamos atomicidad, si el guardado falla, revierte

        Args:
            key (Any): La clave primaria del nodo a actualizar
            data (dict): Nuevos datos
        """
        actual = self._tree.search(key)
        backup_data = actual.data if actual else None
        
        try:
            self._tree.insert(key, data)
            self._storage.save(self._tree, self.treeType)
        except Exception as e:
            if backup_data is not None:
                self._tree.insert(key, backup_data) #Reversion al estado anterior
            else:
                self._tree.insert(key)   # ERA nuevo, revierte el insert
            raise RuntimeError(f"Update Fallido, operacion revertida {e}")
        
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
    
    def select_range(self, min_key, max_key):
        """Retor filas cuya clave este entre min_key y max_key
        Args:
            min_key (Any): Clave minima
            max_key (Any): Clave maxima
        """
        return[
            {"key": key, "data": data}
            for key, data in self._tree.range_search(min_key, max_key)
    
        ]
        
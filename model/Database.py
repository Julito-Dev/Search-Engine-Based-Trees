from Table import Table
import os
import json
class Database:
    def __init__(self, name):
        """Crea una base de datos que administra multiples tablas

        Args:
            name (String): Nombre de la base de datos.
        """
        self.name = name
        self._tables = {}  #Aqui se almacenaran las tablas
        self._load_all()
    
    
    def _load_all(self):
        """Lee /data y reconstruye todas las tablas al iniciar
        """
        
        data_dir = Table.DATA_DIR
        if not os.path.exists(data_dir):
            return
        
        for filename in os.listdir(data_dir):
            if filename.endswith(".json"):
                path = os.path.join(data_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                
                name = payload["table_name"]
                tree_type = payload["tree_type"]
                self._tables[name] = Table(
                    name=name,
                    treeType=tree_type,
                    load=True   #La tabla cargara desde JSON
                )
    
    def createTable(self, name, treeType="AVL"):
        """Crea una nueva tabla y se registra en la base de datos

        Args:
            name (String): Nombre de la tabla.
            treeType (String): "AVL" o "RB". por defecto "AVL"
    
        """
        if name in self._tables:
            raise ValueError(f'La tabla {name} ya existe.')
        
        self._tables[name] = Table(name=name, treeType= treeType)
        
    def dropTable(self, name):
        """Elimina una tabla de la base de datos.

        Args:
            name (String): Nombre de la tabla que se quiere eliminar
        """
        if name not in self._tables:
            raise KeyError(f'La tabla {name} no existe.')
        
        self._tables[name]._deleteFile()  #Borra el JSON
        del self._tables[name]
    
    def get_table(self, name):
        """Retorna un objeto de la clase tabla
        """
        
        if name not in self._tables:
            raise KeyError(f'La tabla {name} no existe')
        
        return self._tables[name]
    
    def list_tables(self):
        """Retorna todas los nombres de todas las tablas en la base de datos
        """
        return list(self._tables.keys())
    
    
    # HELPER PARA EL CRUD DE LA BASE DE DATOS
    def _getOnRaise(self, table_name):
            """Valida que la tabla existe y la retorna
            """
            if table_name not in self._tables:
                raise KeyError(f'La tabla {table_name} no existe')
            
            return self._tables[table_name]
        
        
    #CRUD
    
    def insert(self, table_name, key, data):
        """Inserta una fila en una tabla

        Args:
            table_name (String): Nombre de la tabla donde ocurrira la insercion
            key (Any): Calve primaria ID
            data (dict): Datos de la fila
        """
        self._getOnRaise(table_name).insert_row(key, data)
        
    def delete(self, table_name, key):
        """Elimina una fila de una tabla

        Args:
            table_name (String): Nombre de la tabla donde ocurrira la eliminacion
            key (Any): Clave primaria ID
        """
        self._getOnRaise(table_name).delete_row(key)
        
    def update(self, table_name, key, data):
        """Actualiza los datos de una fila en una tabla

        Args:
            table_name (String): Nombre de la tabla donde ocurrira la actualizacion
            key (Any): Clave primaria ID
            data (dict): Datos actualizados
        """
        self._getOnRaise(table_name).update_row(key, data)
    
    def find(self, table_name, key):
        """Busca una fila de una tabla por su clave ID

        Args:
            table_name (String): Nombre de la tabla donde ocurrira la busqueda
            key (Any): Clave primaria ID
        """
        return self._getOnRaise(table_name).find(key)
    
    
    def select_all(self, table_name):
        """Retorna todas las filas de una tabla

        Args:
            table_name (String): Nombre de la tabla donde ocurrira la seleccion
        """

        return self._getOnRaise(table_name).get_all_rows()
    
    def select_where(self, table_name, filtro):
        """Retorna las filas de una tabla que cumplen cierto filtro

        Args:
            table_name (String): El nombre de la tabla donde ocurrira la seleccion
            filtro (callable): Lambda sobre data. d["Presupuesto"]> 100000
        """
        return self._getOnRaise(table_name).select_where(filtro)
    
    
    def summary(self):
        """retorna un resumen de todas las tablas.
        """
        return {
            "database": self.name,
            "tables": len(self._tables),
            "table_info": {
                name: table.summary()
                for name, table in self._tables.items()
            }
        }
        
    def __repr__(self):
        return(
            f"Database(name={self.name!r}, "
            f"tables={list(self._tables.keys())}"
        )
        
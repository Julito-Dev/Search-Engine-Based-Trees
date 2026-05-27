from Table import Table


class Database:
    def __init__(self, name):
        """Crea una base de datos que administra multiples tablas

        Args:
            name (String): Nombre de la base de datos.
        """
        self.name = name
        self._tables = {}  #Aqui se almacenaran las tablas
    
    
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
        
        
    
    
    
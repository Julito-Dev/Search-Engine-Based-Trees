import csv
import os

class Dataloader:
    def __init__(self, db):
        """Carga datasets en la base de datos.
        """
        
        self.db = db
        
    def loadCSV(self, filepath, table_name):
        """Lee un CSV e inserta sus filas en una tabla existente.

        Args:
            filepath (String): Ruta del archivo CSV
            table_name (String): Tabla destino
        """
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Archivo no encontrado: '{filepath}'")
        
        # verifica si la tabla existe
        self.db._getOnRaise(table_name)
        
        inserted = 0
        skipped = 0
        errors = []
        
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                raise ValueError("El CSV no tiene encabezados.")
            
            key_field= reader.fieldnames[0] # La primera columna es la key
            
            for linenum, row in enumerate(reader, start=2):
                try:
                    raw_key = row[key_field]
                    key = self._cast(raw_key)
                    
                    #Data
                    data = {
                        field: self._cast(value)
                        for field, value in row.items()
                        if field != key_field
                    }
                    
                    self.db.insert(table_name, key, data)
                    inserted += 1
                
                except(ValueError, RuntimeError) as e:
                    errors.append(f"Linea {linenum}: {e}")
                    skipped += 1
                    
        return {"inserted":inserted, "skipped": skipped, "errors": errors}
    
    
    def _cast(self, value):
        """Convierte un String a int, float o Bool.

        Args:
            value (String): Valor a convertir
        """
        
        if value.lower()== "true": return True
        if value.lower()== "false": return False
        try: return int(value)
        except ValueError: pass
        try: return float(value)
        except ValueError: pass
        return value.strip()
    
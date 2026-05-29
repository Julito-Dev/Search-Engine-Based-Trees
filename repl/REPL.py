import json
import os
import sys
from model.Dataloader import Dataloader

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'model'))

from model.Database import Database
from repl.Parser import Parser

class REPL:
    def __init__(self, db_name ="mi_base"):
        self.db = Database(db_name)
        self.parser = Parser()
        self.loader = Dataloader(self.db)
    
    
    def run(self):
        print(f"Motor de Bases de datos - '{self.db.name}'")
        print("Escribe EXIT para salir, HELP para ver comandos. \n")
        
        while True:
            try:
                cmd = input(f"{self.db.name}> ").strip()
            
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo...")
                break
        
            if not cmd:
                continue
            
            try:
                op= self.parser.parse(cmd)
                self._execute(op)
            
            except(ValueError, KeyError) as e:
                print(f"Error: {e}")
                
    def _execute(self, op):
        action = op["action"]
        db = self.db
        
        if action == "exit":
            print("Hasta luego..")
            raise SystemExit
        
        elif action == "help":
            self._print_help()
            
        elif action == "list_tables":
            tables = db.list_tables()
            print("Tablas: ", tables if tables else "(Ninguna)")
        
        elif action == "summary":
            print(json.dumps(db.summary(), indent=2))
        
        elif action == "summary_table":
            print(json.dumps(db.get_table(op["table"]).summary(), indent=2))
        
        elif action == "create_table":
            db.createTable(op["table"], treeType=op["tree_type"])
            print(f"Tabla '{op['table']}' creada ({op['tree_type']}).")
            
        elif action == "drop_table":
            db.dropTable(op["table"])
            print(f"Tabla '{op['table']}' eliminada.")
        
        elif action == "insert":
            db.insert(op["table"], op["key"], op["data"])
            print(f"Fila {op['key']} insertada en '{op['table']}'.")
        
        elif action == "update":
            db.update(op["table"], op["key"], op["data"])
            print(f"Fila '{op['key']} actualizada en '{op['table']}'.")
        
        elif action == "find":
            row = db.find(op["table"], op["key"])
            print(row if row else "No encontrado")
        
        elif action == "select_all":
            rows = db.select_all(op["table"])
            self._print_rows(rows)
        
        elif action == "select_where":
            filtro = self._build_filter(op["field"], op["op"], op["value"])
            rows = db.select_where(op["table"], filtro)
            self._print_rows(rows)
        
        elif action == "select_range":
            rows = db.select_range(op["table"], op["min_key"], op["max_key"])
            self._print_rows(rows)
        
        elif action == "delete":
            db.delete(op["table"], op["key"])
            print(f"Fila {op['key']} eliminada de '{op['table']}'.")
        
        elif action == "load_csv":
            result = self.loader.loadCSV(op["filepath"], op["table"])
            print(f"Insertadas: {result['inserted']} filas.")
            if result["skipped"] > 0:
                print(f"Omitidas:  {result['skipped']} filas.")
            if result["errors"]:
                for e in result["errors"]:
                    print(f"  {e}")
        
    def _build_filter(self, field, op, value):
        """Construye una funcion lambda a partir del campo, operador y valor

        """
        ops = {
            "=": lambda d: d.get(field) == value,
            ">": lambda d: d.get(field) is not None and d.get(field) > value,
            "<": lambda d: d.get(field) is not None and d.get(field)< value,
            ">=": lambda d: d.get(field) is not None and d.get(field)>= value,
            "<=": lambda d: d.get(field) is not None and d.get(field) <= value,
        }
        return ops[op]
    
    def _print_rows(self, rows):
        if not rows:
            print("Sin resultados")
            return

        for row in rows:
            print(f"   [{row['key']}] {row['data']}")
        
    def _print_help(self):
        print("""
            Comandos disponibles:
            CREATE TABLE <nombre> <AVL|RB>
            DROP TABLE <nombre>
            LIST TABLES

            INSERT INTO <tabla> <key> {"campo": valor}
            SELECT * FROM <tabla>
            SELECT * FROM <tabla> WHERE <campo> = <valor>
            SELECT * FROM <tabla> WHERE <campo> > <valor>
            SELECT * FROM <tabla> WHERE <campo> < <valor>
            SELECT * FROM <tabla> WHERE key BETWEEN <min> AND <max>
            UPDATE <tabla> <key> {"campo": valor}
            DELETE FROM <tabla> <key>
            FIND <tabla> <key>

            SUMMARY
            SUMMARY <tabla>
            HELP
            EXIT
                    """)
import json
import re

class Parser:
    def parse(self, command):
        """Convierte un String en un dict con la operacion a ejecutar

        Args:
            command (String): Comando SQL like elegido por el usuario
        """
        
        cmd = command.strip()
        upper = cmd.upper()
        
        #COMANDOS
        
        if upper == "EXIT":
            return {"action": "exit"}
        
        if upper == "LIST TABLES":
            return {"action": "list_tables"}
        
        if upper == "SUMMARY":
            return {"action": "summary"}
        
        
        #SUMMARY <tabla>
        
        m = re.match(r"SUMMARY\s+(\w+)", cmd, re.IGNORECASE)
        if m:
            return {"action": "summary_table", "table": m.group(1)}

        # CREATE TABLE <nombre> <AVL|RB>
        m = re.match(r"CREATE\s+TABLE\s+(\w+)\s+(AVL|RB)", cmd, re.IGNORECASE)
        if m:
            return {"action": "create_table", "table": m.group(1), "tree_type": m.group(2).upper()}
    
        # INSERT INTO <tabla> <key> <json>
        
        m = re.match(r"INSERT\s+INTO\s+(\w+)\s+(\d+)\s+(\{.*\}))", cmd, re.IGNORECASE)
        
        if m:
            try:
                data = json.loads(m.group(3))
            
            except json.JSONDecodeError:
                raise ValueError("El JSON no es Valido.")
            return {"action": "insert", "table": m.group(1), "key": int(m.group(2)), "data":data}
        
        
        # DELETE FROM <from> <key>
        
        m = re.match(r"DELETE\s+FROM\s+(\w+)\s+(\d+)", cmd, re.IGNORECASE)
        
        if m:
            return {"action": "delete", "table": m.group(1), "key": int(m.group(2))}
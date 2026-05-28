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
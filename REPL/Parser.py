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
        
        
        
        
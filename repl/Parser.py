import json
import re

class Parser:
    def parse(self, command):
        """Convierte un String en un dict con la operacion a ejecutar.

        Args:
            command (String): Comando SQL-like escrito por el usuario.

        Returns:
            dict: Operación parseada.

        Raises:
            ValueError: Si el comando no se reconoce.
        """
        cmd   = command.strip()
        upper = cmd.upper()

        if upper == "EXIT":
            return {"action": "exit"}

        if upper == "HELP":
            return {"action": "help"}

        if upper == "LIST TABLES":
            return {"action": "list_tables"}

        if upper == "SUMMARY":
            return {"action": "summary"}

        # SUMMARY <tabla>
        m = re.match(r"SUMMARY\s+(\w+)$", cmd, re.IGNORECASE)
        if m:
            return {"action": "summary_table", "table": m.group(1)}

        # CREATE TABLE <nombre> <AVL|RB>
        m = re.match(r"CREATE\s+TABLE\s+(\w+)\s+(AVL|RB)$", cmd, re.IGNORECASE)
        if m:
            return {"action": "create_table", "table": m.group(1),
                    "tree_type": m.group(2).upper()}

        # DROP TABLE <nombre>
        m = re.match(r"DROP\s+TABLE\s+(\w+)$", cmd, re.IGNORECASE)
        if m:
            return {"action": "drop_table", "table": m.group(1)
            }
        
        # INSERT INTO <tabla> <key> <json>
        m = re.match(r"INSERT\s+INTO\s+(\w+)\s+(\d+)\s+(\{.*\})$", cmd, re.IGNORECASE)
        if m:
            try:
                data = json.loads(m.group(3))
            except json.JSONDecodeError:
                raise ValueError("El JSON no es valido.")
            return {"action": "insert", "table": m.group(1),
                    "key": int(m.group(2)), "data": data}

        # DELETE FROM <tabla> <key>
        m = re.match(r"DELETE\s+FROM\s+(\w+)\s+(\d+)$", cmd, re.IGNORECASE)
        if m:
            return {"action": "delete", "table": m.group(1),
                    "key": int(m.group(2))}

        # UPDATE <tabla> <key> <json>
        m = re.match(r"UPDATE\s+(\w+)\s+(\d+)\s+(\{.*\})$", cmd, re.IGNORECASE)
        if m:
            try:
                data = json.loads(m.group(3))
            except json.JSONDecodeError:
                raise ValueError("El JSON no es valido.")
            return {"action": "update", "table": m.group(1),
                    "key": int(m.group(2)), "data": data}

        # FIND <tabla> <key>
        m = re.match(r"FIND\s+(\w+)\s+(\d+)$", cmd, re.IGNORECASE)
        if m:
            return {"action": "find", "table": m.group(1),
                    "key": int(m.group(2))}

        # SELECT * FROM <tabla> WHERE key BETWEEN <min> AND <max>
        m = re.match(
            r"SELECT\s+\*\s+FROM\s+(\w+)\s+WHERE\s+key\s+BETWEEN\s+(\d+)\s+AND\s+(\d+)$",
            cmd, re.IGNORECASE)
        if m:
            return {"action": "select_range", "table": m.group(1),
                    "min_key": int(m.group(2)), "max_key": int(m.group(3))}

        # SELECT * FROM <tabla> WHERE <campo> >/</=/>=/<= <valor>
        m = re.match(
            r"SELECT\s+\*\s+FROM\s+(\w+)\s+WHERE\s+(\w+)\s*(>=|<=|>|<|=)\s*(.+)$",
            cmd, re.IGNORECASE)
        if m:
            return {"action": "select_where", "table": m.group(1),
                    "field": m.group(2), "op": m.group(3),
                    "value": self._cast(m.group(4).strip())}

        # SELECT * FROM <tabla>
        m = re.match(r"SELECT\s+\*\s+FROM\s+(\w+)$", cmd, re.IGNORECASE)
        if m:
            return {"action": "select_all", "table": m.group(1)}

        raise ValueError(f"Comando no reconocido: '{cmd}'")

    def _cast(self, value):
        """Convierte un string a int, float, bool o str."""
        if value.lower() == "true":  return True
        if value.lower() == "false": return False
        try: return int(value)
        except ValueError: pass
        try: return float(value)
        except ValueError: pass
        return value.strip('"').strip("'")
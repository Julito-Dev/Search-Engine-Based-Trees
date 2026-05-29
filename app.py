import os
import sys
import json

from flask import Flask, render_template, request, jsonify
# Asegura que el paquete model sea importable cuando se ejecuta desde la raíz del repositorio.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, "model"))

from model.Database import Database
from model.Dataloader import Dataloader

app = Flask(__name__, static_folder="static", template_folder="templates")
db = Database("mi_base")
loader = Dataloader(db)


def _is_tree_node(node):
    return node is not None and getattr(node, "key", None) is not None


def _build_ordered_nodes(root):
    ordered = []

    def recurse(node, depth):
        if not _is_tree_node(node):
            return
        recurse(node.left, depth + 1)
        ordered.append((node, depth))
        recurse(node.right, depth + 1)

    recurse(root, 0)
    return ordered


def _build_tree_layout(root):
    ordered = _build_ordered_nodes(root)
    nodes = []
    positions = {}
    margin_x = 100
    step_x = 120
    step_y = 100

    for index, (node, depth) in enumerate(ordered):
        node_id = str(node.key)
        x = margin_x + index * step_x
        y = 40 + depth * step_y
        color = getattr(node, "color", None)
        nodes.append({
            "id": node_id,
            "key": node.key,
            "data": node.data,
            "x": x,
            "y": y,
            "color": "red" if color == "RED" else "black"
        })
        positions[node_id] = {"x": x, "y": y}

    edges = []

    def recurse_edges(node):
        if not _is_tree_node(node):
            return
        node_id = str(node.key)
        if _is_tree_node(node.left):
            edges.append({"from": node_id, "to": str(node.left.key)})
        if _is_tree_node(node.right):
            edges.append({"from": node_id, "to": str(node.right.key)})
        recurse_edges(node.left)
        recurse_edges(node.right)

    recurse_edges(root)
    width = max(640, margin_x * 2 + len(ordered) * step_x)
    height = max(320, (max((depth for _, depth in ordered), default=0) + 1) * step_y + 80)

    return {
        "nodes": nodes,
        "edges": edges,
        "width": width,
        "height": height,
    }


def _table_info(table):
    return {
        "name": table.name,
        "tree_type": table.treeType,
        "summary": table.summary(),
        "rows": table.get_all_rows(),
        "tree": _build_tree_layout(table._tree.root)
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tables", methods=["GET"])
def list_tables():
    return jsonify({"tables": db.list_tables()})


@app.route("/api/create_table", methods=["POST"])
def create_table():
    payload = request.get_json(force=True)
    name = payload.get("name")
    tree_type = payload.get("tree_type", "AVL").upper()

    if not name:
        return jsonify({"error": "El nombre de la tabla es requerido."}), 400

    try:
        db.createTable(name, treeType=tree_type)
        return jsonify({"message": f"Tabla '{name}' creada.", "tables": db.list_tables()})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/insert", methods=["POST"])
def insert_row():
    payload = request.get_json(force=True)
    table_name = payload.get("table")
    key = payload.get("key")
    data = payload.get("data")

    if table_name is None or key is None or data is None:
        return jsonify({"error": "table, key y data son requeridos."}), 400

    try:
        db.insert(table_name, key, data)
        table = db.get_table(table_name)
        return jsonify({"message": "Fila insertada.", "table": _table_info(table)})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/delete", methods=["POST"])
def delete_row():
    payload = request.get_json(force=True)
    table_name = payload.get("table")
    key = payload.get("key")

    if table_name is None or key is None:
        return jsonify({"error": "table y key son requeridos."}), 400

    try:
        db.delete(table_name, key)
        table = db.get_table(table_name)
        return jsonify({"message": "Fila eliminada.", "table": _table_info(table)})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/find", methods=["POST"])
def find_row():
    payload = request.get_json(force=True)
    table_name = payload.get("table")
    key = payload.get("key")

    if table_name is None or key is None:
        return jsonify({"error": "table y key son requeridos."}), 400

    try:
        result = db.find(table_name, key)
        return jsonify({"result": result})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/table/<table_name>", methods=["GET"])
def table_info(table_name):
    try:
        table = db.get_table(table_name)
        return jsonify(_table_info(table))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 404

@app.route("/api/drop_table", methods=["POST"])
def drop_table():
    payload = request.get_json(force=True)
    name = payload.get("name")
    if not name:
        return jsonify({"error": "name es requerido."}), 400
    try:
        db.dropTable(name)
        return jsonify({"message": f"tabla '{name}' eliminada.",
                        "tables": db.list_tables()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/select_all", methods=["POST"])
def select_all():
    payload    = request.get_json(force=True)
    table_name = payload.get("table")
    if not table_name:
        return jsonify({"error": "table es requerido."}), 400
    try:
        rows = db.select_all(table_name)
        return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/select_where", methods=["POST"])
def select_where():
    payload    = request.get_json(force=True)
    table_name = payload.get("table")
    field      = payload.get("field")
    op         = payload.get("op")
    value      = payload.get("value")

    if not all([table_name, field, op, value is not None]):
        return jsonify({"error": "table, field, op y value son requeridos."}), 400

    ops = {
        "=":  lambda d: d.get(field) == value,
        ">":  lambda d: d.get(field) >  value,
        "<":  lambda d: d.get(field) <  value,
        ">=": lambda d: d.get(field) >= value,
        "<=": lambda d: d.get(field) <= value,
    }

    if op not in ops:
        return jsonify({"error": f"Operador '{op}' no válido."}), 400

    try:
        rows = db.select_where(table_name, ops[op])
        return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/select_range", methods=["POST"])
def select_range():
    payload    = request.get_json(force=True)
    table_name = payload.get("table")
    min_key    = payload.get("min_key")
    max_key    = payload.get("max_key")

    if not all([table_name, min_key is not None, max_key is not None]):
        return jsonify({"error": "table, min_key y max_key son requeridos."}), 400

    try:
        rows = db.select_range(table_name, min_key, max_key)
        return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/api/load_csv", methods=["POST"])
def load_csv():
    payload    = request.get_json(force=True)
    table_name = payload.get("table")
    filepath   = payload.get("filepath")

    if not table_name or not filepath:
        return jsonify({"error": "table y filepath son requeridos."}), 400

    try:
        result = loader.loadCSV(filepath, table_name)
        table  = db.get_table(table_name)
        return jsonify({
            "message":  f"Insertadas {result['inserted']} filas.",
            "inserted": result["inserted"],
            "skipped":  result["skipped"],
            "errors":   result["errors"],
            "table":    _table_info(table)
        })
    except (FileNotFoundError, KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

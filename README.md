# Motor de Base de Datos con Árboles Autobalanceados

Motor/gestor de base de datos que utiliza árboles AVL y Rojo-Negro como estructura de indexación y almacenamiento, con soporte para operaciones CRUD, consultas, persistencia en JSON, interfaz de línea de comandos (REPL) e interfaz web.

---

## Características

- Indexación con **AVL Tree** y **Red-Black Tree** implementados desde cero
- Operaciones CRUD con **atomicidad básica** por operación
- **Persistencia en JSON** — los datos sobreviven reinicios
- **Schema opcional** con validación de tipos (int, str, float, bool)
- **SELECT por rango** aprovechando la estructura del árbol — O(log n)
- **Carga de datasets CSV** con detección automática de tipos
- **REPL** con comandos SQL-like
- **Interfaz web** con visualización del árbol en tiempo real (Flask)

---

## Estructura del proyecto

```
Search Engine/
├── main.py                    ← punto de entrada del REPL
├── app.py                     ← servidor Flask (interfaz web)
│
├── model/
│   ├── Node.py                ← nodo base
│   ├── AVLNode.py             ← nodo AVL (agrega height)
│   ├── RBNode.py              ← nodo RB (agrega color y parent)
│   ├── BST.py                 ← clase abstracta base
│   ├── AVLTree.py             ← árbol AVL autobalanceado
│   ├── RBTree.py              ← árbol Rojo-Negro autobalanceado
│   ├── Table.py               ← tabla respaldada por un árbol
│   ├── Database.py            ← gestor de múltiples tablas
│   ├── Dataloader.py          ← carga de datasets CSV
│   └── storage/
│       └── TableStorage.py    ← persistencia en JSON
│
├── repl/
│   ├── Parser.py              ← parser de comandos SQL-like
│   └── REPL.py                ← loop de comandos
│
├── static/
│   ├── app.js                 ← lógica de la interfaz web
│   └── style.css              ← estilos
│
├── templates/
│   └── index.html             ← interfaz web
│
├── datasets/                  ← CSVs para cargar (crear manualmente)
└── data/                      ← JSONs generados automáticamente
```

---

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd "Search Engine"

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Instalar dependencias
pip install flask
```

---

## Uso — REPL

```bash
python main.py
```

### Comandos disponibles

```sql
-- Tablas
CREATE TABLE <nombre> <AVL|RB>
DROP TABLE <nombre>
LIST TABLES
SUMMARY
SUMMARY <tabla>

-- CRUD
INSERT INTO <tabla> <key> {"campo": valor}
UPDATE <tabla> <key> {"campo": valor}
DELETE FROM <tabla> <key>
FIND <tabla> <key>

-- Consultas
SELECT * FROM <tabla>
SELECT * FROM <tabla> WHERE <campo> = <valor>
SELECT * FROM <tabla> WHERE <campo> > <valor>
SELECT * FROM <tabla> WHERE <campo> < <valor>
SELECT * FROM <tabla> WHERE key BETWEEN <min> AND <max>

-- Dataset
LOAD <archivo.csv> INTO <tabla>
LOAD <archivo.csv> INTO <tabla> AUTOID

-- Otros
HELP
EXIT
```

### Ejemplo de sesión

```
mi_base> CREATE TABLE usuarios AVL
Tabla 'usuarios' creada (AVL).

mi_base> INSERT INTO usuarios 1 {"nombre": "Ana", "edad": 25}
Fila 1 insertada en 'usuarios'.

mi_base> SELECT * FROM usuarios WHERE edad > 20
  [1] {'nombre': 'Ana', 'edad': 25}

mi_base> LOAD datasets/datos.csv INTO usuarios
Insertadas: 50 filas.

mi_base> EXIT
Hasta luego.
```

---

## Uso — Interfaz Web

```bash
python app.py
```

Abrir el navegador en:

```
http://localhost:5000
```

### Funcionalidades de la interfaz

- Crear y eliminar tablas (AVL o RB)
- Insertar, actualizar, eliminar y buscar filas
- Filtrar por campo y operador (`>`, `<`, `=`, `>=`, `<=`)
- Buscar por rango de claves
- Cargar datasets CSV
- Visualización del árbol en tiempo real

---

## Schema de tabla

```python
# Con schema — valida tipos al insertar
db.createTable("productos", treeType="AVL", schema={
    "nombre": str,
    "precio": float,
    "stock":  int,
    "activo": bool
})

# Sin schema — acepta cualquier dict
db.createTable("libre", treeType="AVL")
```

Tipos disponibles: `str`, `int`, `float`, `bool`

---

## Complejidad temporal

| Operación | Complejidad |
|---|---|
| insert | O(log n) |
| delete | O(log n) |
| search | O(log n) |
| inorder | O(n) |
| select_where | O(n) |
| select_range | O(log n + k) |

Donde `n` es el número de nodos y `k` es el número de resultados en el rango.

---

## Complejidad espacial

| Estructura | Espacio |
|---|---|
| AVLTree | O(n) |
| RBTree | O(n) |
| select_range | O(k) |
| inorder | O(n) |

---

## Atomicidad

Cada operación CRUD garantiza atomicidad básica — si el guardado en disco falla, el árbol en memoria se revierte al estado anterior:

```
insert → falla al guardar → delete (rollback)
delete → falla al guardar → insert (rollback)
update → falla al guardar → insert con data anterior (rollback)
```

---

## Persistencia

Los datos se guardan automáticamente en `/data` después de cada operación. Al reiniciar, `Database` carga todas las tablas desde los archivos JSON.

```
data/
  usuarios.json
  productos.json
```

Formato del archivo:

```json
{
  "table_name": "usuarios",
  "tree_type": "AVL",
  "schema": {"nombre": "str", "edad": "int"},
  "rows": [
    {"key": 1, "data": {"nombre": "Ana", "edad": 25}},
    {"key": 2, "data": {"nombre": "Luis", "edad": 30}}
  ]
}
```

---

## Carga de datasets CSV

El CSV debe tener encabezados en la primera fila. La primera columna se usa como clave primaria:

```csv
id,nombre,edad,ciudad
1,Ana,25,Bogota
2,Luis,30,Medellin
```

```
mi_base> LOAD datasets/usuarios.csv INTO usuarios
Insertadas: 2 filas.
```

Si el CSV no tiene una columna de ID, usar `AUTOID`:

```
mi_base> LOAD datasets/datos.csv INTO tabla AUTOID
```

---

## API REST (Flask)

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/tables` | Listar tablas |
| POST | `/api/create_table` | Crear tabla |
| POST | `/api/drop_table` | Eliminar tabla |
| POST | `/api/insert` | Insertar fila |
| POST | `/api/delete` | Eliminar fila |
| POST | `/api/find` | Buscar por key |
| POST | `/api/select_all` | Todas las filas |
| POST | `/api/select_where` | Filtrar filas |
| POST | `/api/select_range` | Rango de keys |
| POST | `/api/load_csv` | Cargar CSV |
| GET | `/api/table/<name>` | Info + árbol |

---

## Principios de diseño

- **SOLID** — cada clase tiene una sola responsabilidad
- **Separación de capas** — model / repl / static / templates
- **Delegación** — Table delega persistencia a TableStorage
- **Abstracción** — BST define el contrato, AVLTree y RBTree lo implementan

---

## Autores
Julian David Paez Ortega 20251020165
Sergio Andres Diaz Cuervo 20251020166
Brayan David Santos Alvarez 20251020157



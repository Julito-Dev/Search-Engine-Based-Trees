# Motor de Base de Datos sobre Árboles Balanceados

Motor de base de datos en memoria indexado mediante árboles binarios balanceados AVL y Rojinegro. Soporta dos modos de uso: una interfaz web  y una CLI interactiva. Los datos se persisten automáticamente en archivos JSON.


## Requisitos

- Python 3.9+
- Flask

```bash
pip install flask
```



## Ejecución

### Interfaz web

```bash
python app.py
```

Abre el navegador en `http://localhost:5000`.

### CLI interactiva (

```bash
python -m repl.REPL
```


## Comandos disponibles (REPL)

### Gestión de tablas

```sql
CREATE TABLE productos AVL
CREATE TABLE usuarios RB
LIST TABLES
DROP TABLE productos
```

### Insertar y modificar filas

```sql
INSERT INTO productos 1 {"nombre": "Teclado", "precio": 45.9}
INSERT INTO productos 2 {"nombre": "Mouse", "precio": 19.99}
UPDATE productos 2 {"nombre": "Mouse Pro", "precio": 34.99}
DELETE FROM productos 2
```

### Consultas

```sql
SELECT * FROM productos
FIND productos 1
SELECT * FROM productos WHERE precio > 30
SELECT * FROM productos WHERE key BETWEEN 1 AND 3
```

### Métricas y utilidades

```sql
SUMMARY
SUMMARY productos
HELP
EXIT
```

---

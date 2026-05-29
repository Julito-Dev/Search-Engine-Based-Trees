const statusBox = document.getElementById("status-box");
const tableSelect = document.getElementById("table-select");
const rowsTable = document.getElementById("rows-table");
const treeInfo = document.getElementById("tree-info");
const treeSvg = document.getElementById("tree-svg");
let activeTable = null;

const showStatus = (text, error = false) => {
  statusBox.textContent = text;
  statusBox.style.background = error ? "#fee2e2" : "#eef2ff";
  statusBox.style.color = error ? "#991b1b" : "#1e3a8a";
  statusBox.style.borderColor = error ? "#fecaca" : "#c7d2fe";
};

const fetchTables = async () => {
  const response = await fetch("/api/tables");
  const data = await response.json();
  tableSelect.innerHTML = "";

  if (!data.tables || data.tables.length === 0) {
    tableSelect.innerHTML = "<option value=\"\">(No hay tablas)</option>";
    activeTable = null;
    showStatus("Crea una tabla para comenzar.");
    clearTree();
    return;
  }

  data.tables.forEach((name, index) => {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    tableSelect.appendChild(option);
    if (index === 0) activeTable = name;
  });

  if (!activeTable) activeTable = data.tables[0];
  tableSelect.value = activeTable;
  loadTable(activeTable);
};

const loadTable = async (tableName) => {
  if (!tableName) {
    showStatus("Selecciona una tabla válida.", true);
    return;
  }

  const response = await fetch(`/api/table/${tableName}`);
  const payload = await response.json();

  if (payload.error) {
    showStatus(payload.error, true);
    return;
  }

  activeTable = tableName;
  renderTableInfo(payload);
  renderRows(payload.rows);
  renderTree(payload.tree);
  showStatus(`Tabla activa: ${tableName} (${payload.tree_type})`);
};

const renderTableInfo = (table) => {
  treeInfo.innerHTML = `
    <div><strong>Nombre:</strong> ${table.name}</div>
    <div><strong>Tipo:</strong> ${table.tree_type}</div>
    <div><strong>Filas:</strong> ${table.summary.node_count}</div>
    <div><strong>Min key:</strong> ${table.summary.min_key ?? "-"}</div>
    <div><strong>Max key:</strong> ${table.summary.max_key ?? "-"}</div>
  `;
};

const renderRows = (rows) => {
  if (!rows || rows.length === 0) {
    rowsTable.innerHTML = "<p>No hay filas registradas.</p>";
    return;
  }

  const table = document.createElement("table");
  const header = document.createElement("thead");
  const body = document.createElement("tbody");

  // Encabezados (Key + cada campo del data)
  const fields = Object.keys(rows[0].data);
  header.innerHTML = `
    <tr>
      <th>key</th>
      ${fields.map(f => `<th>${f}</th>`).join("")}
    </tr>
    `;
  
  //filas
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.key}</td>
      ${fields.map(f => `<td>${row.data[f] ?? "-"}</td>`).join("")}
    `;
    body.appendChild(tr);
  });

  table.appendChild(header)
  table.appendChild(body)
  rowsTable.innerHTML = "";
  rowsTable.appendChild(table)
};

const clearTree = () => {
  treeSvg.innerHTML = "";
  treeSvg.setAttribute("viewBox", "0 0 800 320");
  treeInfo.innerHTML = "";
  rowsTable.innerHTML = "";
};

const renderTree = (tree) => {
  if (!tree || !tree.nodes || tree.nodes.length === 0) {
    clearTree();
    treeSvg.innerHTML = "<text x=20 y=40 fill='#374151'>El árbol está vacío.</text>";
    return;
  }

  treeSvg.innerHTML = "";
  treeSvg.setAttribute("viewBox", `0 0 ${tree.width} ${tree.height}`);

  tree.edges.forEach((edge) => {
    const from = tree.nodes.find((n) => n.id === edge.from);
    const to   = tree.nodes.find((n) => n.id === edge.to);
    if (!from || !to) return;

    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", from.x);
    line.setAttribute("y1", from.y + 20);
    line.setAttribute("x2", to.x);
    line.setAttribute("y2", to.y - 20);
    line.setAttribute("class", "edge-line");
    treeSvg.appendChild(line);
  });

  tree.nodes.forEach((node) => {
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", node.x);
    circle.setAttribute("cy", node.y);
    circle.setAttribute("r", 24);
    circle.setAttribute("class", "node-circle");
    circle.setAttribute("fill", node.color === "red" ? "#ef4444" : "#111827");
    treeSvg.appendChild(circle);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", node.x);
    text.setAttribute("y", node.y + 5);
    text.setAttribute("class", "node-label");
    text.textContent = node.key;
    treeSvg.appendChild(text);
  });
};

const postAction = async (url, body, successText) => {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const payload = await response.json();

  if (payload.error) {
    showStatus(payload.error, true);
    return null;
  }

  showStatus(successText);
  return payload;
};

const setupForms = () => {

  // ── Crear tabla ──────────────────────────────────
  document.getElementById("create-table-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name     = document.getElementById("new-table-name").value.trim();
    const treeType = document.getElementById("new-table-type").value;
    if (!name) { showStatus("El nombre de tabla es obligatorio.", true); return; }

    const payload = await postAction("/api/create_table", { name, tree_type: treeType }, `Tabla '${name}' creada.`);
    if (payload) {
      await fetchTables();
      tableSelect.value = name;
      loadTable(name);
      document.getElementById("new-table-name").value = "";
    }
  });

  // ── Eliminar tabla ───────────────────────────────
  document.getElementById("drop-table-btn").addEventListener("click", async () => {
    if (!activeTable) { showStatus("Selecciona una tabla.", true); return; }
    if (!confirm(`¿Eliminar tabla '${activeTable}'?`)) return;

    const payload = await postAction("/api/drop_table", { name: activeTable }, `Tabla '${activeTable}' eliminada.`);
    if (payload) {
      activeTable = null;
      await fetchTables();
    }
  });

  // ── Insertar ─────────────────────────────────────
  document.getElementById("insert-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla antes de insertar.", true); return; }

    const key = Number(document.getElementById("insert-key").value);
    let data;
    try { data = JSON.parse(document.getElementById("insert-data").value.trim()); }
    catch { showStatus("JSON inválido en los datos.", true); return; }

    const payload = await postAction("/api/insert", { table: activeTable, key, data }, "Fila insertada.");
    if (payload) {
      renderTableInfo(payload.table);
      renderRows(payload.table.rows);
      renderTree(payload.table.tree);
      document.getElementById("insert-key").value  = "";
      document.getElementById("insert-data").value = "";
    }
  });

  // ── Actualizar ───────────────────────────────────
  document.getElementById("update-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla antes de actualizar.", true); return; }

    const key = Number(document.getElementById("update-key").value);
    let data;
    try { data = JSON.parse(document.getElementById("update-data").value.trim()); }
    catch { showStatus("JSON inválido en los datos.", true); return; }

    const payload = await postAction("/api/insert", { table: activeTable, key, data }, `Fila ${key} actualizada.`);
    if (payload) {
      renderTableInfo(payload.table);
      renderRows(payload.table.rows);
      renderTree(payload.table.tree);
      document.getElementById("update-key").value  = "";
      document.getElementById("update-data").value = "";
    }
  });

  // ── Eliminar fila ────────────────────────────────
  document.getElementById("delete-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla antes de eliminar.", true); return; }

    const key     = Number(document.getElementById("delete-key").value);
    const payload = await postAction("/api/delete", { table: activeTable, key }, "Fila eliminada.");
    if (payload) {
      renderTableInfo(payload.table);
      renderRows(payload.table.rows);
      renderTree(payload.table.tree);
      document.getElementById("delete-key").value = "";
    }
  });

  // ── Buscar fila ──────────────────────────────────
  document.getElementById("find-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla antes de buscar.", true); return; }

    const key      = Number(document.getElementById("find-key").value);
    const response = await postAction("/api/find", { table: activeTable, key }, "Búsqueda realizada.");
    if (response && response.result) {
      showStatus(`Encontrado: ${JSON.stringify(response.result)}`);
    } else if (response && response.result === null) {
      showStatus("No se encontró la fila.", true);
    }
  });

  // ── Filtrar WHERE ────────────────────────────────
  document.getElementById("select-where-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla.", true); return; }

    const field = document.getElementById("where-field").value.trim();
    const op    = document.getElementById("where-op").value;
    const raw   = document.getElementById("where-value").value.trim();
    const value = (raw === "" || isNaN(raw)) ? raw : Number(raw);

    const payload = await postAction("/api/select_where",
      { table: activeTable, field, op, value },
      "Filtro aplicado."
    );
    if (payload) renderRows(payload.rows);
  });

  // ── Rango de claves ──────────────────────────────
  document.getElementById("select-range-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla.", true); return; }

    const min_key = parseInt(document.getElementById("range-min").value);
    const max_key = parseInt(document.getElementById("range-max").value);

    const payload = await postAction("/api/select_range",
      { table: activeTable, min_key, max_key },
      `Rango [${min_key}, ${max_key}] aplicado.`
    );
    if (payload) renderRows(payload.rows);
  });

  // ── Cargar CSV ───────────────────────────────────
  document.getElementById("load-csv-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!activeTable) { showStatus("Selecciona una tabla.", true); return; }

    const filepath = document.getElementById("csv-filepath").value.trim();
    const payload  = await postAction("/api/load_csv",
      { table: activeTable, filepath },
      "CSV cargado."
    );
    if (payload) {
      showStatus(payload.message + (payload.skipped ? ` (${payload.skipped} omitidas)` : ""));
      renderTableInfo(payload.table);
      renderRows(payload.table.rows);
      renderTree(payload.table.tree);
      document.getElementById("csv-filepath").value = "";
    }
  });

  // ── Cambio de tabla activa ───────────────────────
  tableSelect.addEventListener("change", () => {
    const selected = tableSelect.value;
    if (selected) loadTable(selected);
  });
};

window.addEventListener("DOMContentLoaded", async () => {
  setupForms();
  await fetchTables();
});
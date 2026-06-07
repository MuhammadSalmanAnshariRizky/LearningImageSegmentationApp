/**
 * Script untuk Live Code Notebook - Edge-Based Segmentation
 */

let edgeCellCount = 0;
let edgeEditors = {};
let edgeImagePath = "";

// 1. Inisiasi
document.addEventListener("DOMContentLoaded", function () {
  loadEdgeState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in edgeEditors) {
            if (edgeEditors[id]) edgeEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("edgeNotebook");
  if (notebook) observer.observe(notebook);
});

// 2. Local Storage
function saveEdgeState() {
  const cellsData = [];
  for (const id in edgeEditors) {
    cellsData.push({
      id: id,
      code: edgeEditors[id].getValue(),
      output: document.getElementById(`edge-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_Edge", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_Edge", edgeImagePath);
  const fileListElem = document.getElementById("edgeFileList");
  if (fileListElem)
    localStorage.setItem("currentImageName_Edge", fileListElem.innerHTML);
  localStorage.setItem("cellCount_Edge", edgeCellCount);
}

function loadEdgeState() {
  const savedCells = JSON.parse(localStorage.getItem("notebookCells_Edge"));
  const savedPath = localStorage.getItem("currentImagePath_Edge");
  const savedImageUI = localStorage.getItem("currentImageName_Edge");
  const savedCellCount = localStorage.getItem("cellCount_Edge");

  if (savedPath && savedImageUI) {
    edgeImagePath = savedPath;
    document.getElementById("edgeFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) edgeCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) =>
      createEdgeCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Tambah Cell
function addEdgeCell() {
  edgeCellCount++;
  const defaultCode = `import cv2
import numpy as np
import os

# 1. MEMBACA CITRA & KONVERSI WARNA
image = cv2.imread('....')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 2. GRAYSCALE
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. EDGE DETECTION (OPERATOR CANNY)
edges = cv2.Canny(gray, 100, 200)

# 4. EDGE LINKING (MORPHOLOGICAL CLOSING)
kernel = np.ones((3, 3), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# 5. MENCARI KONTUR
contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 6. REGION EXTRACTION
mask = np.zeros(gray.shape, dtype=np.uint8)
cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)

# 7. MENYIMPAN HASIL
cv2.imwrite(os.path.join(output_dir, "citra_asli.jpg"), image)
cv2.imwrite(os.path.join(output_dir, "edge_detection.jpg"), edges)
cv2.imwrite(os.path.join(output_dir, "edge_linking.jpg"), closed)
cv2.imwrite(os.path.join(output_dir, "region_extraction.jpg"), mask)

print("Proses segmentasi berbasis tepi selesai dijalankan!")
print(f"Jumlah kontur objek yang terdeteksi: {len(contours)}")`;

  createEdgeCellDOM(
    edgeCellCount,
    defaultCode,
    "Output Edge-Based muncul di sini...",
  );
  saveEdgeState();
}

function createEdgeCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("edgeNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "edge-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">Edge In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runEdgeCell(${id})" title="Run"><i class="fa-solid fa-play"></i></button>
                <button class="btn-icon delete" onclick="deleteEdgeCell(${id})" title="Hapus"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>
        <textarea id="edge-editor-${id}"></textarea>
        <div id="edge-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`edge-editor-${id}`),
    {
      mode: "python",
      theme: "dracula",
      lineNumbers: true,
      lineWrapping: true,
    },
  );
  editor.setValue(codeText);
  editor.setSize("100%", "auto");
  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveEdgeState();
  });
  edgeEditors[id] = editor;
}

// 4. Run Cell
function runEdgeCell(id) {
  const code = edgeEditors[id].getValue();
  const outputBox = document.getElementById(`edge-output-${id}`);
  outputBox.innerHTML = "⏳ Running Edge-Based Segmentation...";

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: edgeImagePath }),
  })
    .then((res) => res.json())
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3"><pre>${data.output}</pre></div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${data.before_image ? renderEdgeImgCard("Citra Asli", "/static/results/citra_asli.jpg") : ""}
                    ${renderEdgeImgCard("Edge Detection", "/static/results/edge_detection.jpg")}
                    ${renderEdgeImgCard("Edge Linking", "/static/results/edge_linking.jpg")}
                    ${renderEdgeImgCard("Hasil Segmentasi", "/static/results/region_extraction.jpg")}
                </div>
            </div>`;
      saveEdgeState();
    });
}

function renderEdgeImgCard(title, src) {
  const t = Date.now();
  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.8rem;">${title}</h6>
        <img src="${src}?t=${t}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 120px; cursor: pointer;"
             data-bs-toggle="modal" data-bs-target="#edgeImageModal" 
             onclick="openEdgeModal('${src}?t=${t}')">
    </div>`;
}

// 5. Utilitas
function openEdgeModal(src) {
  document.getElementById("edgeModalImage").src = src;
}
function deleteEdgeCell(id) {
  document.getElementById("edge-cell-" + id).remove();
  delete edgeEditors[id];
  saveEdgeState();
}
function triggerEdgeUpload() {
  document.getElementById("edgeFileInput").click();
}

function handleEdgeUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("image", file);
  fetch("/upload-image", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      edgeImagePath = data.path;
      document.getElementById("edgeFileList").innerHTML =
        `<li><i class="fa-solid fa-file-image me-2 text-danger"></i> ${file.name}</li>`;
      saveEdgeState();
    });
}

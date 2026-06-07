/**
 * Script untuk Live Code Notebook - Region Growing Segmentation
 */

let regionCellCount = 0;
let regionEditors = {};
let regionImagePath = "";

// 1. Inisiasi Lifecycle
document.addEventListener("DOMContentLoaded", function () {
  loadRegionState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in regionEditors) {
            if (regionEditors[id]) regionEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("regionNotebook");
  if (notebook) observer.observe(notebook);
});

// 2. Sinkronisasi State Ke Local Storage
function saveRegionState() {
  const cellsData = [];
  for (const id in regionEditors) {
    cellsData.push({
      id: id,
      code: regionEditors[id].getValue(),
      output: document.getElementById(`region-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_Region", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_Region", regionImagePath);
  const fileListElem = document.getElementById("regionFileList");
  if (fileListElem)
    localStorage.setItem("currentImageName_Region", fileListElem.innerHTML);
  localStorage.setItem("cellCount_Region", regionCellCount);
}

function loadRegionState() {
  const savedCells = JSON.parse(localStorage.getItem("notebookCells_Region"));
  const savedPath = localStorage.getItem("currentImagePath_Region");
  const savedImageUI = localStorage.getItem("currentImageName_Region");
  const savedCellCount = localStorage.getItem("cellCount_Region");

  if (savedPath && savedImageUI) {
    regionImagePath = savedPath;
    document.getElementById("regionFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) regionCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) =>
      createRegionCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Pembuatan Cell DOM
function addRegionCell() {
  regionCellCount++;
  const defaultCode = `import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. MEMBACA CITRA GRAYSCALE
img = cv2.imread('_____', cv2.IMREAD_GRAYSCALE)
if img is None:
    print("Gambar tidak ditemukan!")
    exit()

# 2. MENENTUKAN SEED POINT & THRESHOLD TOLERANSI
seed = (270, 220)
threshold = 31

# 3. ALGORITMA CORE PROCESS REGION GROWING
rows, cols = img.shape
segmented = np.zeros((rows, cols), np.uint8)
visited = np.zeros((rows, cols), np.bool_)
seed_value = int(img[seed])
queue = [seed]

while len(queue) > 0:
    x, y = queue.pop(0)
    if visited[x, y]:
        continue
    visited[x, y] = True
    
    if abs(int(img[x, y]) - seed_value) <= threshold:
        segmented[x, y] = 255
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = x + dx
                ny = y + dy
                # Proteksi batas dimensi matriks citra
                if 0 <= nx < rows and 0 <= ny < cols:
                    queue.append((nx, ny))

# 4. MENYIMPAN FISIK MATRIKS CITRA HASIL UNTUK WEB PREVIEW
cv2.imwrite(os.path.join(output_dir, "citra_asli_region.jpg"), img)
cv2.imwrite(os.path.join(output_dir, "hasil_region_growing.jpg"), segmented)

# 5. MENYIMPAN VISUALISASI TITIK SEED POINT MENGGUNAKAN MATPLOTLIB
plt.figure(figsize=(5, 4))
plt.imshow(img, cmap='gray')
plt.scatter(seed[1], seed[0], color='red', s=50, label='Seed Point')
plt.title('Posisi Titik Seed')
plt.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "visualisasi_seed.jpg"))
plt.close()

print("Proses Segmentasi Region Growing Selesai Dijalankan!")
print(f"Intensitas Nilai Piksel Seed: {seed_value}")`;

  createRegionCellDOM(
    regionCellCount,
    defaultCode,
    "Output Region Growing muncul di sini...",
  );
  saveRegionState();
}

function createRegionCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("regionNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "region-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">Region In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runRegionCell(${id})" title="Run"><i class="fa-solid fa-play"></i></button>
                <button class="btn-icon delete" onclick="deleteRegionCell(${id})" title="Hapus"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>
        <textarea id="region-editor-${id}"></textarea>
        <div id="region-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`region-editor-${id}`),
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
    saveRegionState();
  });
  regionEditors[id] = editor;
}

// 4. Integrasi Backend Compilation
function runRegionCell(id) {
  const code = regionEditors[id].getValue();
  const outputBox = document.getElementById(`region-output-${id}`);
  outputBox.innerHTML = "⏳ Processing Region Growing Compiling...";

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: regionImagePath }),
  })
    .then((res) => res.json())
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3"><pre>${data.output}</pre></div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${data.before_image ? renderRegionImgCard("Citra Asli", "/static/results/citra_asli_region.jpg") : ""}
                    ${renderRegionImgCard("Letak Seed Point", "/static/results/visualisasi_seed.jpg")}
                    ${renderRegionImgCard("Hasil Region Growing", "/static/results/hasil_region_growing.jpg")}
                </div>
            </div>`;
      saveRegionState();
    });
}

function renderRegionImgCard(title, src) {
  const t = Date.now();
  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.8rem;">${title}</h6>
        <img src="${src}?t=${t}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 120px; cursor: pointer;"
             data-bs-toggle="modal" data-bs-target="#regionImageModal" 
             onclick="openRegionModal('${src}?t=${t}')">
    </div>`;
}

// 5. Utilitas Sidebar Workspace
function openRegionModal(src) {
  document.getElementById("regionModalImage").src = src;
}
function deleteRegionCell(id) {
  document.getElementById("region-cell-" + id).remove();
  delete regionEditors[id];
  saveRegionState();
}
function triggerRegionUpload() {
  document.getElementById("regionFileInput").click();
}

function handleRegionUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("image", file);
  fetch("/upload-image", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      regionImagePath = data.path;
      document.getElementById("regionFileList").innerHTML =
        `<li><i class="fa-solid fa-file-image me-2 text-danger"></i> ${file.name}</li>`;
      saveRegionState();
    });
}

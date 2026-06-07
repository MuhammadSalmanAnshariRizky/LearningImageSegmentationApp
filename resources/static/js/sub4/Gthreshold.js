/**
 * Script untuk Live Code Notebook - Global Thresholding (Iterative Selection)
 */

let thresholdCellCount = 0;
let thresholdEditors = {};
let thresholdImagePath = "";

// 1. Inisiasi Observer
document.addEventListener("DOMContentLoaded", function () {
  loadThresholdState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in thresholdEditors) {
            if (thresholdEditors[id]) thresholdEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("thresholdNotebook");
  if (notebook) observer.observe(notebook);
});

// 2. Local Storage Management
function saveThresholdState() {
  const cellsData = [];
  for (const id in thresholdEditors) {
    cellsData.push({
      id: id,
      code: thresholdEditors[id].getValue(),
      output: document.getElementById(`threshold-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_Threshold", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_Threshold", thresholdImagePath);
  const fileListElem = document.getElementById("thresholdFileList");
  if (fileListElem)
    localStorage.setItem("currentImageName_Threshold", fileListElem.innerHTML);
  localStorage.setItem("cellCount_Threshold", thresholdCellCount);
}

function loadThresholdState() {
  const savedCells = JSON.parse(
    localStorage.getItem("notebookCells_Threshold"),
  );
  const savedPath = localStorage.getItem("currentImagePath_Threshold");
  const savedImageUI = localStorage.getItem("currentImageName_Threshold");
  const savedCellCount = localStorage.getItem("cellCount_Threshold");

  if (savedPath && savedImageUI) {
    thresholdImagePath = savedPath;
    document.getElementById("thresholdFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) thresholdCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) =>
      createThresholdCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Tambah Lembar Kerja Cell
function addThresholdCell() {
  thresholdCellCount++;
  const defaultCode = `import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. MEMBACA CITRA GRAYSCALE
img = cv2.imread('_____', cv2.IMREAD_GRAYSCALE)
if img is None:
    print("Gambar tidak ditemukan!")
    exit()

# 2. MENENTUKAN THRESHOLD AWAL
T = np.mean(img)

# 3. MELAKUKAN ITERATIVE THRESHOLD SELECTION
iteration = 0
while True:
    G1 = img[img > T]
    G2 = img[img <= T]
    if len(G1) == 0 or len(G2) == 0:
        break
    m1 = np.mean(G1)
    m2 = np.mean(G2)
    T_new = (m1 + m2) / 2
    iteration += 1
    if abs(T - T_new) < 0.5:
        break
    T = T_new

iterative_threshold = T_new

# 4. MELAKUKAN SEGMENTASI CITRA
_, segmented = cv2.threshold(img, iterative_threshold, 255, cv2.THRESH_BINARY)

# 5. MENGHITUNG HISTOGRAM
hist = cv2.calcHist([img], [0], None, [256], [0, 256])

# 6. MENYIMPAN MATRIKS HASIL KE DIREKTORI STATIS BACKEND
cv2.imwrite(os.path.join(output_dir, "citra_grayscale.jpg"), img)
cv2.imwrite(os.path.join(output_dir, "hasil_segmentasi.jpg"), segmented)

# 7. GENERATE GRAFIK HISTOGRAM DAN SAVE FISIK
plt.figure(figsize=(6, 4))
plt.plot(hist, color='blue')
plt.axvline(iterative_threshold, color='red', linestyle='--')
plt.title('Histogram Citra')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "grafik_histogram.jpg"))
plt.close()

print( "Proses Global Thresholding Selesai!" )
print(f"Nilas Ambang Batas Otomatis (T): {iterative_threshold:.2f}")
print(f"Total Iterasi Komputasi: {iteration}")`;

  createThresholdCellDOM(
    thresholdCellCount,
    defaultCode,
    "Output Global Thresholding muncul di sini...",
  );
  saveThresholdState();
}

function createThresholdCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("thresholdNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "threshold-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">Threshold In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runThresholdCell(${id})" title="Run"><i class="fa-solid fa-play"></i></button>
                <button class="btn-icon delete" onclick="deleteThresholdCell(${id})" title="Hapus"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>
        <textarea id="threshold-editor-${id}"></textarea>
        <div id="threshold-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`threshold-editor-${id}`),
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
    saveThresholdState();
  });
  thresholdEditors[id] = editor;
}

// 4. Eksekusi Kompilasi Matriks
function runThresholdCell(id) {
  const code = thresholdEditors[id].getValue();
  const outputBox = document.getElementById(`threshold-output-${id}`);
  outputBox.innerHTML = "⏳ Running Global Thresholding Selection...";

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: thresholdImagePath }),
  })
    .then((res) => res.json())
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3"><pre>${data.output}</pre></div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${data.before_image ? renderThresholdImgCard("Citra Grayscale", "/static/results/citra_grayscale.jpg") : ""}
                    ${renderThresholdImgCard("Histogram Citra", "/static/results/grafik_histogram.jpg")}
                    ${renderThresholdImgCard("Hasil Segmentasi", "/static/results/hasil_segmentasi.jpg")}
                </div>
            </div>`;
      saveThresholdState();
    });
}

function renderThresholdImgCard(title, src) {
  const t = Date.now();
  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.8rem;">${title}</h6>
        <img src="${src}?t=${t}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 120px; cursor: pointer;"
             data-bs-toggle="modal" data-bs-target="#thresholdImageModal" 
             onclick="openThresholdModal('${src}?t=${t}')">
    </div>`;
}

// 5. Utilitas File Upload & Management
function openThresholdModal(src) {
  document.getElementById("thresholdModalImage").src = src;
}
function deleteThresholdCell(id) {
  document.getElementById("threshold-cell-" + id).remove();
  delete thresholdEditors[id];
  saveThresholdState();
}
function triggerThresholdUpload() {
  document.getElementById("thresholdFileInput").click();
}

function handleThresholdUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("image", file);
  fetch("/upload-image", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      thresholdImagePath = data.path;
      document.getElementById("thresholdFileList").innerHTML =
        `<li><i class="fa-solid fa-file-image me-2 text-danger"></i> ${file.name}</li>`;
      saveThresholdState();
    });
}

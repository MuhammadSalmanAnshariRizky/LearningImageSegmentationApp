/**
 * Script untuk Live Code Notebook - Thresholding (Citra Biner)
 */

let thresholdCellCount = 0;
let thresholdEditors = {};
let thresholdImagePath = "";

// ==========================================
// 1. INISIASI & INTERSECTION OBSERVER
// ==========================================
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
  if (notebook) {
    observer.observe(notebook);
  }
});

// ==========================================
// 2. LOCAL STORAGE (SIMPAN & MUAT DATA)
// ==========================================
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
  if (fileListElem) {
    localStorage.setItem("currentImageName_Threshold", fileListElem.innerHTML);
  }
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

  if (savedCellCount) {
    thresholdCellCount = parseInt(savedCellCount);
  }

  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) => {
      createThresholdCellDOM(cellData.id, cellData.code, cellData.output);
    });
  }
}

// ==========================================
// 3. TAMBAH CELL & RENDER DOM
// ==========================================
function addThresholdCell() {
  thresholdCellCount++;

  // Template Kode Rumpang untuk Materi Thresholding
  const defaultCode = `import cv2
import numpy as np
import os

# =====================================
# BACA GAMBAR GRAYSCALE
# =====================================
# Pastikan nama file sesuai dengan yang di-upload!
img = cv2.imread('uploads/.....', cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Gambar tidak ditemukan!")
else:
    # =====================================
    # UKURAN CITRA
    # =====================================
    M, N = img.shape

    # =====================================
    # HITUNG NILAI THRESHOLD
    # T = jumlah seluruh piksel / (M x N)
    # =====================================
    # Lengkapi variabel di bawah ini:
    total_pixel = np.sum(.....)
    T = total_pixel / (..... * .....)

    # =====================================
    # PROSES THRESHOLDING
    # Jika piksel > T maka jadikan 255 (putih), selain itu 0 (hitam)
    # =====================================
    threshold_img = np.where(img > ....., 255, 0).astype(np.uint8)

    # =====================================
    # SIMPAN HASIL
    # =====================================
    save_path = os.path.join(output_dir, "hasil_threshold.jpg")
    cv2.imwrite(save_path, threshold_img)

    # =====================================
    # OUTPUT
    # =====================================
    print("Threshold berhasil dibuat!")
    print(f"Ukuran citra: {M} x {N}")
    print(f"Nilai Threshold: {T:.2f}")`;

  const defaultOutput = `<span class="text-muted">> Output threshold akan muncul di sini...</span>`;

  createThresholdCellDOM(thresholdCellCount, defaultCode, defaultOutput);
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
                <button class="btn-icon run" onclick="runThresholdCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteThresholdCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
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

  setTimeout(() => {
    editor.refresh();
  }, 10);

  editor.on("change", function (cm) {
    cm.setSize(null, "auto");
    saveThresholdState();
  });

  thresholdEditors[id] = editor;
}

// ==========================================
// 4. JALANKAN KODE (RUN CELL)
// ==========================================
function runThresholdCell(id) {
  if (!thresholdEditors[id]) return;

  const code = thresholdEditors[id].getValue();
  const outputBox = document.getElementById(`threshold-output-${id}`);

  outputBox.innerHTML = `<span class="text-warning font-monospace">⏳ Menjalankan threshold...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      code: code,
      image_path: thresholdImagePath,
    }),
  })
    .then(async (res) => {
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        console.error("Bukan JSON:", text);
        throw new Error(text);
      }
    })
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3">
                    <pre class="text-success font-monospace mb-0">${data.output}</pre>
                </div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${
                      data.before_image
                        ? `
                        <div class="image-card text-center border p-2 rounded-3 bg-white">
                            <h6 class="fw-bold text-secondary mb-2" style="font-size:0.9rem;">Gambar Asli (Grayscale)</h6>
                            <img src="${data.before_image}" class="result-image preview-image img-fluid rounded" 
                                 style="max-height: 150px; cursor: pointer;"
                                 data-bs-toggle="modal" data-bs-target="#thresholdImageModal" 
                                 onclick="openThresholdModal('${data.before_image}')">
                        </div>
                    `
                        : ""
                    }
                    
                    ${
                      data.after_image
                        ? `
                        <div class="image-card text-center border p-2 rounded-3 bg-white">
                            <h6 class="fw-bold text-secondary mb-2" style="font-size:0.9rem;">Hasil Biner</h6>
                            <img src="${data.after_image}" class="result-image preview-image img-fluid rounded" 
                                 style="max-height: 150px; cursor: pointer;"
                                 data-bs-toggle="modal" data-bs-target="#thresholdImageModal" 
                                 onclick="openThresholdModal('${data.after_image}')">
                        </div>
                    `
                        : ""
                    }
                </div>
            </div>
        `;
      saveThresholdState();
    })
    .catch((err) => {
      console.error(err);
      outputBox.innerHTML = `<pre style="color:#ef4444;" class="font-monospace">Error: ${err.message}</pre>`;
      saveThresholdState();
    });
}

// ==========================================
// 5. MANAJEMEN MODAL, UPLOAD & HAPUS CELL
// ==========================================
function openThresholdModal(src) {
  const modalImg = document.getElementById("thresholdModalImage");
  if (modalImg) modalImg.src = src;
}

function deleteThresholdCell(id) {
  const cellElem = document.getElementById("threshold-cell-" + id);
  if (cellElem) cellElem.remove();
  delete thresholdEditors[id];
  saveThresholdState();
}

function triggerThresholdUpload() {
  const fileInput = document.getElementById("thresholdFileInput");
  if (fileInput) fileInput.click();
}

function handleThresholdUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("image", file);

  // Menggunakan path relatif agar stabil
  fetch("/upload-image", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      thresholdImagePath = data.path;

      const fileListElem = document.getElementById("thresholdFileList");
      if (fileListElem) {
        fileListElem.innerHTML = `
                <li>
                    <i class="fa-solid fa-file-image me-2 text-primary"></i>
                    ${file.name}
                </li>
            `;
      }
      saveThresholdState();
    })
    .catch((err) => {
      alert("Gagal mengupload citra.");
    });
}

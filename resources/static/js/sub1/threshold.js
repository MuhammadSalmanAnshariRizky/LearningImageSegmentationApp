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
    observer.observe(notebook.closest(".notebook-wrapper"));
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

  const defaultCode = `import cv2
import numpy as np
import os

# 1. MEMBACA CITRA GRAYSCALE
# tulis nama file dari gambar yang akan diproses
image = cv2.imread('.....', cv2.IMREAD_GRAYSCALE)

# 2. MENGHITUNG NILAI THRESHOLD
# tuliskan 'np.mean' untuk menghitung rata-rata intensitas piksel
threshold = ....(image)

# Tampilkan nilai threshold yang telah dihitung.
# Tuliskan nama variabel yang menyimpan nilai threshold.
print("Nilai Threshold:", ...)

# 3. MELAKUKAN THRESHOLDING
# Lengkapi parameter pertama dengan variabel yang menyimpan citra grayscale.
# Lengkapi parameter kedua dengan variabel yang menyimpan nilai threshold.
_, binary_image = cv2.threshold(
    ...,
    ...,
    255,
    cv2.THRESH_BINARY
)

# 4. MENYIMPAN HASIL
# Lengkapi dengan variabel yang menyimpan hasil citra biner (binary image).
cv2.imwrite(
    os.path.join(output_dir, "hasil_threshold.jpg"),
    ...
)

# 5. MENAMPILKAN INFORMASI
print("Thresholding berhasil dilakukan!")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;
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
            <span class="text-muted small fw-bold">In [${id}]:</span>
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

  setTimeout(() => editor.refresh(), 10);

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

  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Sedang memproses kodemu...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: thresholdImagePath }),
  })
    .then(async (res) => {
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        throw new Error(text);
      }
    })
    .then((data) => {
      if (data.error || (data.output && data.output.includes("Traceback"))) {
        outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>❌ Ups! Ada kesalahan:</strong><pre class="mt-2 text-danger">${data.error || data.output}</pre></div>`;
      } else {
        let outputHTML = `
            <div class="text-success font-monospace mb-3">
                <strong>✅ Hebat! Hasil konversi:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        if (data.before_image)
          outputHTML += createThresholdImageCard(
            "Gambar Asli",
            data.before_image,
          );
        if (data.after_image)
          outputHTML += createThresholdImageCard(
            "Hasil Biner",
            data.after_image,
          );

        // Fallback jika backend mengirim array images
        if (data.images && Array.isArray(data.images)) {
          data.images.forEach((img) => {
            outputHTML += createThresholdImageCard(img.title, img.url);
          });
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveThresholdState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
      saveThresholdState();
    });
}

function createThresholdImageCard(title, srcUrl) {
  return `
      <div class="image-card text-center border p-2 rounded-3 bg-white shadow-sm" style="width: fit-content;">
          <h6 class="fw-bold text-secondary mb-2" style="font-size:0.85rem;">${title}</h6>
          <img src="${srcUrl}" class="result-image preview-image img-fluid rounded" 
               style="max-height: 140px; cursor: pointer; object-fit: contain;"
               data-bs-toggle="modal" data-bs-target="#imageModal" 
               onclick="openThresholdModal('${srcUrl}')">
      </div>
    `;
}

// ==========================================
// 5. MANAJEMEN MODAL, UPLOAD & HAPUS CELL
// ==========================================
function openThresholdModal(src) {
  const modalImg = document.getElementById("modalImage");
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
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_grayscale" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("thresholdFileList").innerHTML = `
        <div class="text-center text-muted mt-3 small">
            <i class="fa-solid fa-spinner fa-spin me-2"></i>Mengunggah...
        </div>
    `;

    fetch("/upload-image", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        thresholdImagePath = data.path;

        document.getElementById("thresholdFileList").innerHTML = `
        <div class="image-preview-card mt-3">
            <div class="img-wrapper">
                <img src="${imageSrc}" class="preview-img" alt="Preview File" style="max-width:100%; border-radius:8px;">
            </div>
            <div class="file-name-text mt-2 small text-truncate" title="${data.filename}">
                <i class="fa-solid fa-file-image me-1 text-primary"></i>
                ${data.filename}
            </div>
        </div>
    `;
        saveThresholdState();
      })
      .catch((err) => {
        document.getElementById("thresholdFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };
  reader.readAsDataURL(originalFile);
}

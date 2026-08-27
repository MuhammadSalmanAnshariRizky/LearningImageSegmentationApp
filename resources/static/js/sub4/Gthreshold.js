/**
 * Script untuk Live Code Notebook - Global Thresholding (Iterative Selection) - TANPA MATPLOTLIB
 */

let globalThresholdCellCount = 0;
let globalThresholdEditors = {};
let globalThresholdImagePath = "";

// 1. Inisiasi Observer
document.addEventListener("DOMContentLoaded", function () {
  loadGlobalThresholdState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in globalThresholdEditors) {
            if (globalThresholdEditors[id]) globalThresholdEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("globalThresholdNotebook");
  if (notebook) observer.observe(notebook);
});

// 2. Local Storage Management
function saveGlobalThresholdState() {
  const cellsData = [];
  for (const id in globalThresholdEditors) {
    cellsData.push({
      id: id,
      code: globalThresholdEditors[id].getValue(),
      output: document.getElementById(`globalthreshold-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_GlobalThreshold", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_GlobalThreshold", globalThresholdImagePath);
  const fileListElem = document.getElementById("globalThresholdFileList");
  if (fileListElem)
    localStorage.setItem("currentImageName_GlobalThreshold", fileListElem.innerHTML);
  localStorage.setItem("cellCount_GlobalThreshold", globalThresholdCellCount);
}

function loadGlobalThresholdState() {
  const savedCells = JSON.parse(
    localStorage.getItem("notebookCells_GlobalThreshold"),
  );
  const savedPath = localStorage.getItem("currentImagePath_GlobalThreshold");
  const savedImageUI = localStorage.getItem("currentImageName_GlobalThreshold");
  const savedCellCount = localStorage.getItem("cellCount_GlobalThreshold");

  if (savedPath && savedImageUI) {
    globalThresholdImagePath = savedPath;
    document.getElementById("globalThresholdFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) globalThresholdCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) =>
      createGlobalThresholdCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Tambah Lembar Kerja Cell
function addGlobalThresholdCell() {
  globalThresholdCellCount++;

  // KODE PYTHON TANPA MATPLOTLIB
  const defaultCode = `import cv2
import numpy as np
import os

# 1. MEMBACA CITRA GRAYSCALE
# Tuliskan nama file gambar yang kamu unggah (misal: 'gambar.jpg') 
# lalu tuliskan 'cv2.imread' dan ' cv2.IMREAD_GRAYSCALE' untuk membaca sebagai citra grayscale
img = cv2....('....', cv2....)

# 2. ITERATIVE THRESHOLD SELECTION
# Tuliskan 'np.mean' pada numpy (np) untuk mencari rata-rata intensitas awal citra
T = np....(img)
iteration = 0

while True:
    # Membagi piksel menjadi dua kelompok berdasarkan Threshold (T)
    G1 = img[img > T]
    G2 = img[img <= T]
    
    # Menghindari pembagian kosong
    if len(G1) == 0 or len(G2) == 0:
        break
        
    # Tuliskan 'np.mean' untuk menghitung rata-rata dari masing-masing kelompok
    m1 = np....(G1)
    m2 = np....(G2)
    
    # Menghitung Threshold baru
    T_new = (m1 + m2) / 2
    iteration += 1
    
    # Kondisi berhenti jika nilai T sudah stabil
    if abs(T - T_new) < 0.5:
        break
    
    T = T_new

global_threshold_val = T_new

# 3. HASIL SEGMENTASI (THRESHOLDING)
# Tuliskan 'cv2.threshold' dan 'cv2.THRESH_BINARY_INV' agar objek utama menjadi area putih (255)
_, segmented = cv2....(img, global_threshold_val, 255, cv2....)

# 4. MEMBERSIHKAN MASK (CLOSING)
# Tuliskan 'cv2.getStructuringElement' dan 'cv2.MORPH_ELLIPSE' untuk membuat kernel elips
kernel = cv2....(cv2...., (5, 5))

# Tuliskan 'cv2.morphologyEx' dan 'cv2.MORPH_CLOSE' untuk menutup lubang kecil pada objek
segmented_clean = cv2....(segmented, cv2...., kernel)

# 5. EKSTRAKSI OBJEK
# Tuliskan 'cv2.bitwise_and' untuk memotong citra asli menggunakan mask yang dibersihkan
extracted_img = cv2....(img, img, mask=segmented_clean)

# 6. MENYIMPAN HASIL
# Tuliskan 'imwrite' untuk menyimpan citra hasil proses ke dalam direktori
cv2....(os.path.join(output_dir, "1_citra_grayscale.jpg"), img)
cv2....(os.path.join(output_dir, "2_mask_segmentasi.jpg"), segmented_clean)
cv2....(os.path.join(output_dir, "3_ekstraksi_objek.jpg"), extracted_img)

# OUTPUT CONSOLE
print("=== ITERATIVE THRESHOLD SELECTION ===")
print("Proses Global Thresholding Selesai!")
print(f"Jumlah Iterasi Komputasi : {iteration}")
print(f"Nilai Ambang Batas Otomatis (T) : {global_threshold_val:.2f}")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createGlobalThresholdCellDOM(globalThresholdCellCount, defaultCode, defaultOutput);
  saveGlobalThresholdState();
}

function createGlobalThresholdCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("globalThresholdNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "globalthreshold-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runGlobalThresholdCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteGlobalThresholdCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </div>
        <textarea id="globalthreshold-editor-${id}"></textarea>
        <div id="globalthreshold-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`globalthreshold-editor-${id}`),
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

  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveGlobalThresholdState();
  });
  globalThresholdEditors[id] = editor;
}

// 4. Eksekusi Kompilasi Matriks
function runGlobalThresholdCell(id) {
  if (!globalThresholdEditors[id]) return;

  const code = globalThresholdEditors[id].getValue();
  const outputBox = document.getElementById(`globalthreshold-output-${id}`);
  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Menghitung iterasi threshold...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: globalThresholdImagePath }),
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
                <strong>✅ Hebat! Komputasi berhasil diselesaikan:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        if (data.images && Array.isArray(data.images)) {
          data.images.forEach((img) => {
            // Abaikan penarikan gambar histogram dari backend jika kebetulan masih tersisa
            let titleLower = img.title.toLowerCase();
            if (
              !titleLower.includes("grafik") &&
              !titleLower.includes("histogram")
            ) {
              let cleanTitle = img.title
                .replace("citra_", "Citra ")
                .replace("hasil_", "Hasil ")
                .replace(".jpg", "")
                .replace(".png", "");

              cleanTitle = cleanTitle.replace(/\b\w/g, (c) => c.toUpperCase());
              outputHTML += renderGlobalThresholdImgCard(cleanTitle, img.url);
            }
          });
        } else {
          // Fallback tanpa memanggil file histogram
          outputHTML += renderGlobalThresholdImgCard(
            "Citra Grayscale",
            "/static/results/citra_grayscale.jpg",
          );
          outputHTML += renderGlobalThresholdImgCard(
            "Hasil Segmentasi",
            "/static/results/hasil_segmentasi.jpg",
          );
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveGlobalThresholdState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
    });
}

function renderGlobalThresholdImgCard(title, srcUrl) {
  const t = Date.now();
  const urlWithCacheBuster = srcUrl.includes("?")
    ? `${srcUrl}&t=${t}`
    : `${srcUrl}?t=${t}`;

  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white shadow-sm d-flex flex-column align-items-center" style="width: fit-content;">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.85rem;">
            ${title}
        </h6>

        <div class="bg-light rounded border d-flex align-items-center justify-content-center"
             style="width: 120px; height: 120px; overflow: hidden;">
            <img src="${urlWithCacheBuster}"
                 class="result-image preview-image img-fluid"
                 style="width: 100%; height: 100%; cursor: zoom-in; object-fit: contain; image-rendering: pixelated;"
                 title="Klik untuk melihat ukuran penuh"
                 data-bs-toggle="modal"
                 data-bs-target="#globalThresholdImageModal"
                 onclick="openGlobalThresholdModal('${urlWithCacheBuster}')">
        </div>

        <div class="text-muted mt-2"
             style="font-size: 0.7rem; cursor: pointer;"
             data-bs-toggle="modal"
             data-bs-target="#globalThresholdImageModal"
             onclick="openGlobalThresholdModal('${urlWithCacheBuster}')">
            Klik gambar untuk memperbesar
        </div>
    </div>
`;
}

// 5. Utilitas File Upload & Management
function openGlobalThresholdModal(src) {
  document.getElementById("globalThresholdModalImage").src = src;
}

function deleteGlobalThresholdCell(id) {
  document.getElementById("globalthreshold-cell-" + id).remove();
  delete globalThresholdEditors[id];
  saveGlobalThresholdState();
}

function triggerGlobalThresholdUpload2() {
  document.getElementById("globalThresholdFileInput").click();
}

function handleGlobalThresholdUpload(event) {
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_globalthreshold" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("globalThresholdFileList").innerHTML = `
        <div class="text-center text-muted mt-3 small">
            <i class="fa-solid fa-spinner fa-spin me-2"></i>Mengunggah...
        </div>
    `;

    fetch("/upload-image", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
        globalThresholdImagePath = data.path;

        document.getElementById("globalThresholdFileList").innerHTML = `
        <div class="image-preview-card mt-3">
            <div class="img-wrapper text-center">
                <img src="${imageSrc}" class="preview-img img-fluid rounded border border-secondary" style="max-height: 120px; object-fit: cover;" alt="Preview File">
            </div>
            <div class="file-name-text mt-2 small text-truncate fw-bold text-dark text-center" title="${data.filename}">
                <i class="fa-solid fa-file-image me-1 text-custom-blue"></i>
                ${data.filename}
            </div>
        </div>
        `;
        saveGlobalThresholdState();
      })
      .catch((err) => {
        document.getElementById("globalThresholdFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };

  reader.readAsDataURL(originalFile);
}
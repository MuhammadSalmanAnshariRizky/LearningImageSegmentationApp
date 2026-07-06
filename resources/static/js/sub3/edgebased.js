/**
 * Script untuk Live Code Notebook - Edge-Based Segmentation
 */

let edgeCellCount = 0;
let edgeEditors = {};
let edgeImagePath = "";

// ==========================================
// 1. INISIASI & INTERSECTION OBSERVER
// ==========================================
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
  if (notebook) {
    observer.observe(notebook);
  }
});

// ==========================================
// 2. LOCAL STORAGE (SIMPAN & MUAT DATA)
// ==========================================
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
  if (fileListElem) {
    localStorage.setItem("currentImageName_Edge", fileListElem.innerHTML);
  }
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

  if (savedCellCount) {
    edgeCellCount = parseInt(savedCellCount);
  }

  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) => {
      createEdgeCellDOM(cellData.id, cellData.code, cellData.output);
    });
  }
}

// ==========================================
// 3. TAMBAH CELL & RENDER DOM
// ==========================================
function addEdgeCell() {
  edgeCellCount++;

  const defaultCode = `import cv2
import numpy as np
import os

# 1. MEMBACA CITRA GRAYSCALE
# Tuliskan nama file gambar yang kamu upload di bagian upload file
image_path = '...'

# Tuliskan 'imread' dan 'IMREAD_GRAYSCALE' untuk membaca gambar langsung sebagai hitam putih
image = cv2....(image_path, cv2....) 

# 2. EDGE DETECTION (OPERATOR CANNY)
# Tuliskan 'Canny' untuk melakukan deteksi tepi pada citra 
edges = cv2....(image, 65, 100)

# 3. EDGE LINKING (MORPHOLOGICAL CLOSING)
# Bentuk kernel yang akan kita gunakan adalah elips, tuliskan 'MORPH_ELLIPSE'
kernel = cv2.getStructuringElement(cv2...., (5, 5))

# Lakukan operasi morfologi penutupan (closing), tuliskan 'MORPH_CLOSE'
closed = cv2.morphologyEx(edges, cv2...., kernel, iterations=1)

# 4. MENCARI KONTUR
# Tuliskan 'findContours' untuk mendeteksi batas-batas tepi objek yang sudah menyambung
contours, hierarchy = cv2....(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. REGION EXTRACTION (MASK KONTUR TERBESAR)
# Buat kanvas kosong (hitam) dengan ukuran yang sama dengan citra asli, tuliskan 'zeros_like'
mask = np....(image)

if len(contours) > 0:
    # Cari objek utama berdasarkan luas area terbesar, tuliskan 'contourArea'
    largest_contour = max(contours, key=cv2....)
    
    # Warnai penuh bagian dalam kontur tersebut, tuliskan 'FILLED'
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2....)
    
    # Ekstrak objek asli dengan memotongnya menggunakan operasi logika, tuliskan 'bitwise_and'
    segmented = cv2....(image, image, mask=mask)
    
    # Hitung kembali luas objek yang didapatkan, tuliskan 'contourArea'
    area = cv2....(largest_contour)
    print(f"Luas objek terbesar: {area:.2f} piksel")
else:
    print("Tidak ada kontur yang ditemukan.")
    segmented = image.copy()

# 6. MENYIMPAN HASIL
# Tuliskan 'imwrite' untuk menyimpan kelima citra hasil proses ke dalam direktori
cv2....(os.path.join(output_dir, "1_citra_asli.jpg"), image)
cv2....(os.path.join(output_dir, "2_edge_detection.jpg"), edges)
cv2....(os.path.join(output_dir, "3_edge_linking.jpg"), closed)
cv2....(os.path.join(output_dir, "4_region_extraction.jpg"), mask)
cv2....(os.path.join(output_dir, "5_segmented_result.jpg"), segmented)

print("Proses segmentasi berbasis tepi selesai dijalankan!")
print(f"Jumlah kontur ditemukan secara keseluruhan: {len(contours)}")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createEdgeCellDOM(edgeCellCount, defaultCode, defaultOutput);
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
            <span class="text-muted small fw-bold">In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runEdgeCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteEdgeCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
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

  setTimeout(() => {
    editor.refresh();
  }, 10);

  editor.on("change", function (cm) {
    cm.setSize(null, "auto");
    saveEdgeState();
  });

  edgeEditors[id] = editor;
}

// ==========================================
// 4. JALANKAN KODE (RUN CELL)
// ==========================================
function runEdgeCell(id) {
  if (!edgeEditors[id]) return;

  const code = edgeEditors[id].getValue();
  const outputBox = document.getElementById(`edge-output-${id}`);

  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Sedang memproses kodemu...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: edgeImagePath }),
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
                <strong>✅ Hebat! Proses segmentasi berhasil:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        // LOGIKA PENAMPILAN GAMBAR HASIL YANG SAMA DENGAN GRAYSCALE
        if (data.images && Array.isArray(data.images)) {
          // Menampilkan citra asli terlebih dahulu jika ada
          let originalImage = data.images.find((img) =>
            img.title.toLowerCase().includes("asli"),
          );
          if (originalImage) {
            outputHTML += createEdgeImageCard("Citra Asli", originalImage.url);
          }

          // Menampilkan sisa gambar lainnya secara dinamis
          data.images.forEach((img) => {
            let titleLower = img.title.toLowerCase();
            if (!titleLower.includes("asli")) {
              let cleanTitle = img.title
                .replace("edge_", "Edge ")
                .replace("region_", "Region ")
                .replace(".jpg", "")
                .replace(".png", "");

              // Kapitalisasi Huruf Awal
              cleanTitle = cleanTitle.replace(/\b\w/g, (c) => c.toUpperCase());

              outputHTML += createEdgeImageCard(cleanTitle, img.url);
            }
          });
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveEdgeState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
    });
}

function createEdgeImageCard(title, srcUrl) {
  // Tambahkan timestamp agar browser tidak load dari cache (mengatasi error 404 cache lama)
  const timestamp = new Date().getTime();
  const urlWithCacheBuster = srcUrl.includes("?")
    ? `${srcUrl}&t=${timestamp}`
    : `${srcUrl}?t=${timestamp}`;

  return `
      <div class="image-card text-center border p-2 rounded-3 bg-white shadow-sm d-flex flex-column align-items-center" style="width: fit-content;">
          <h6 class="fw-bold text-secondary mb-2" style="font-size:0.85rem;">${title}</h6>
          
          <div class="bg-light rounded border d-flex align-items-center justify-content-center" style="width: 120px; height: 120px; overflow: hidden;">
              <img src="${urlWithCacheBuster}" class="result-image preview-image img-fluid" 
                   style="width: 100%; height: 100%; cursor: zoom-in; object-fit: contain; image-rendering: pixelated;"
                   title="Klik untuk melihat ukuran penuh"
                   data-bs-toggle="modal" data-bs-target="#edgeImageModal" 
                   onclick="openEdgeModal('${urlWithCacheBuster}')">
          </div>
          
          <div class="text-muted mt-2" style="font-size: 0.7rem; cursor: pointer;" 
               data-bs-toggle="modal" data-bs-target="#edgeImageModal" 
               onclick="openEdgeModal('${urlWithCacheBuster}')">
              Klik gambar untuk memperbesar
          </div>
      </div>
    `;
}

// ==========================================
// 5. MANAJEMEN MODAL, UPLOAD & HAPUS CELL
// ==========================================
function openEdgeModal(src) {
  const modalImg = document.getElementById("edgeModalImage");
  if (modalImg) modalImg.src = src;
}

function deleteEdgeCell(id) {
  const cellElem = document.getElementById("edge-cell-" + id);
  if (cellElem) cellElem.remove();
  delete edgeEditors[id];
  saveEdgeState();
}

function triggerEdgeUpload() {
  const fileInput = document.getElementById("edgeFileInput");
  if (fileInput) fileInput.click();
}

function handleEdgeUpload(event) {
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  // Menyamakan standar nama file seperti di grayscale
  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_edge" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("edgeFileList").innerHTML = `
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
        edgeImagePath = data.path;

        document.getElementById("edgeFileList").innerHTML = `
        <div class="image-preview-card mt-3">
            <div class="img-wrapper">
                <img src="${imageSrc}" class="preview-img" alt="Preview File">
            </div>
            <div class="file-name-text mt-2 small text-truncate" title="${data.filename}">
                <i class="fa-solid fa-file-image me-1 text-primary"></i>
                ${data.filename}
            </div>
        </div>
    `;
        saveEdgeState();
      })
      .catch((err) => {
        document.getElementById("edgeFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };

  reader.readAsDataURL(originalFile);
}

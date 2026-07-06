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
import os

# 1. MEMBACA CITRA GRAYSCALE
# Tuliskan nama file gambar yang kamu unggah
# lalu tuliskan 'cv2.imread' dan 'cv2.IMREAD_GRAYSCALE' untuk membaca sebagai hitam putih
img = cv2....('...', cv2....)

# 2. MENENTUKAN SEED POINT & THRESHOLD TOLERANSI
# Tuliskan angka 50 dan 114 secara berurutan untuk koordinat seed, serta 140 untuk threshold
seed = (..., ...)   # (baris, kolom);(y,x)
threshold = ...

# 3. MEMBUAT VISUALISASI TITIK SEED MANUAL MENGGUNAKAN OPENCV
# Tuliskan 'cv2.cvtColor' dan 'cv2.COLOR_GRAY2BGR' untuk mengubah ke format warna BGR agar bisa digambar lingkaran merah
citra_seed = cv2....(img, cv2....)

# Tuliskan 'cv2.circle' untuk menggambarkan penanda titik (seed) awal pada citra
cv2....(citra_seed, (seed[1], seed[0]), radius=5, color=(0, 0, 255), thickness=-1)

# 4. ALGORITMA CORE PROCESS REGION GROWING (MEMBUAT MASK)
rows, cols = img.shape

# Tuliskan 'np.zeros' pada numpy (np) untuk membuat matriks kosong bertipe data np.uint8
segmented = np....((rows, cols), np.uint8)

# Tuliskan 'np.zeros' pada numpy (np) untuk membuat penanda piksel yang sudah dikunjungi bertipe np.bool_
visited = np....((rows, cols), np.bool_)

seed_value = int(img[seed])
queue = [seed]

while len(queue) > 0:
    x, y = queue.pop(0)

    if visited[x, y]:
        continue

    visited[x, y] = True

    # Similarity Criterion
    if abs(int(img[x, y]) - seed_value) <= threshold:
        segmented[x, y] = 255

        # 8-connectivity (Mengecek 8 tetangga di sekitarnya)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = x + dx
                ny = y + dy

                if (0 <= nx < rows and 
                    0 <= ny < cols and 
                    not visited[nx, ny]):
                    queue.append((nx, ny))

# 5. EKSTRAKSI GAMBAR DARI MASK (POST-PROCESSING)
# Tuliskan 'cv2.getStructuringElement' dan 'cv2.MORPH_ELLIPSE' untuk membuat struktur kernel elips ukuran 9x9
kernel = cv2....(cv2...., (9, 9))

# Tuliskan 'cv2.morphologyEx' dan 'cv2.MORPH_CLOSE' untuk membersihkan lubang kecil pada mask hasil segmentasi
segmented_clean = cv2....(segmented, cv2...., kernel)

# Tuliskan 'cv2.bitwise_and' untuk memotong citra asli berdasarkan area putih pada mask
extracted_img = cv2....(img, img, mask=segmented_clean)

# 6. MENYIMPAN HASIL
# Tuliskan 'imwrite' untuk menyimpan keempat citra hasil proses ke dalam direktori
cv2....(os.path.join(output_dir, "citra_asli_region.jpg"), img)
cv2....(os.path.join(output_dir, "visualisasi_seed.jpg"), citra_seed)
cv2....(os.path.join(output_dir, "hasil_region_growing.jpg"), segmented)
cv2....(os.path.join(output_dir, "hasil_ekstraksi.jpg"), extracted_img)

print("Proses Segmentasi Region Growing Selesai Dijalankan!")
print(f"Intensitas Nilai Piksel Seed Point: {seed_value}")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createRegionCellDOM(regionCellCount, defaultCode, defaultOutput);
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
            <span class="text-muted small fw-bold">In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runRegionCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteRegionCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
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

  setTimeout(() => {
    editor.refresh();
  }, 10);

  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveRegionState();
  });
  regionEditors[id] = editor;
}

// 4. Integrasi Backend Compilation
function runRegionCell(id) {
  if (!regionEditors[id]) return;

  const code = regionEditors[id].getValue();
  const outputBox = document.getElementById(`region-output-${id}`);
  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Mengeksekusi penelusuran Region Growing...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: regionImagePath }),
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
                <strong>✅ Hebat! Komputasi Region Growing selesai:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        if (data.images && Array.isArray(data.images)) {
          // --- PROSES SORTING LOGIS DISINI ---
          // Kita mapping berdasarkan kata kunci nama file agar urutannya konsisten
          const logicalOrder = ["asli", "seed", "growing", "ekstraksi"];

          data.images.sort((a, b) => {
            const indexA = logicalOrder.findIndex((key) =>
              a.title.toLowerCase().includes(key),
            );
            const indexB = logicalOrder.findIndex((key) =>
              b.title.toLowerCase().includes(key),
            );
            return indexA - indexB;
          });

          data.images.forEach((img) => {
            let cleanTitle = img.title
              .replace("citra_", "Citra ")
              .replace("visualisasi_", "Visualisasi ")
              .replace("hasil_", "Hasil ")
              .replace("_region", "")
              .replace("_growing", " Growing")
              .replace(".jpg", "")
              .replace(".png", "");

            cleanTitle = cleanTitle.replace(/\b\w/g, (c) => c.toUpperCase());
            outputHTML += renderRegionImgCard(cleanTitle, img.url);
          });
        } else {
          // Fallback Render Statis (Juga disesuaikan urutannya)
          outputHTML += renderRegionImgCard(
            "Citra Asli",
            "/static/results/citra_asli_region.jpg",
          );
          outputHTML += renderRegionImgCard(
            "Visualisasi Seed",
            "/static/results/visualisasi_seed.jpg",
          );
          outputHTML += renderRegionImgCard(
            "Hasil Region Growing",
            "/static/results/hasil_region_growing.jpg",
          );
          outputHTML += renderRegionImgCard(
            "Hasil Ekstraksi",
            "/static/results/hasil_ekstraksi.jpg",
          );
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveRegionState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
    });
}

function renderRegionImgCard(title, srcUrl) {
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
                 data-bs-target="#regionImageModal"
                 onclick="openRegionModal('${urlWithCacheBuster}')">
        </div>

        <div class="text-muted mt-2"
             style="font-size: 0.7rem; cursor: pointer;"
             data-bs-toggle="modal"
             data-bs-target="#regionImageModal"
             onclick="openRegionModal('${urlWithCacheBuster}')">
            Klik gambar untuk memperbesar
        </div>
    </div>
`;
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
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_region" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("regionFileList").innerHTML = `
        <div class="text-center text-muted mt-3 small">
            <i class="fa-solid fa-spinner fa-spin me-2"></i>Mengunggah...
        </div>
    `;

    fetch("/upload-image", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
        regionImagePath = data.path;

        document.getElementById("regionFileList").innerHTML = `
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
        saveRegionState();
      })
      .catch((err) => {
        document.getElementById("regionFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };

  reader.readAsDataURL(originalFile);
}

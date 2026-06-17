let cellCount = 0;
let editors = {};
let currentImagePath = "";

// ==========================================
// 1. INISIASI & INTERSECTION OBSERVER
// ==========================================
document.addEventListener("DOMContentLoaded", function () {
  loadState();

  // Mencegah CodeMirror hancur saat pindah tab/section
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in editors) {
            if (editors[id]) editors[id].refresh();
          }
        }, 50);
      }
    });
  });

  const notebook = document.querySelector(".notebook-wrapper");
  if (notebook) {
    observer.observe(notebook);
  }
});

// ==========================================
// 2. LOCAL STORAGE (SIMPAN & MUAT DATA)
// ==========================================
function saveState() {
  const cellsData = [];
  for (const id in editors) {
    cellsData.push({
      id: id,
      code: editors[id].getValue(),
      output: document.getElementById(`output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_Grayscale", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_Grayscale", currentImagePath);

  const fileListElem = document.getElementById("fileList");
  if (fileListElem) {
    localStorage.setItem("currentImageName_Grayscale", fileListElem.innerHTML);
  }
  localStorage.setItem("cellCount_Grayscale", cellCount);
}

function loadState() {
  const savedCells = JSON.parse(
    localStorage.getItem("notebookCells_Grayscale"),
  );
  const savedPath = localStorage.getItem("currentImagePath_Grayscale");
  const savedImageUI = localStorage.getItem("currentImageName_Grayscale");
  const savedCellCount = localStorage.getItem("cellCount_Grayscale");

  if (savedPath && savedImageUI) {
    currentImagePath = savedPath;
    document.getElementById("fileList").innerHTML = savedImageUI;
  }

  if (savedCellCount) {
    cellCount = parseInt(savedCellCount);
  }

  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) => {
      createCellDOM(cellData.id, cellData.code, cellData.output);
    });
  }
}

// ==========================================
// 3. TAMBAH CELL & RENDER DOM
// ==========================================
function addCell() {
  cellCount++;

  // Template Kode Rumpang untuk 3 Metode Grayscale
  const defaultCode = `import cv2
import numpy as np
import os
# 1. BACA GAMBAR DARI UPLOAD
# tuliskan nama file dari gambar yang akan diproses
img = cv2.imread('.....')

# 2. PISAHKAN CHANNEL BGR
# OpenCV menggunakan urutan: 0 = Biru (Blue), 1 = Hijau (Green), dan 2 = Merah (Red)

B = img[:, :, 0]

# Lengkapi indeks kanal hijau
G = img[:, :, .....]

# Lengkapi indeks kanal merah
R = img[:, :, .....]

# 3. METODE GRAYSCALE

# A. Lightness Method
# Mencari nilai maksimum dan minimum dari kanal RGB
max_rgb = cv2.max(cv2.max(R, G), B)
min_rgb = cv2.min(cv2.min(R, G), B)

# Lengkapi dengan variabel yang menyimpan nilai maksimum dan minimum RGB
gray_lightness = ((..... + .....) / 2).astype(np.uint8)

# B. Average Method
# Lengkapi dengan jumlah kanal warna yang digunakan
gray_average = ((R + G + B) / .....).astype(np.uint8)

# C. Luminosity Method
# Bobot masing masing kanal yaitu : Merah = 0.21, Hijau = 0.72, dan Biru  = 0.07
# Lengkapi dengan bobot yang sesuai untuk kanal merah, hijau, dan biru
gray_luminosity = (
    (..... * R) +
    (..... * G) +
    (..... * B)
).astype(np.uint8)

# 4. SIMPAN HASIL
cv2.imwrite(os.path.join(output_dir, "hasil_lightness.jpg"), gray_lightness)
cv2.imwrite(os.path.join(output_dir, "hasil_average.jpg"), gray_average)
cv2.imwrite(os.path.join(output_dir, "hasil_luminosity.jpg"), gray_luminosity)

# 5. OUTPUT
print("Luar biasa! Ketiga metode Grayscale berhasil diproses!")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createCellDOM(cellCount, defaultCode, defaultOutput);
  saveState();
}

function createCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("notebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "cell-" + id;

  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </div>
        <textarea id="editor-${id}"></textarea>
        <div id="output-${id}" class="output-box">${outputHTML}</div>
    `;

  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`editor-${id}`),
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
    saveState();
  });

  editors[id] = editor;
}

// ==========================================
// 4. JALANKAN KODE (RUN CELL)
// ==========================================
function runCell(id) {
  if (!editors[id]) return;

  const code = editors[id].getValue();
  const outputBox = document.getElementById(`output-${id}`);

  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Sedang memproses kodemu...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: currentImagePath }),
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
        // Tampilkan Output Konsol
        let outputHTML = `
            <div class="text-success font-monospace mb-3">
                <strong>✅ Hebat! Hasil konversi:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        // LOGIKA PENAMPILAN 3 GAMBAR HASIL
        // Memeriksa jika backend mengirim key spesifik
        if (data.hasil_lightness)
          outputHTML += createImageCard("Lightness", data.hasil_lightness);
        if (data.hasil_average)
          outputHTML += createImageCard("Average", data.hasil_average);
        if (data.hasil_luminosity)
          outputHTML += createImageCard("Luminosity", data.hasil_luminosity);

        // Fallback: Jika backend mengirim daftar gambar dalam array 'images'
        if (data.images && Array.isArray(data.images)) {
          data.images.forEach((img) => {
            // Filter: Abaikan gambar asli, hanya ambil gambar hasil
            let titleLower = img.title.toLowerCase();
            if (
              !titleLower.includes("asli") &&
              !titleLower.includes("rgb") &&
              !titleLower.includes("before")
            ) {
              let cleanTitle = img.title
                .replace("hasil_", "")
                .replace(".jpg", "")
                .replace(".png", "");
              cleanTitle =
                cleanTitle.charAt(0).toUpperCase() + cleanTitle.slice(1);
              outputHTML += createImageCard(cleanTitle, img.url);
            }
          });
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
    });
}

// Komponen Helper untuk merender elemen kartu gambar
function createImageCard(title, srcUrl) {
  return `
      <div class="image-card text-center border p-2 rounded-3 bg-white shadow-sm" style="width: fit-content;">
          <h6 class="fw-bold text-secondary mb-2" style="font-size:0.85rem;">${title}</h6>
          <img src="${srcUrl}" class="result-image preview-image img-fluid rounded" 
               style="max-height: 140px; cursor: pointer; object-fit: contain;"
               data-bs-toggle="modal" data-bs-target="#imageModal" 
               onclick="openImageModal('${srcUrl}')">
      </div>
    `;
}

// ==========================================
// 5. MANAJEMEN MODAL, UPLOAD & HAPUS CELL
// ==========================================
function openImageModal(src) {
  const modalImg = document.getElementById("modalImage");
  if (modalImg) modalImg.src = src;
}

function deleteCell(id) {
  const cellElem = document.getElementById("cell-" + id);
  if (cellElem) cellElem.remove();
  delete editors[id];
  saveState();
}

function triggerUpload() {
  const fileInput = document.getElementById("fileInput");
  if (fileInput) fileInput.click();
}

function handleUpload(event) {
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_rgb" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("fileList").innerHTML = `
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
        currentImagePath = data.path;

        document.getElementById("fileList").innerHTML = `
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

        saveState();
      })
      .catch((err) => {
        document.getElementById("fileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };

  reader.readAsDataURL(originalFile);
}

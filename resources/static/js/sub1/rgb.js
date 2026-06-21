/**
 * Script untuk Live Code Notebook - RGB Channel Separation
 */

let rgbCellCount = 0;
let rgbEditors = {};
let rgbImagePath = "";

// ==========================================
// 1. INISIASI & INTERSECTION OBSERVER
// ==========================================
document.addEventListener("DOMContentLoaded", function () {
  loadRGBState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in rgbEditors) {
            if (rgbEditors[id]) rgbEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("rgbNotebook");
  if (notebook) observer.observe(notebook.closest(".notebook-wrapper"));
});

// ==========================================
// 2. LOCAL STORAGE (SIMPAN & MUAT DATA)
// ==========================================
function saveRGBState() {
  const cellsData = [];
  for (const id in rgbEditors) {
    cellsData.push({
      id: id,
      code: rgbEditors[id].getValue(),
      output: document.getElementById(`rgb-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_RGB", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_RGB", rgbImagePath);

  const fileListElem = document.getElementById("rgbFileList");
  if (fileListElem) {
    localStorage.setItem("currentImageName_RGB", fileListElem.innerHTML);
  }
  localStorage.setItem("cellCount_RGB", rgbCellCount);
}

function loadRGBState() {
  const savedCells = JSON.parse(localStorage.getItem("notebookCells_RGB"));
  const savedPath = localStorage.getItem("currentImagePath_RGB");
  const savedImageUI = localStorage.getItem("currentImageName_RGB");
  const savedCellCount = localStorage.getItem("cellCount_RGB");

  if (savedPath && savedImageUI) {
    rgbImagePath = savedPath;
    document.getElementById("rgbFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) {
    rgbCellCount = parseInt(savedCellCount);
  }
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) => {
      createRGBCellDOM(cellData.id, cellData.code, cellData.output);
    });
  }
}

// ==========================================
// 3. TAMBAH CELL & RENDER DOM
// ==========================================
function addRGBCell() {
  rgbCellCount++;
  const defaultCode = `import cv2
import numpy as np
import os

# LANGKAH 1 : MEMBACA GAMBAR
# Isi parameter dengan nama file yang digunakan
img = cv2.imread('...')

# LANGKAH 2 : MEMISAHKAN KANAL WARNA
# OpenCV menggunakan format BGR (Blue, Green, Red)
# Indeks kanal: 0 = Biru (Blue) 1 = Hijau (Green) 2 = Merah (Red)

B = img[:, :, ...]  # Mengambil seluruh piksel kanal biru
G = img[:, :, ...]  # Mengambil seluruh piksel kanal hijau
R = img[:, :, ...]  # Mengambil seluruh piksel kanal merah

# LANGKAH 3 : MEMBUAT GAMBAR KHUSUS KANAL MERAH
red_img = np.zeros_like(img)

# Gunakan variabel R agar citra hanya menampilkan kanal merah
red_img[:, :, 2] = ...

# LANGKAH 4 : MEMBUAT GAMBAR KHUSUS KANAL HIJAU
green_img = np.zeros_like(img)

# Gunakan variabel G agar citra hanya menampilkan kanal merah
green_img[:, :, 1] = ...

# LANGKAH 5 : MEMBUAT GAMBAR KHUSUS KANAL BIRU
blue_img = np.zeros_like(img)

# Gunakan variabel B agar citra hanya menampilkan kanal merah
blue_img[:, :, 0] = ...

# LANGKAH 6 : MENYIMPAN HASIL PEMISAHAN KANAL, 
# Lengkapi bagian yang kosong dengan menuliskan 'red_img', 'green_img', dan 'blue_img'
cv2.imwrite(os.path.join(output_dir, "kanal_red.jpg"), ...)
cv2.imwrite(os.path.join(output_dir, "kanal_green.jpg"), ...)
cv2.imwrite(os.path.join(output_dir, "kanal_blue.jpg"), ...)

print("Pemisahan kanal RGB berhasil dilakukan.")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;
  createRGBCellDOM(rgbCellCount, defaultCode, defaultOutput);
  saveRGBState();
}

function createRGBCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("rgbNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "rgb-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">RGB In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runRGBCell(${id})" title="Run"><i class="fa-solid fa-play"></i></button>
                <button class="btn-icon delete" onclick="deleteRGBCell(${id})" title="Hapus"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>
        <textarea id="rgb-editor-${id}"></textarea>
        <div id="rgb-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`rgb-editor-${id}`),
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

  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveRGBState();
  });
  rgbEditors[id] = editor;
}

// ==========================================
// 4. JALANKAN KODE (RUN CELL)
// ==========================================
function runRGBCell(id) {
  if (!rgbEditors[id]) return;

  const code = rgbEditors[id].getValue();
  const outputBox = document.getElementById(`rgb-output-${id}`);

  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Mengekstrak kanal warna...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: rgbImagePath }),
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
                <strong>✅ Hebat! Hasil ekstraksi:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
                ${data.before_image ? createRGBImageCard("Gambar Asli", data.before_image) : ""}
        `;

        // Logika Dinamis Penangkapan Gambar dari Backend (Mirip Grayscale)
        if (data.images && Array.isArray(data.images)) {
          data.images.forEach((img) => {
            let titleLower = img.title.toLowerCase();

            // Abaikan jika itu gambar asli, karena sudah di-render di atas
            if (
              !titleLower.includes("asli") &&
              !titleLower.includes("before") &&
              !titleLower.includes("rgb")
            ) {
              // Percantik judul secara otomatis berdasarkan nama filenya
              let cleanTitle = img.title;
              if (titleLower.includes("red")) cleanTitle = "Kanal Merah (Red)";
              else if (titleLower.includes("green"))
                cleanTitle = "Kanal Hijau (Green)";
              else if (titleLower.includes("blue"))
                cleanTitle = "Kanal Biru (Blue)";

              outputHTML += createRGBImageCard(cleanTitle, img.url);
            }
          });
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveRGBState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
      saveRGBState();
    });
}

function createRGBImageCard(title, srcUrl) {
  return `
      <div class="image-card text-center border p-2 rounded-3 bg-white shadow-sm d-flex flex-column align-items-center" style="width: fit-content;">
          <h6 class="fw-bold text-secondary mb-2" style="font-size:0.85rem;">${title}</h6>
          
          <div class="bg-light rounded border d-flex align-items-center justify-content-center" style="width: 120px; height: 120px; overflow: hidden;">
              <img src="${srcUrl}" class="result-image preview-image img-fluid" 
                   style="width: 100%; height: 100%; cursor: zoom-in; object-fit: contain; image-rendering: pixelated;"
                   title="Klik untuk melihat ukuran penuh"
                   data-bs-toggle="modal" data-bs-target="#rgbImageModal" 
                   onclick="openRGBModal(this.src)">
          </div>
          
          <div class="text-muted mt-2" style="font-size: 0.7rem; cursor: pointer;" 
               data-bs-toggle="modal" data-bs-target="#rgbImageModal" 
               onclick="openRGBModal('${srcUrl}')">
              Klik gambar untuk memperbesar
          </div>
      </div>
    `;
}

// ==========================================
// 5. MANAJEMEN MODAL & UPLOAD
// ==========================================
function openRGBModal(src) {
  const modalImg = document.getElementById("rgbModalImage"); // Sesuai ID di HTML baru
  if (modalImg) {
    modalImg.src = src;
  }
}

function deleteRGBCell(id) {
  const cellElem = document.getElementById("rgb-cell-" + id);
  if (cellElem) cellElem.remove();
  delete rgbEditors[id];
  saveRGBState();
}

function triggerRGBUpload() {
  const fileInput = document.getElementById("rgbFileInput");
  if (fileInput) fileInput.click();
}

function handleRGBUpload(event) {
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

    document.getElementById("rgbFileList").innerHTML = `
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
        rgbImagePath = data.path;

        document.getElementById("rgbFileList").innerHTML = `
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
        saveRGBState();
      })
      .catch((err) => {
        document.getElementById("rgbFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };
  reader.readAsDataURL(originalFile);
}

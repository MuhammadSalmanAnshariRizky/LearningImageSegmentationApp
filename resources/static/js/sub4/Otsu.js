/**
 * Script untuk Live Code Notebook - Otsu Thresholding (Tanpa Matplotlib)
 */

let otsuCellCount = 0;
let otsuEditors = {};
let otsuImagePath = "";

// 1. Inisiasi Observer
document.addEventListener("DOMContentLoaded", function () {
  loadOtsuState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in otsuEditors) {
            if (otsuEditors[id]) otsuEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("otsuNotebook");
  if (notebook) observer.observe(notebook);
});

// 2. Local Storage Management
function saveOtsuState() {
  const cellsData = [];
  for (const id in otsuEditors) {
    cellsData.push({
      id: id,
      code: otsuEditors[id].getValue(),
      output: document.getElementById(`otsu-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_Otsu", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_Otsu", otsuImagePath);
  const fileListElem = document.getElementById("otsuFileList");
  if (fileListElem)
    localStorage.setItem("currentImageName_Otsu", fileListElem.innerHTML);
  localStorage.setItem("cellCount_Otsu", otsuCellCount);
}

function loadOtsuState() {
  const savedCells = JSON.parse(localStorage.getItem("notebookCells_Otsu"));
  const savedPath = localStorage.getItem("currentImagePath_Otsu");
  const savedImageUI = localStorage.getItem("currentImageName_Otsu");
  const savedCellCount = localStorage.getItem("cellCount_Otsu");

  if (savedPath && savedImageUI) {
    otsuImagePath = savedPath;
    document.getElementById("otsuFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) otsuCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) =>
      createOtsuCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Tambah Lembar Kerja Cell
function addOtsuCell() {
  otsuCellCount++;

  // Script Python Otomatis (Tanpa Plotting Matplotlib)
  const defaultCode = `import cv2
import numpy as np
import os

# 1. MEMBACA CITRA GRAYSCALE
# Tuliskan nama file gambar yang kamu unggah (misal: 'gambar.jpg')
# lalu tuliskan 'cv2.imread' dan 'cv2.IMREAD_GRAYSCALE' untuk membaca sebagai citra grayscale
img = cv2....('....', cv2....)

# 2. OTSU THRESHOLDING
# Tuliskan 'cv2.threshold' untuk fungsi ambang batas.
# Lalu tuliskan 'cv2.THRESH_BINARY_INV' dan 'cv2.THRESH_OTSU' untuk menghitung T optimal secara otomatis
threshold_value, binary_image = cv2....(img, 0, 255, cv2.... + cv2....)

# 3. MEMBERSIHKAN MASK (CLOSING)
# Tuliskan 'cv2.getStructuringElement' dan 'cv2.MORPH_ELLIPSE' untuk membuat kernel elips
kernel = cv2....(cv2...., (5, 5))

# Tuliskan 'cv2.morphologyEx' dan 'cv2.MORPH_CLOSE' untuk menutup lubang kecil pada objek
binary_clean = cv2....(binary_image, cv2...., kernel)

# 4. EKSTRAKSI OBJEK
# Tuliskan 'cv2.bitwise_and' untuk memotong objek utama dari latar belakang
extracted_image = cv2....(img, img, mask=binary_clean)

# 5. MENYIMPAN HASIL
# Tuliskan 'cv2.imwrite' untuk menyimpan ketiga citra hasil proses ke dalam direktori
cv2....(os.path.join(output_dir, "1_citra_grayscale.jpg"), img)
cv2....(os.path.join(output_dir, "2_mask_segmentasi.jpg"), binary_clean)
cv2....(os.path.join(output_dir, "3_ekstraksi_objek.jpg"), extracted_image)

# OUTPUT CONSOLE
print("=== OTSU THRESHOLDING ===")
print("Proses Otsu Thresholding Selesai!")
print(f"Nilai Ambang Otomatis Optimal Terkalkulasi (T): {threshold_value:.0f}")`;
  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createOtsuCellDOM(otsuCellCount, defaultCode, defaultOutput);
  saveOtsuState();
}

function createOtsuCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("otsuNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "otsu-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runOtsuCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteOtsuCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </div>
        <textarea id="otsu-editor-${id}"></textarea>
        <div id="otsu-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`otsu-editor-${id}`),
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
    saveOtsuState();
  });
  otsuEditors[id] = editor;
}

// 4. Eksekusi Kompilasi Matriks
function runOtsuCell(id) {
  if (!otsuEditors[id]) return;

  const code = otsuEditors[id].getValue();
  const outputBox = document.getElementById(`otsu-output-${id}`);
  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Menganalisis threshold Otsu...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: otsuImagePath }),
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
                <strong>✅ Hebat! Komputasi Otsu berhasil:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        if (data.images && Array.isArray(data.images)) {
          data.images.forEach((img) => {
            let titleLower = img.title.toLowerCase();
            // Abaikan file grafik histogram jika sebelumnya tersimpan
            if (
              !titleLower.includes("grafik") &&
              !titleLower.includes("histogram")
            ) {
              let cleanTitle = img.title
                .replace("citra_", "Citra ")
                .replace("hasil_", "Hasil ")
                .replace("_otsu", "")
                .replace(".jpg", "")
                .replace(".png", "");

              cleanTitle = cleanTitle.replace(/\b\w/g, (c) => c.toUpperCase());
              outputHTML += renderOtsuImgCard(cleanTitle, img.url);
            }
          });
        } else {
          // Fallback Render Statis (Hanya 2 gambar)
          outputHTML += renderOtsuImgCard(
            "Citra Grayscale",
            "/static/results/citra_grayscale_otsu.jpg",
          );
          outputHTML += renderOtsuImgCard(
            "Hasil Segmentasi",
            "/static/results/hasil_otsu_thresholding.jpg",
          );
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveOtsuState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
    });
}

function renderOtsuImgCard(title, srcUrl) {
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
                 data-bs-target="#otsuImageModal"
                 onclick="openOtsuModal('${urlWithCacheBuster}')">
        </div>

        <div class="text-muted mt-2"
             style="font-size: 0.7rem; cursor: pointer;"
             data-bs-toggle="modal"
             data-bs-target="#otsuImageModal"
             onclick="openOtsuModal('${urlWithCacheBuster}')">
            Klik gambar untuk memperbesar
        </div>
    </div>
`;
}

// 5. Utilitas File Upload & Management
function openOtsuModal(src) {
  document.getElementById("otsuModalImage").src = src;
}

function deleteOtsuCell(id) {
  document.getElementById("otsu-cell-" + id).remove();
  delete otsuEditors[id];
  saveOtsuState();
}

function triggerOtsuUpload() {
  document.getElementById("otsuFileInput").click();
}

function handleOtsuUpload(event) {
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_otsu" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("otsuFileList").innerHTML = `
        <div class="text-center text-muted mt-3 small">
            <i class="fa-solid fa-spinner fa-spin me-2"></i>Mengunggah...
        </div>
    `;

    fetch("/upload-image", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
        otsuImagePath = data.path;

        document.getElementById("otsuFileList").innerHTML = `
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
        saveOtsuState();
      })
      .catch((err) => {
        document.getElementById("otsuFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };

  reader.readAsDataURL(originalFile);
}

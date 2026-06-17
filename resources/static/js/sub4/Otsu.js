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
import os

# 1. MEMBACA CITRA GRAYSCALE
# Tuliskan nama file gambar pada bagian argumen di bawah ini
img = cv2.imread('_____', cv2.IMREAD_GRAYSCALE)
if img is None:
    print("Gambar tidak ditemukan!")
    exit()

# 2. MELAKUKAN OTSU THRESHOLDING
T, otsu_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 3. MENYIMPAN MATRIKS HASIL FISIK UNTUK ANTARMUKA WEB
cv2.imwrite(os.path.join(output_dir, "citra_grayscale_otsu.jpg"), img)
cv2.imwrite(os.path.join(output_dir, "hasil_otsu_thresholding.jpg"), otsu_img)

print("Proses Otsu Thresholding Selesai!")
print(f"Nilai Ambang Otomatis Optimal Terkalkulasi (T): {T:.0f}")`;

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
    <div class="image-card text-center border p-2 rounded-3 bg-white shadow-sm" style="width: fit-content;">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.85rem;">${title}</h6>
        <img src="${urlWithCacheBuster}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 140px; cursor: pointer; object-fit: contain;"
             data-bs-toggle="modal" data-bs-target="#otsuImageModal" 
             onclick="openOtsuModal('${urlWithCacheBuster}')">
    </div>`;
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

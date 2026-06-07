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
  localStorage.setItem("notebookCells_Lightness", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_Lightness", currentImagePath);

  const fileListElem = document.getElementById("fileList");
  if (fileListElem) {
    localStorage.setItem("currentImageName_Lightness", fileListElem.innerHTML);
  }
  localStorage.setItem("cellCount_Lightness", cellCount);
}

function loadState() {
  const savedCells = JSON.parse(
    localStorage.getItem("notebookCells_Lightness"),
  );
  const savedPath = localStorage.getItem("currentImagePath_Lightness");
  const savedImageUI = localStorage.getItem("currentImageName_Lightness");
  const savedCellCount = localStorage.getItem("cellCount_Lightness");

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
// ==========================================
// 3. TAMBAH CELL & RENDER DOM
// ==========================================
function addCell() {
  cellCount++;

  // Template Kode Rumpang untuk Metode Luminosity
  const defaultCode = `import cv2
import numpy as np
import os

# =====================================
# BACA GAMBAR DARI UPLOAD
# =====================================
# Pastikan nama file sesuai dengan yang di-upload!
img = cv2.imread('.....')

# =====================================
# AMBIL CHANNEL BGR
# =====================================
B = img[:, :, 0]
G = img[:, :, .....]
R = img[:, :, .....]

# =====================================
# LUMINOSITY METHOD
# =====================================
# Lengkapi bobot rumusnya di bawah ini:
gray = ((..... * R) + (..... * G) + (..... * B)).astype(np.uint8)

# =====================================
# SIMPAN HASIL
# =====================================
# Direktori output_dir sudah otomatis disiapkan oleh sistem
save_path = os.path.join(output_dir, "hasil_luminosity.jpg")
cv2.imwrite(save_path, gray)

# =====================================
# OUTPUT
# =====================================
print("Grayscale Luminosity berhasil diproses!")
`;

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

  // Pastikan render awal mulus
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

  outputBox.innerHTML = `<span class="text-warning font-monospace">⏳ Running...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code: code,
      image_path: currentImagePath,
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
      // Tampilkan teks console dan gambar (jika ada) dari respon Flask
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
                            <h6 class="fw-bold text-secondary mb-2" style="font-size:0.9rem;">Gambar Asli</h6>
                            <img src="${data.before_image}" class="result-image preview-image img-fluid rounded" 
                                 style="max-height: 150px; cursor: pointer;"
                                 data-bs-toggle="modal" data-bs-target="#imageModal" 
                                 onclick="openImageModal('${data.before_image}')">
                        </div>
                    `
                        : ""
                    }
                    
                    ${
                      data.after_image
                        ? `
                        <div class="image-card text-center border p-2 rounded-3 bg-white">
                            <h6 class="fw-bold text-secondary mb-2" style="font-size:0.9rem;">Hasil Grayscale</h6>
                            <img src="${data.after_image}" class="result-image preview-image img-fluid rounded" 
                                 style="max-height: 150px; cursor: pointer;"
                                 data-bs-toggle="modal" data-bs-target="#imageModal" 
                                 onclick="openImageModal('${data.after_image}')">
                        </div>
                    `
                        : ""
                    }
                </div>
            </div>
        `;
      saveState();
    })
    .catch((err) => {
      console.error(err);
      outputBox.innerHTML = `<pre style="color:#ef4444;" class="font-monospace">Error: ${err.message}</pre>`;
      saveState();
    });
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

function uploadImage(event, id) {
  const file = event.target.files[0];
  const preview = document.getElementById(`preview-${id}`);
  if (file && preview) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
  }
}

function triggerUpload() {
  const fileInput = document.getElementById("fileInput");
  if (fileInput) fileInput.click();
}

function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("image", file);

  fetch("/upload-image", {
    // Menyesuaikan endpoint menjadi relative path seperti run-code
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      currentImagePath = data.path;

      const fileListElem = document.getElementById("fileList");
      if (fileListElem) {
        fileListElem.innerHTML = `
                <li>
                    <i class="fa-solid fa-file-image me-2 text-primary"></i>
                    ${file.name}
                </li>
            `;
      }
      saveState();
    })
    .catch((err) => {
      alert("Gagal mengupload gambar.");
    });
}

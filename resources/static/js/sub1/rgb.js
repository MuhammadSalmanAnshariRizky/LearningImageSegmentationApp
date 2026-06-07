/**
 * Script untuk Live Code Notebook - RGB Channel Separation
 */

let rgbCellCount = 0;
let rgbEditors = {};
let rgbImagePath = "";

// 1. Inisiasi
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
  if (notebook) observer.observe(notebook);
});

// 2. Local Storage
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
  if (fileListElem)
    localStorage.setItem("currentImageName_RGB", fileListElem.innerHTML);
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
  if (savedCellCount) rgbCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) =>
      createRGBCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Tambah Cell
function addRGBCell() {
  rgbCellCount++;
  const defaultCode = `import cv2
import numpy as np
import os

# 1. BACA GAMBAR
img = cv2.imread('....')

# 2. PISAHKAN KANAL (Format OpenCV: BGR)
B = img[:, :, 0]
G = img[:, :, .....]
R = img[:, :, .....]

# 3. BUAT KANAL WARNA TERPISAH
red_img = np.zeros_like(img)
red_img[:, :, 2] = R

green_img = np.zeros_like(img)
green_img[:, :, 1] = G

blue_img = np.zeros_like(img)
blue_img[:, :, 0] = B

# 4. SIMPAN HASIL
cv2.imwrite(os.path.join(output_dir, "kanal_red.jpg"), red_img)
cv2.imwrite(os.path.join(output_dir, "kanal_green.jpg"), green_img)
cv2.imwrite(os.path.join(output_dir, "kanal_blue.jpg"), blue_img)

print("Kanal RGB berhasil dipisahkan!")`;

  createRGBCellDOM(rgbCellCount, defaultCode, "Output RGB muncul di sini...");
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
  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveRGBState();
  });
  rgbEditors[id] = editor;
}

// 4. Run Cell
function runRGBCell(id) {
  const code = rgbEditors[id].getValue();
  const outputBox = document.getElementById(`rgb-output-${id}`);
  outputBox.innerHTML = "⏳ Running RGB...";

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: rgbImagePath }),
  })
    .then((res) => res.json())
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3"><pre>${data.output}</pre></div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${data.before_image ? renderRGBImgCard("Asli", data.before_image) : ""}
                    ${renderRGBImgCard("Red", "/static/results/kanal_red.jpg")}
                    ${renderRGBImgCard("Green", "/static/results/kanal_green.jpg")}
                    ${renderRGBImgCard("Blue", "/static/results/kanal_blue.jpg")}
                </div>
            </div>`;
      saveRGBState();
    });
}

function renderRGBImgCard(title, src) {
  const t = Date.now();
  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.8rem;">${title}</h6>
        <img src="${src}?t=${t}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 120px; cursor: pointer;"
             data-bs-toggle="modal" data-bs-target="#rgbImageModal" 
             onclick="openRGBModal('${src}?t=${t}')">
    </div>`;
}

// 5. Utilitas
function openRGBModal(src) {
  document.getElementById("rgbModalImage").src = src;
}
function deleteRGBCell(id) {
  document.getElementById("rgb-cell-" + id).remove();
  delete rgbEditors[id];
  saveRGBState();
}
function triggerRGBUpload() {
  document.getElementById("rgbFileInput").click();
}

function handleRGBUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("image", file);
  fetch("/upload-image", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      rgbImagePath = data.path;
      document.getElementById("rgbFileList").innerHTML =
        `<li><i class="fa-solid fa-file-image me-2 text-danger"></i> ${file.name}</li>`;
      saveRGBState();
    });
}

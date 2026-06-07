/**
 * Script untuk Live Code Notebook - Otsu Thresholding
 */

let otsuCellCount = 0;
let otsuEditors = {};
let otsuImagePath = "";

// 1. Inisiasi
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

// 2. Local Storage
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

// 3. Tambah Cell
function addOtsuCell() {
  otsuCellCount++;
  const defaultCode = `import cv2
import matplotlib.pyplot as plt
import os

# 1. MEMBACA CITRA GRAYSCALE
img = cv2.imread('_____', cv2.IMREAD_GRAYSCALE)

# 2. MELAKUKAN OTSU THRESHOLDING
T, otsu_img = cv2.threshold(
    img,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 3. MENGHITUNG HISTOGRAM CITRA
hist = cv2.calcHist([img], [0], None, [256], [0, 256])

# 4. MENYIMPAN MATRIKS HASIL FISIK UNTUK ANTARMUKA WEB
cv2.imwrite(os.path.join(output_dir, "citra_grayscale_otsu.jpg"), img)
cv2.imwrite(os.path.join(output_dir, "hasil_otsu_thresholding.jpg"), otsu_img)

# 5. MEMBUAT DAN MENYIMPAN GRAFIK PLOT HISTOGRAM
plt.figure(figsize=(6, 4))
plt.plot(hist, color='blue')
plt.axvline(T, color='red', linestyle='--')
plt.title('Histogram Citra')
plt.xlabel('Intensitas Piksel')
plt.ylabel('Frekuensi')
plt.xlim([0, 256])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "grafik_histogram_otsu.jpg"))
plt.close()

print("Proses Otsu Thresholding Selesai!")
print(f"Nilai Ambang Otomatis Optimal Terkalkulasi (T): {T:.0f}")`;

  createOtsuCellDOM(
    otsuCellCount,
    defaultCode,
    "Output Otsu Thresholding muncul di sini...",
  );
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
            <span class="text-muted small fw-bold">Otsu In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runOtsuCell(${id})" title="Run"><i class="fa-solid fa-play"></i></button>
                <button class="btn-icon delete" onclick="deleteOtsuCell(${id})" title="Hapus"><i class="fa-solid fa-trash"></i></button>
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
  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveOtsuState();
  });
  otsuEditors[id] = editor;
}

// 4. Run Cell
function runOtsuCell(id) {
  const code = otsuEditors[id].getValue();
  const outputBox = document.getElementById(`otsu-output-${id}`);
  outputBox.innerHTML = "⏳ Running Otsu Thresholding Detection...";

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: otsuImagePath }),
  })
    .then((res) => res.json())
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3"><pre>${data.output}</pre></div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${data.before_image ? renderOtsuImgCard("Citra Grayscale", "/static/results/citra_grayscale_otsu.jpg") : ""}
                    ${renderOtsuImgCard("Histogram & Threshold", "/static/results/grafik_histogram_otsu.jpg")}
                    ${renderOtsuImgCard("Hasil Otsu", "/static/results/hasil_otsu_thresholding.jpg")}
                </div>
            </div>`;
      saveOtsuState();
    });
}

function renderOtsuImgCard(title, src) {
  const t = Date.now();
  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.8rem;">${title}</h6>
        <img src="${src}?t=${t}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 120px; cursor: pointer;"
             data-bs-toggle="modal" data-bs-target="#otsuImageModal" 
             onclick="openOtsuModal('${src}?t=${t}')">
    </div>`;
}

// 5. Utilitas
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
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("image", file);
  fetch("/upload-image", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      otsuImagePath = data.path;
      document.getElementById("otsuFileList").innerHTML =
        `<li><i class="fa-solid fa-file-image me-2 text-danger"></i> ${file.name}</li>`;
      saveOtsuState();
    });
}

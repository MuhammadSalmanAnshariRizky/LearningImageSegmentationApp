/**
 * Script untuk Live Code Notebook - Split & Merge Segmentation
 */

let splitMergeCellCount = 0;
let splitMergeEditors = {};
let splitMergeImagePath = "";

// 1. Inisiasi Lifecycle
document.addEventListener("DOMContentLoaded", function () {
  loadSplitMergeState();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          for (const id in splitMergeEditors) {
            if (splitMergeEditors[id]) splitMergeEditors[id].refresh();
          }
        }, 50);
      }
    });
  });
  const notebook = document.getElementById("splitMergeNotebook");
  if (notebook) observer.observe(notebook);
});

// 2. Sinkronisasi State Ke Local Storage
function saveSplitMergeState() {
  const cellsData = [];
  for (const id in splitMergeEditors) {
    cellsData.push({
      id: id,
      code: splitMergeEditors[id].getValue(),
      output: document.getElementById(`splitmerge-output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells_SplitMerge", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath_SplitMerge", splitMergeImagePath);

  const fileListElem = document.getElementById("splitMergeFileList");
  if (fileListElem) {
    localStorage.setItem("currentImageName_SplitMerge", fileListElem.innerHTML);
  }
  localStorage.setItem("cellCount_SplitMerge", splitMergeCellCount);
}

function loadSplitMergeState() {
  const savedCells = JSON.parse(
    localStorage.getItem("notebookCells_SplitMerge"),
  );
  const savedPath = localStorage.getItem("currentImagePath_SplitMerge");
  const savedImageUI = localStorage.getItem("currentImageName_SplitMerge");
  const savedCellCount = localStorage.getItem("cellCount_SplitMerge");

  if (savedPath && savedImageUI) {
    splitMergeImagePath = savedPath;
    document.getElementById("splitMergeFileList").innerHTML = savedImageUI;
  }
  if (savedCellCount) splitMergeCellCount = parseInt(savedCellCount);
  if (savedCells && savedCells.length > 0) {
    savedCells.forEach((cellData) => {
      createSplitMergeCellDOM(cellData.id, cellData.code, cellData.output);
    });
  }
}

// 3. Pembuatan Cell DOM & Struktur default Python Code
function addSplitMergeCell() {
  splitMergeCellCount++;

  // Mengintegrasikan kode program runtut sesuai dengan langkah instruksional materi
  const defaultCode = `import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. PARAMETER STRATEGIS SEGMENTASI
STD_THRESHOLD = 12.0
MIN_SIZE = 8
MIN_MEAN = 0
MAX_MEAN = 110
MERGE_THRESHOLD = 15.0

# 2. FUNGSI PENGECEKAN HOMOGENITAS REGION
def is_homogeneous(region):
    sigma = np.std(region)
    mean = np.mean(region)
    return (
        sigma < STD_THRESHOLD
        and MIN_MEAN < mean < MAX_MEAN
    )

# 3. ALGORITMA REGION SPLITTING (QUADTREE)
label_counter = 1
def split_region(img, labels, x, y, w, h):
    global label_counter
    region = img[y:y+h, x:x+w]
    
    # kondisi berhenti
    if (
        w <= MIN_SIZE
        or h <= MIN_SIZE
        or is_homogeneous(region)
    ):
        labels[y:y+h, x:x+w] = label_counter
        label_counter += 1
        return

    # split menjadi 4 bagian
    hw = w // 2
    hh = h // 2
    split_region(img, labels, x, y, hw, hh)
    split_region(img, labels, x + hw, y, w - hw, hh)
    split_region(img, labels, x, y + hh, hw, h - hh)
    split_region(img, labels, x + hw, y + hh, w - hw, h - hh)

# 4. ALGORITMA REGION MERGING
def merge_regions(img, labels):
    changed = True
    while changed:
        changed = False
        unique_labels = np.unique(labels)
        for label1 in unique_labels:
            mask1 = labels == label1
            if np.sum(mask1) == 0:
                continue
            mean1 = np.mean(img[mask1])
            dilated = cv2.dilate(
                mask1.astype(np.uint8),
                np.ones((3,3), np.uint8)
            )
            neighbors = np.unique(labels[dilated > 0])
            for label2 in neighbors:
                if label1 == label2:
                    continue
                mask2 = labels == label2
                if np.sum(mask2) == 0:
                    continue
                mean2 = np.mean(img[mask2])
                if abs(mean1 - mean2) < MERGE_THRESHOLD:
                    labels[mask2] = label1
                    changed = True
    return labels

# 5. MENENTUKAN CITRA BINER HASIL SEGMENTASI
def create_binary_segmentation(img, labels):
    output = np.zeros_like(img)
    unique_labels = np.unique(labels)
    for label in unique_labels:
        mask = labels == label
        mean_intensity = np.mean(img[mask])
        # kriteria filter objek gelap
        if mean_intensity < 120:
            output[mask] = 255
    return output

# 6. PROGRAM UTAMA (EXECUTION)
# Ganti parameter string di bawah dengan gambar kerja dari berkas workspace!
img = cv2.imread('_____', cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Gambar tidak ditemukan! Periksa kembali unggahan berkas gambar Anda.")
    exit()

# Inisialisasi label matriks nol
labels = np.zeros(img.shape, dtype=np.int32)

# Eksekusi Splitting & Merging
split_region(img, labels, 0, 0, img.shape[1], img.shape[0])
labels = merge_regions(img, labels)
segmented = create_binary_segmentation(img, labels)



# 8. MENYIMPAN VISUALISASI HASIL MATPLOTLIB
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Citra Asli')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(labels, cmap='nipy_spectral')
plt.title('Label Region')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(segmented, cmap='gray')
plt.title('Hasil Split and Merge')
plt.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "visualisasi_plt_splitmerge.jpg"))
plt.close()

print("Proses Segmentasi Split and Merge Sukses Dieksekusi!")
print(f"Total Kluster Region Unik Terbentuk: {len(np.unique(labels))}")`;

  createSplitMergeCellDOM(
    splitMergeCellCount,
    defaultCode,
    "Output Konsol Split & Merge muncul di sini...",
  );
  saveSplitMergeState();
}

function createSplitMergeCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("splitMergeNotebook");
  if (!container) return;

  const cell = document.createElement("div");
  cell.className = "cell";
  cell.id = "splitmerge-cell-" + id;
  cell.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small fw-bold">SplitMerge In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runSplitMergeCell(${id})" title="Run Code"><i class="fa-solid fa-play"></i></button>
                <button class="btn-icon delete" onclick="deleteSplitMergeCell(${id})" title="Hapus Cell"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>
        <textarea id="splitmerge-editor-${id}"></textarea>
        <div id="splitmerge-output-${id}" class="output-box">${outputHTML}</div>
    `;
  container.appendChild(cell);

  const editor = CodeMirror.fromTextArea(
    document.getElementById(`splitmerge-editor-${id}`),
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
    saveSplitMergeState();
  });
  splitMergeEditors[id] = editor;
}

// 4. Integrasi Backend Compilation
function runSplitMergeCell(id) {
  const code = splitMergeEditors[id].getValue();
  const outputBox = document.getElementById(`splitmerge-output-${id}`);
  outputBox.innerHTML =
    "⏳ Kompilasi Segmentasi Split & Merge Sedang Berjalan...";

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: splitMergeImagePath }),
  })
    .then((res) => res.json())
    .then((data) => {
      outputBox.innerHTML = `
            <div class="result-wrapper">
                <div class="console-output mb-3"><pre>${data.output}</pre></div>
                <div class="image-results d-flex gap-3 flex-wrap">
                    ${renderSplitMergeImgCard("Citra Asli", "/static/results/citra_asli_splitmerge.jpg")}
                    ${renderSplitMergeImgCard("Peta Label Region", "/static/results/visualisasi_plt_splitmerge.jpg")}
                    ${renderSplitMergeImgCard("Hasil Akhir Segmentasi", "/static/results/hasil_biner_splitmerge.jpg")}
                </div>
            </div>`;
      saveSplitMergeState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger">Terjadi kesalahan sistem kompilasi backend: ${err}</div>`;
    });
}

function renderSplitMergeImgCard(title, src) {
  const timestamp = Date.now();
  return `
    <div class="image-card text-center border p-2 rounded-3 bg-white">
        <h6 class="fw-bold text-secondary mb-2" style="font-size:0.8rem;">${title}</h6>
        <img src="${src}?t=${timestamp}" class="result-image preview-image img-fluid rounded" 
             style="max-height: 120px; cursor: pointer;"
             data-bs-toggle="modal" data-bs-target="#splitMergeImageModal" 
             onclick="openSplitMergeModal('${src}?t=${timestamp}')">
    </div>`;
}

// 5. Utilitas Sidebar Workspace & Modal Action
function openSplitMergeModal(src) {
  document.getElementById("splitMergeModalImage").src = src;
}

function deleteSplitMergeCell(id) {
  const cellElem = document.getElementById("splitmerge-cell-" + id);
  if (cellElem) cellElem.remove();
  delete splitMergeEditors[id];
  saveSplitMergeState();
}

function triggerSplitMergeUpload() {
  document.getElementById("splitMergeFileInput").click();
}

function handleSplitMergeUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("image", file);

  fetch("/upload-image", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      splitMergeImagePath = data.path;
      document.getElementById("splitMergeFileList").innerHTML =
        `<li><i class="fa-solid fa-file-image me-2 text-danger"></i> ${file.name}</li>`;
      saveSplitMergeState();
    });
}

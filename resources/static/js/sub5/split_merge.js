/**
 * Script untuk Live Code Notebook - Split & Merge Segmentation (Tanpa Matplotlib)
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
  if (fileListElem)
    localStorage.setItem("currentImageName_SplitMerge", fileListElem.innerHTML);
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
    savedCells.forEach((cellData) =>
      createSplitMergeCellDOM(cellData.id, cellData.code, cellData.output),
    );
  }
}

// 3. Pembuatan Cell DOM
function addSplitMergeCell() {
  splitMergeCellCount++;

  const defaultCode = `import cv2
import numpy as np
import os

# PARAMETER 
STD_THRESHOLD = 10     # Standar deviasi untuk deteksi homogenitas
MERGE_THRESHOLD = 20   # Toleransi kemiripan saat merge
MIN_SIZE = 4           # Ukuran minimum region

# PREDICATE HOMOGENITAS
def is_homogeneous(region):
    # Tuliskan 'std' pada numpy (np) untuk mencari nilai standar deviasi dari region
    sigma = np....(region)
    return sigma < STD_THRESHOLD

# QUADTREE SPLITTING
label_counter = 1
def split_region(img, labels, x, y, w, h):
    global label_counter
    region = img[y:y+h, x:x+w]
    
    if (w <= MIN_SIZE or h <= MIN_SIZE or is_homogeneous(region)):
        labels[y:y+h, x:x+w] = label_counter
        label_counter += 1
        return

    hw = w // 2
    hh = h // 2
    split_region(img, labels, x, y, hw, hh)
    split_region(img, labels, x + hw, y, w - hw, hh)
    split_region(img, labels, x, y + hh, hw, h - hh)
    split_region(img, labels, x + hw, y + hh, w - hw, h - hh)

# MERGING
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
            # Tuliskan 'dilate' untuk melebarkan area mask agar tetangga region bisa terdeteksi
            dilated = cv2....(mask1.astype(np.uint8), np.ones((3,3), np.uint8))
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

# MEMBUAT HASIL SEGMENTASI BINER
def create_binary_segmentation(img, labels):
    output = np.zeros_like(img)
    unique_labels = np.unique(labels)
    for label in unique_labels:
        mask = labels == label
        mean_intensity = np.mean(img[mask])
        
        if mean_intensity < 150: 
            output[mask] = 255
    return output

# MAIN PROGRAM
# 1. MEMBACA CITRA GRAYSCALE
# Tuliskan nama file gambar yang kamu unggah 
# lalu tuliskan 'cv2.imread' dan 'cv2.IMREAD_GRAYSCALE' untuk membaca sebagai hitam putih
img = cv2....('...', cv2....)

# Eksekusi Splitting & Merging
label_counter = 1 
labels = np.zeros(img.shape, dtype=np.int32)
split_region(img, labels, 0, 0, img.shape[1], img.shape[0])
labels = merge_regions(img, labels)
segmented = create_binary_segmentation(img, labels)

# POST-PROCESSING
# Tuliskan 'cv2.getStructuringElement' dan 'cv2.MORPH_ELLIPSE' untuk membuat struktur kernel elips ukuran 9x9
kernel = cv2....(cv2...., (9, 9))

# Tuliskan 'cv2.morphologyEx' dan 'cv2.MORPH_CLOSE' untuk membersihkan lubang kecil pada mask hasil segmentasi
segmented_clean = cv2....(segmented, cv2...., kernel)

# Tuliskan 'cv2.GaussianBlur' untuk menghaluskan tepi mask dengan ukuran kernel (15, 15)
blurred_mask = cv2....(segmented_clean, (15, 15), 0)

# Tuliskan 'cv2.threshold' dan 'cv2.THRESH_BINARY' untuk menegaskan kembali hasil blur menjadi mask biner tajam kembali
_, smooth_mask = cv2....(blurred_mask, 127, 255, cv2....)

# EKSTRAKSI GAMBAR DARI MASK
# Tuliskan 'cv2.bitwise_and' untuk memotong citra asli menggunakan mask yang sudah halus
extracted_img = cv2....(img, img, mask=smooth_mask)

# MENYIMPAN FISIK MATRIKS CITRA HASIL UNTUK WEB PREVIEW
if np.max(labels) > 0:
    labels_norm = np.uint8(255 * (labels / np.max(labels)))
else:
    labels_norm = np.uint8(labels)

# Tuliskan 'cv2.applyColorMap' dan 'cv2.COLORMAP_JET' untuk mewarnai label segmentasi agar bervariasi layaknya spektrum warna
visualisasi_label = cv2....(labels_norm, cv2....)

# Tuliskan 'cv2.imwrite' untuk menyimpan keempat citra hasil proses ke dalam direktori
cv2....(os.path.join(output_dir, "citra_asli_splitmerge.jpg"), img)
cv2....(os.path.join(output_dir, "visualisasi_label_splitmerge.jpg"), visualisasi_label)
cv2....(os.path.join(output_dir, "hasil_mask_splitmerge.jpg"), smooth_mask)
cv2....(os.path.join(output_dir, "hasil_ekstraksi_splitmerge.jpg"), extracted_img)

print("Proses Segmentasi Split and Merge Selesai Dijalankan!")
print(f"Total Kluster Region Unik Terbentuk: {len(np.unique(labels))}")`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createSplitMergeCellDOM(splitMergeCellCount, defaultCode, defaultOutput);
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
            <span class="text-muted small fw-bold">In [${id}]:</span>
            <div class="cell-actions">
                <button class="btn-icon run" onclick="runSplitMergeCell(${id})" title="Run">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteSplitMergeCell(${id})" title="Hapus">
                    <i class="fa-solid fa-trash"></i>
                </button>
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

  setTimeout(() => {
    editor.refresh();
  }, 10);

  editor.on("change", () => {
    editor.setSize(null, "auto");
    saveSplitMergeState();
  });
  splitMergeEditors[id] = editor;
}

// 4. Integrasi Backend Compilation
function runSplitMergeCell(id) {
  if (!splitMergeEditors[id]) return;

  const code = splitMergeEditors[id].getValue();
  const outputBox = document.getElementById(`splitmerge-output-${id}`);
  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Mengeksekusi penelusuran Split & Merge...</span>`;

  fetch("/run-code", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code, image_path: splitMergeImagePath }),
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
                <strong>✅ Hebat! Komputasi Split & Merge selesai:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>
            <div class="image-results d-flex gap-3 flex-wrap justify-content-start mt-3">
        `;

        if (data.images && Array.isArray(data.images)) {
          // --- PROSES SORTING URUTAN LOGIS DISINI ---
          const logicalOrder = ["asli", "label", "mask", "ekstraksi"];

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
              .replace("citra_asli", "Citra Asli")
              .replace("visualisasi_label", "Peta Label")
              .replace("hasil_mask", "Mask")
              .replace("hasil_ekstraksi", "Hasil Ekstraksi")
              .replace("_splitmerge", "");

            cleanTitle = cleanTitle.replace(/\b\w/g, (c) => c.toUpperCase());
            outputHTML += renderSplitMergeImgCard(cleanTitle, img.url);
          });
        } else {
          // Fallback Render Statis dengan Urutan yang Tepat
          outputHTML += renderSplitMergeImgCard(
            "Citra Asli",
            "/static/results/citra_asli_splitmerge.jpg",
          );
          outputHTML += renderSplitMergeImgCard(
            "Peta Label Split & Merge",
            "/static/results/visualisasi_label_splitmerge.jpg",
          );
          outputHTML += renderSplitMergeImgCard(
            "Mask Split & Merge",
            "/static/results/hasil_mask_splitmerge.jpg",
          );
          outputHTML += renderSplitMergeImgCard(
            "Hasil Ekstraksi Split & Merge",
            "/static/results/hasil_ekstraksi_splitmerge.jpg",
          );
        }

        outputHTML += `</div>`;
        outputBox.innerHTML = outputHTML;
      }
      saveSplitMergeState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<div class="text-danger font-monospace"><strong>🚨 Gagal terhubung ke server!</strong><br>${err.message}</div>`;
    });
}

function renderSplitMergeImgCard(title, srcUrl) {
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
                 data-bs-target="#splitMergeImageModal"
                 onclick="openSplitMergeModal('${urlWithCacheBuster}')">
        </div>

        <div class="text-muted mt-2"
             style="font-size: 0.7rem; cursor: pointer;"
             data-bs-toggle="modal"
             data-bs-target="#splitMergeImageModal"
             onclick="openSplitMergeModal('${urlWithCacheBuster}')">
            Klik gambar untuk memperbesar
        </div>
    </div>
`;
}

// 5. Utilitas Sidebar Workspace
function openSplitMergeModal(src) {
  document.getElementById("splitMergeModalImage").src = src;
}

function deleteSplitMergeCell(id) {
  document.getElementById("splitmerge-cell-" + id).remove();
  delete splitMergeEditors[id];
  saveSplitMergeState();
}

function triggerSplitMergeUpload() {
  document.getElementById("splitMergeFileInput").click();
}

function handleSplitMergeUpload(event) {
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_splitmerge" + extension;

  const reader = new FileReader();
  reader.onload = function (e) {
    const imageSrc = e.target.result;
    const formData = new FormData();

    formData.append("image", originalFile, newFileName);

    document.getElementById("splitMergeFileList").innerHTML = `
        <div class="text-center text-muted mt-3 small">
            <i class="fa-solid fa-spinner fa-spin me-2"></i>Mengunggah...
        </div>
    `;

    fetch("/upload-image", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
        splitMergeImagePath = data.path;

        document.getElementById("splitMergeFileList").innerHTML = `
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
        saveSplitMergeState();
      })
      .catch((err) => {
        document.getElementById("splitMergeFileList").innerHTML = `
            <div class="text-danger mt-3 small text-center">
                Gagal mengunggah gambar.
            </div>
        `;
      });
  };

  reader.readAsDataURL(originalFile);
}

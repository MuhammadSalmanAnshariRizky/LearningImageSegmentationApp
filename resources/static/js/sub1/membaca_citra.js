let cellCount = 0;
let editors = {};
let currentImagePath = "";

// 1. Fungsi untuk MEMUAT data saat halaman pertama kali dibuka
document.addEventListener("DOMContentLoaded", function () {
  loadState();

  // ==========================================
  // ✨ OBAT ANTI-HANCUR (INTERSECTION OBSERVER)
  // ==========================================
  // Deteksi jika area editor masuk ke dalam layar / menjadi terlihat
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Refresh semua editor yang ada dengan jeda super singkat
        setTimeout(() => {
          for (const id in editors) {
            editors[id].refresh();
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

// 2. Fungsi untuk MENYIMPAN semua state ke localStorage
function saveState() {
  const cellsData = [];
  for (const id in editors) {
    cellsData.push({
      id: id,
      code: editors[id].getValue(),
      output: document.getElementById(`output-${id}`).innerHTML,
    });
  }
  localStorage.setItem("notebookCells", JSON.stringify(cellsData));
  localStorage.setItem("currentImagePath", currentImagePath);
  localStorage.setItem(
    "currentImageName",
    document.getElementById("fileList").innerHTML,
  );
  localStorage.setItem("cellCount", cellCount);
}

// 3. Fungsi untuk MENGAMBIL data dari localStorage
function loadState() {
  const savedCells = JSON.parse(localStorage.getItem("notebookCells"));
  const savedPath = localStorage.getItem("currentImagePath");
  const savedImageUI = localStorage.getItem("currentImageName");
  const savedCellCount = localStorage.getItem("cellCount");

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

// 4. Tombol Add Cell diklik
function addCell() {
  cellCount++;

  // Menggunakan komentar yang singkat, padat, dan on-point
  const defaultCode = `# 1. Import library OpenCV (ketik: cv2)
import .....

# 2. Baca gambar sebagai grayscale (tuliskan fungsi membaca gambar yaitu: cv2.imread dan nama file: 'citra_input.png')
image = .....imread('.....', cv2.IMREAD_GRAYSCALE)

# 3. Tampilkan matriks piksel citra (tuliskan variabel: image)
print(.....)`;

  const defaultOutput = `<span class="text-success font-monospace">> Output akan muncul di sini...</span>`;

  createCellDOM(cellCount, defaultCode, defaultOutput);
  saveState();
}

// 5. Core logic untuk membangun elemen HTML Code Editor
function createCellDOM(id, codeText, outputHTML) {
  const container = document.getElementById("notebook");
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

  // ✨ TAMBAHAN OBAT: Pastikan cell baru langsung direfresh jika ditambahkan saat layar aktif
  setTimeout(() => {
    editor.refresh();
  }, 10);

  editor.on("change", function (cm) {
    cm.setSize(null, "auto");
    saveState();
  });

  editors[id] = editor;
}

// 6. Fungsi Run Code
function runCell(id) {
  const code = editors[id].getValue();
  const outputBox = document.getElementById(`output-${id}`);

  // Mengubah pesan loading menjadi lebih interaktif
  outputBox.innerHTML = `<span class="text-warning font-monospace"><i class="fa-solid fa-spinner fa-spin me-2"></i>⏳ Sedang memproses kodemu...</span>`;

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
    .then((res) => res.json())
    .then((data) => {
      // 1. Cek jika error dikirim secara eksplisit oleh backend
      if (data.error) {
        outputBox.innerHTML = `
            <div class="text-danger font-monospace">
                <strong>❌ Ups! Ada sedikit kesalahan di kodemu:</strong>
                <pre class="mt-2 mb-0 text-danger">${data.error}</pre>
            </div>`;
      }
      // 2. Cek jika output mengandung pesan error bawaan Python (Traceback, dll)
      else if (
        data.output &&
        (data.output.includes("Traceback (most recent call last):") ||
          data.output.includes("SyntaxError:") ||
          data.output.includes("NameError:"))
      ) {
        outputBox.innerHTML = `
            <div class="text-danger font-monospace">
                <strong>❌ Ups! Sepertinya ada kode yang kurang tepat. Coba periksa lagi ya:</strong>
                <pre class="mt-2 mb-0 text-danger">${data.output}</pre>
            </div>`;
      }
      // 3. Jika benar-benar bersih dari error
      else {
        outputBox.innerHTML = `
            <div class="text-success font-monospace">
                <strong>✅ Hebat! Kode berhasil dijalankan. Berikut hasilnya:</strong>
                <pre class="mt-2 mb-0 text-success">${data.output}</pre>
            </div>`;
      }
      saveState();
    })
    .catch((err) => {
      // Jika terjadi masalah pada sistem/jaringan
      outputBox.innerHTML = `
          <div class="text-danger font-monospace">
              <strong>🚨 Waduh, sistem gagal terhubung ke server. Coba periksa koneksi atau klik Run lagi ya!</strong>
              <br><span class="small">Detail sistem: ${err.message || err}</span>
          </div>`;
      saveState();
    });
}

// 7. Fungsi Hapus Cell
function deleteCell(id) {
  document.getElementById("cell-" + id).remove();
  delete editors[id];
  saveState();
}

// 8. Logika Upload Image & Preview
function triggerUpload() {
  document.getElementById("fileInput").click();
}
function handleUpload(event) {
  const originalFile = event.target.files[0];
  if (!originalFile) return;

  // 1. Tentukan Ekstensi dan Nama Baru
  const extension = originalFile.name.substring(
    originalFile.name.lastIndexOf("."),
  );
  const newFileName = "citra_input" + extension;

  // 2. Membaca file untuk dijadikan preview menggunakan FileReader
  const reader = new FileReader();

  reader.onload = function (e) {
    const imageSrc = e.target.result; // URL Base64 dari gambar

    const formData = new FormData();

    // ✨ TRIK AMPUH: Langsung paksa nama barunya di sini
    // Parameter ke-3 secara otomatis akan menimpa nama file asli saat dikirim ke Flask
    formData.append("image", originalFile, newFileName);

    // Ubah tampilan UI menjadi status 'Uploading...'
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

        // Render UI Preview Gambar
        // ✨ PERUBAHAN: Sekarang UI akan menampilkan newFileName (citra_grayscale)
        document.getElementById("fileList").innerHTML = `
                <div class="image-preview-card mt-3">
                    <div class="img-wrapper">
                        <img src="${imageSrc}" class="preview-img" alt="Preview File">
                    </div>
                    <div class="file-name-text mt-2 small text-truncate" title="${newFileName}">
                        <i class="fa-solid fa-file-image me-1 text-primary"></i>
                        ${newFileName}
                    </div>
                </div>
            `;
        saveState(); // Simpan UI preview ke localStorage
      })
      .catch((err) => {
        document.getElementById("fileList").innerHTML = `
                <div class="text-danger mt-3 small text-center">
                    Gagal mengunggah gambar.
                </div>
            `;
      });
  };

  // Eksekusi pembacaan file
  reader.readAsDataURL(originalFile);
}

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
  const defaultCode = `# 1. Inisiasi library OpenCV\nimport .....\n\n# 2. Membaca gambar dari file yang sudah di-upload\nimage = .....imread('.....')\n\n# 3. Menampilkan isi nilai piksel atau matriks citra\nprint(.....)`;
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

  outputBox.innerHTML = `<span class="text-warning font-monospace">⏳ Running...</span>`;

  fetch("http://127.0.0.1:5000/run-code", {
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
      outputBox.innerHTML = `<pre class="text-success font-monospace mb-0">${data.output}</pre>`;
      saveState();
    })
    .catch((err) => {
      outputBox.innerHTML = `<span class="text-danger font-monospace">Error: ${err}</span>`;
      saveState();
    });
}

// 7. Fungsi Hapus Cell
function deleteCell(id) {
  document.getElementById("cell-" + id).remove();
  delete editors[id];
  saveState();
}

// 8. Logika Upload Image
function triggerUpload() {
  document.getElementById("fileInput").click();
}

function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("image", file);

  fetch("http://127.0.0.1:5000/upload-image", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      currentImagePath = data.path;
      document.getElementById("fileList").innerHTML = `
            <li>
                <i class="fa-solid fa-file-image me-2 text-primary"></i>
                ${file.name}
            </li>
        `;
      saveState();
    });
}

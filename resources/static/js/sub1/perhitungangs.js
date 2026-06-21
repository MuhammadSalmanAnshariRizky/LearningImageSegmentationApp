let animInterval;
let currentRow = 0;
let currentCol = 0;
let isAnimating = false;
let isPaused = false;

// Data mentah matriks
const matrixR = [
  [110, 80, 90],
  [50, 60, 100],
  [20, 40, 120],
];
const matrixG = [
  [15, 20, 160],
  [10, 150, 80],
  [110, 50, 90],
];
const matrixB = [
  [120, 60, 80],
  [30, 140, 170],
  [80, 110, 100],
];

function startAnimation() {
  if (isAnimating && !isPaused) return;

  isAnimating = true;
  isPaused = false;

  // Atur tampilan tombol
  document.getElementById("btn-play").style.display = "none";
  document.getElementById("btn-pause").style.display = "inline-block";
  document.getElementById("btn-reset").disabled = false;

  // Jika mulai dari awal, jalankan piksel pertama langsung tanpa menunggu delay
  if (
    currentRow === 0 &&
    currentCol === 0 &&
    !document.querySelector(".highlight-res")
  ) {
    processNextPixel();
  }

  // Mulai interval 2.5 detik agar user punya waktu membaca proses
  animInterval = setInterval(processNextPixel, 2500);
}

function pauseAnimation() {
  isPaused = true;
  clearInterval(animInterval);

  // Ubah tampilan tombol kembali ke Lanjut
  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-play").style.display = "inline-block";
  document.getElementById("btn-play").innerHTML =
    '<i class="fa-solid fa-play me-1"></i> Lanjut';
}
function processNextPixel() {
  clearHighlights();

  // --- PERBAIKAN DI BAGIAN INI ---
  if (currentRow >= 3) {
    clearInterval(animInterval);
    isAnimating = false; // Kembalikan status animasi

    addLogToTerminal(
      '<span class="text-success fw-bold">✓ Selesai! Matriks berhasil dikonversi.</span>',
      "",
    );

    // Ubah tampilan tombol saat selesai
    document.getElementById("btn-pause").style.display = "none";

    let btnPlay = document.getElementById("btn-play");
    btnPlay.style.display = "inline-block";
    btnPlay.disabled = true; // Nonaktifkan tombol karena proses sudah selesai
    btnPlay.innerHTML = '<i class="fa-solid fa-check me-1"></i> Selesai';

    return;
  }
  // -------------------------------

  let rVal = matrixR[currentRow][currentCol];
  let gVal = matrixG[currentRow][currentCol];
  let bVal = matrixB[currentRow][currentCol];
  let minVal = Math.min(rVal, gVal, bVal);
  let maxVal = Math.max(rVal, gVal, bVal);
  let result = (minVal + maxVal) / 2;

  // Highlight Matriks
  document
    .getElementById(`r-${currentRow}-${currentCol}`)
    .classList.add("highlight-r");
  document
    .getElementById(`g-${currentRow}-${currentCol}`)
    .classList.add("highlight-g");
  document
    .getElementById(`b-${currentRow}-${currentCol}`)
    .classList.add("highlight-b");

  // Tambahkan ke Terminal Log dengan warna spesifik
  let logMsg = `
    <div class="mb-2 pb-2 border-bottom border-secondary">
      <div class="text-white fw-bold mb-1">[Baris ${currentRow}, Kolom ${currentCol}]</div>
      <div>
        min(<span class="text-danger fw-bold">${rVal}</span>, <span class="text-success fw-bold">${gVal}</span>, <span class="text-primary fw-bold">${bVal}</span>) = <span class="text-amber fw-bold">${minVal}</span>
      </div>
      <div>
        max(<span class="text-danger fw-bold">${rVal}</span>, <span class="text-success fw-bold">${gVal}</span>, <span class="text-primary fw-bold">${bVal}</span>) = <span class="text-cyan fw-bold">${maxVal}</span>
      </div>
      <div class="text-white mt-1">
        Grayscale = (${minVal} + ${maxVal}) / 2 = <span class="text-white fs-5 fw-bold bg-secondary px-2 rounded">${result}</span>
      </div>
    </div>`;
  addLogToTerminal(logMsg);

  // Update Hasil
  let resCell = document.getElementById(`res-${currentRow}-${currentCol}`);
  resCell.innerText = result;
  resCell.classList.add("highlight-res");

  setTimeout(() => {
    resCell.classList.remove("highlight-res");
    resCell.classList.add("done-res");
  }, 1800);

  currentCol++;
  if (currentCol >= 3) {
    currentCol = 0;
    currentRow++;
  }
}

// Fungsi pembantu untuk menambah log
function addLogToTerminal(html, extraClass = "") {
  const container = document.getElementById("process-log-container");
  if (document.getElementById("log-placeholder")) container.innerHTML = "";

  const div = document.createElement("div");
  div.className = "log-entry " + extraClass;
  div.innerHTML = html;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight; // Auto-scroll ke paling bawah
}

function clearHighlights() {
  const tds = document.querySelectorAll(".anim-matrix td");
  tds.forEach((td) => {
    td.classList.remove(
      "highlight-r",
      "highlight-g",
      "highlight-b",
      "highlight-res",
    );
  });
}
function resetAnimation() {
  clearInterval(animInterval);
  isAnimating = false;
  isPaused = false;
  currentRow = 0;
  currentCol = 0;

  clearHighlights();

  // Reset nilai di tabel hasil
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      let resCell = document.getElementById(`res-${i}-${j}`);
      resCell.innerText = "?";
      resCell.classList.remove("done-res");
    }
  }

  // Perbaikan: Reset Log Terminal ke kondisi awal beserta placeholdernya
  const logContainer = document.getElementById("process-log-container");
  if (logContainer) {
    logContainer.innerHTML =
      '<div id="log-placeholder" class="text-success mt-2">Klik tombol mulai untuk melihat perhitungan...</div>';
  }

  // (Opsional) Jika elemen process-box masih ada di HTML dan ingin dikosongkan juga
  const processBox = document.getElementById("process-box");
  if (processBox) {
    processBox.innerHTML = "";
  }

  // Reset UI dan Tombol
  let btnPlay = document.getElementById("btn-play");
  btnPlay.style.display = "inline-block";
  btnPlay.disabled = false;
  btnPlay.innerHTML = '<i class="fa-solid fa-play me-1"></i> Mulai';

  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-reset").disabled = true;
}

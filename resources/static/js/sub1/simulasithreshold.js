const initialValuesThresh = [
  100, 120, 130, 140, 90, 110, 150, 160, 80, 100, 120, 140, 70, 90, 110, 130,
];

// Ambil element menggunakan ID yang sudah dibuat unik
const inputContainerThresh = document.getElementById("input-matrix-thresh");
const resultContainerThresh = document.getElementById("result-matrix-thresh");
const logContainerThresh = document.getElementById("simulation-log-thresh");

let inputsThresh = [];
let resultsThresh = [];
const FIXED_THRESHOLD_VAL = 115;

let currentIdxThresh = 0;
let intervalThresh = null;
let isPlayingThresh = false;

// 1. Inisialisasi Grid Input dan Output dengan Koordinat (0, 1, 2, 3)
function initGridsThresh() {
  if (!inputContainerThresh || !resultContainerThresh) return;

  inputContainerThresh.innerHTML = "";
  resultContainerThresh.innerHTML = "";
  inputsThresh = [];
  resultsThresh = [];

  // Fungsi pembantu untuk membuat grid beserta label koordinatnya
  function buildGrid(container, isInput) {
    // Mengubah layout container menjadi 5 kolom (1 untuk label kiri, 4 untuk data)
    container.style.display = "grid";
    container.style.gridTemplateColumns = "auto repeat(4, 1fr)";
    // Jarak antar sel diperkecil dari 8px menjadi 3px
    container.style.gap = "3px";
    container.style.alignItems = "center";
    container.style.justifyItems = "center";

    // Bagian sudut kiri atas dibiarkan kosong
    container.appendChild(document.createElement("div"));

    // Render Koordinat Kolom (Atas: 0, 1, 2, 3)
    for (let c = 0; c < 4; c++) {
      const colLabel = document.createElement("div");
      // Dihapus fs-5, margin diperkecil (mb-1) agar lebih menempel dengan kotak
      colLabel.className = "fw-bold text-muted small mb-1";
      colLabel.innerText = c;
      container.appendChild(colLabel);
    }

    // Render Baris beserta Koordinat Baris
    for (let r = 0; r < 4; r++) {
      // Koordinat Baris (Kiri: 0, 1, 2, 3)
      const rowLabel = document.createElement("div");
      // Dihapus fs-5, margin diperkecil (me-1) agar lebih menempel dengan kotak
      rowLabel.className = "fw-bold text-muted small me-1";
      rowLabel.innerText = r;
      container.appendChild(rowLabel);

      // Data Sel (4x4)
      for (let c = 0; c < 4; c++) {
        const idx = r * 4 + c;
        const cell = document.createElement("div");

        if (isInput) {
          cell.className = "pixel-input shadow-sm";
          cell.innerText = initialValuesThresh[idx];
          inputsThresh.push(cell);
        } else {
          cell.className = "result-cell pixel-pending shadow-sm text-danger";
          cell.innerText = "?";
          resultsThresh.push(cell);
        }
        container.appendChild(cell);
      }
    }
  }

  buildGrid(inputContainerThresh, true);
  buildGrid(resultContainerThresh, false);
}
// 2. Logika Satu Langkah Simulasi
function stepSimThresh() {
  if (currentIdxThresh >= 16) {
    pauseSimThresh();
    addLogThresh(
      "✅ Proses Thresholding Selesai!",
      "text-success fw-bold text-center mt-3 border-0",
    );
    document.getElementById("btn-play-thresh").disabled = true;
    return;
  }

  if (currentIdxThresh > 0) {
    inputsThresh[currentIdxThresh - 1].classList.remove("highlight-active");
    resultsThresh[currentIdxThresh - 1].classList.remove("highlight-active");
  }

  const val = initialValuesThresh[currentIdxThresh];
  const baris = Math.floor(currentIdxThresh / 4);
  const kolom = currentIdxThresh % 4;

  inputsThresh[currentIdxThresh].classList.add("highlight-active");
  resultsThresh[currentIdxThresh].classList.add("highlight-active");

  let logMsg = `\\( f(${baris},${kolom}) \\) = ${val}. `;

  if (val > FIXED_THRESHOLD_VAL) {
    resultsThresh[currentIdxThresh].className =
      "result-cell pixel-1 highlight-active shadow-sm";
    resultsThresh[currentIdxThresh].innerText = "1";
    logMsg += `<span class="text-info fw-bold">${val} > ${FIXED_THRESHOLD_VAL}</span> ➔ Hasil: 1 (Putih)`;
  } else {
    resultsThresh[currentIdxThresh].className =
      "result-cell pixel-0 highlight-active shadow-sm";
    resultsThresh[currentIdxThresh].innerText = "0";
    logMsg += `<span class="text-danger fw-bold">${val} &le; ${FIXED_THRESHOLD_VAL}</span> ➔ Hasil: 0 (Hitam)`;
  }

  addLogThresh(logMsg);
  logContainerThresh.scrollTop = logContainerThresh.scrollHeight;
  currentIdxThresh++;
}

// 3. Tambahkan Teks ke Kotak Log & Render MathJax
function addLogThresh(htmlMessage, extraClasses = "") {
  if (currentIdxThresh === 0) logContainerThresh.innerHTML = "";

  const p = document.createElement("div");
  p.className = `log-entry ${extraClasses}`;
  p.innerHTML = htmlMessage;
  logContainerThresh.appendChild(p);

  if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
    MathJax.typesetPromise([p]).catch((err) =>
      console.log("MathJax error: ", err.message),
    );
  }
}

// 4. Pengendalian Tombol
function startSimThresh() {
  if (currentIdxThresh >= 16) resetSimThresh();

  if (!isPlayingThresh) {
    isPlayingThresh = true;

    document.getElementById("btn-play-thresh").style.display = "none";
    document.getElementById("btn-pause-thresh").style.display = "inline-block";

    intervalThresh = setInterval(stepSimThresh, 1000);

    if (currentIdxThresh === 0) {
      addLogThresh(
        "▶️ <em class='text-success'>Memulai proses seleksi piksel...</em>",
        "border-0",
      );
    }
  }
}

function pauseSimThresh() {
  isPlayingThresh = false;
  clearInterval(intervalThresh);

  document.getElementById("btn-pause-thresh").style.display = "none";
  document.getElementById("btn-play-thresh").style.display = "inline-block";
}

function resetSimThresh() {
  pauseSimThresh();
  currentIdxThresh = 0;

  inputsThresh.forEach((cell) => cell.classList.remove("highlight-active"));
  resultsThresh.forEach((cell) => {
    cell.className = "result-cell pixel-pending shadow-sm text-danger";
    cell.innerText = "?";
  });

  document.getElementById("btn-play-thresh").disabled = false;
  logContainerThresh.innerHTML = `<div class="text-success text-center mt-auto mb-auto" id="log-placeholder-thresh">Klik tombol "Mulai" untuk melihat proses seleksi per piksel...</div>`;
}

// 5. Inisialisasi Penuh Saat Web Dimuat
// Kita gunakan DOMContentLoaded agar aman jika ada script lain
document.addEventListener("DOMContentLoaded", () => {
  initGridsThresh();

  const btnPlayT = document.getElementById("btn-play-thresh");
  const btnPauseT = document.getElementById("btn-pause-thresh");
  const btnResetT = document.getElementById("btn-reset-thresh");

  if (btnPlayT) btnPlayT.addEventListener("click", startSimThresh);
  if (btnPauseT) btnPauseT.addEventListener("click", pauseSimThresh);
  if (btnResetT) btnResetT.addEventListener("click", resetSimThresh);
});

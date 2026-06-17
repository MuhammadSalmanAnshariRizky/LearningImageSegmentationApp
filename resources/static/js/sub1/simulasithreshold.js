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

// 1. Inisialisasi Grid Input (Statis) dan Output (Pending)
function initGridsThresh() {
  if (!inputContainerThresh || !resultContainerThresh) return; // Mencegah error jika div tidak ditemukan

  inputContainerThresh.innerHTML = "";
  resultContainerThresh.innerHTML = "";
  inputsThresh = [];
  resultsThresh = [];

  for (let i = 0; i < 16; i++) {
    const cellIn = document.createElement("div");
    cellIn.className = "pixel-input shadow-sm";
    cellIn.innerText = initialValuesThresh[i];
    inputContainerThresh.appendChild(cellIn);
    inputsThresh.push(cellIn);

    const cellOut = document.createElement("div");
    cellOut.className = "result-cell pixel-pending shadow-sm";
    cellOut.innerText = "?";
    resultContainerThresh.appendChild(cellOut);
    resultsThresh.push(cellOut);
  }
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
  const baris = Math.floor(currentIdxThresh / 4) + 1;
  const kolom = (currentIdxThresh % 4) + 1;

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
    cell.className = "result-cell pixel-pending shadow-sm";
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

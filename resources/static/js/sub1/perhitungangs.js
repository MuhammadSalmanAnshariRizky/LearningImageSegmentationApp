let animInterval;
let currentRow = 0;
let currentCol = 0;
let isAnimating = false;

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
  if (isAnimating) return;

  isAnimating = true;
  document.getElementById("btn-play").disabled = true;
  document.getElementById("btn-reset").disabled = false;

  // Mulai loop animasi setiap 2 detik (2000 ms) agar user sempat membaca
  animInterval = setInterval(processNextPixel, 2000);
  processNextPixel(); // Jalankan piksel pertama langsung
}

function processNextPixel() {
  // 1. Bersihkan highlight dari piksel sebelumnya
  clearHighlights();

  // Jika sudah mencapai ujung matriks (3x3), hentikan animasi
  if (currentRow >= 3) {
    clearInterval(animInterval);
    document.getElementById("process-box").innerHTML =
      `<span class="text-success"><i class="fa-solid fa-check-circle"></i> Selesai! Semua piksel berhasil dikonversi.</span>`;
    isAnimating = false;
    return;
  }

  // 2. Ambil nilai piksel saat ini
  let rVal = matrixR[currentRow][currentCol];
  let gVal = matrixG[currentRow][currentCol];
  let bVal = matrixB[currentRow][currentCol];

  // 3. Sorot (Highlight) sel di HTML
  document
    .getElementById(`r-${currentRow}-${currentCol}`)
    .classList.add("highlight-r");
  document
    .getElementById(`g-${currentRow}-${currentCol}`)
    .classList.add("highlight-g");
  document
    .getElementById(`b-${currentRow}-${currentCol}`)
    .classList.add("highlight-b");

  // 4. Lakukan perhitungan Lightness
  let minVal = Math.min(rVal, gVal, bVal);
  let maxVal = Math.max(rVal, gVal, bVal);
  let result = (minVal + maxVal) / 2;

  // 5. Tampilkan proses di Kotak Proses
  let processHTML = `
        <span class="text-light">Posisi (${currentRow}, ${currentCol}):</span><br>
        <span class="text-info">min</span>(<span class="text-danger">${rVal}</span>, <span class="text-success">${gVal}</span>, <span class="text-primary">${bVal}</span>) = <span class="text-warning">${minVal}</span> | 
        <span class="text-info">max</span>(<span class="text-danger">${rVal}</span>, <span class="text-success">${gVal}</span>, <span class="text-primary">${bVal}</span>) = <span class="text-warning">${maxVal}</span><br>
        <span class="text-white">(${minVal} + ${maxVal}) / 2 = </span><strong class="text-success fs-4">${result}</strong>
    `;
  document.getElementById("process-box").innerHTML = processHTML;

  // 6. Masukkan hasil ke matriks Grayscale
  let resCell = document.getElementById(`res-${currentRow}-${currentCol}`);
  resCell.innerText = result;
  resCell.classList.add("highlight-res");

  // Tambahkan class 'done-res' agar tetap punya warna setelah highlight hilang
  setTimeout(() => {
    resCell.classList.add("done-res");
  }, 1500);

  // 7. Pindah ke kolom/baris selanjutnya
  currentCol++;
  if (currentCol >= 3) {
    currentCol = 0;
    currentRow++;
  }
}

function clearHighlights() {
  // Hapus semua class highlight dari semua td
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
  currentRow = 0;
  currentCol = 0;

  clearHighlights();

  // Reset isi matriks hasil dan kotak proses
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      let resCell = document.getElementById(`res-${i}-${j}`);
      resCell.innerText = "?";
      resCell.classList.remove("done-res");
    }
  }

  document.getElementById("process-box").innerHTML =
    `<span class="text-muted">Klik tombol mulai untuk melihat perhitungan...</span>`;
  document.getElementById("btn-play").disabled = false;
  document.getElementById("btn-reset").disabled = true;
}

// Konfigurasi Algoritma Matriks 5x5
const matrix = [
  [1, 2, 6, 7, 8],
  [2, 3, 5, 8, 9],
  [6, 4, 3, 2, 1],
  [7, 8, 2, 1, 0],
  [9, 9, 3, 0, 1],
];
const rows = 5,
  cols = 5;
const seedR = 2,
  seedC = 2; // Berada tepat di tengah (nilai 3)
const seedVal = matrix[seedR][seedC];
const threshold = 2;

// 8-Connectivity Directions
const directions = [
  [-1, 0],
  [-1, 1],
  [0, 1],
  [1, 1],
  [1, 0],
  [1, -1],
  [0, -1],
  [-1, -1],
];

// State Kontrol
let isPlaying = false;
let isPaused = false;
let isReset = false;
let animSpeed = 800; // ms per langkah

const btnPlay = document.getElementById("btn-play");
const btnPause = document.getElementById("btn-pause");
const btnReset = document.getElementById("btn-reset");
const logContainer = document.getElementById("process-log-container");

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function writeLog(message, type = "normal") {
  const p = document.createElement("div");
  p.innerHTML = message;
  if (type === "success") p.className = "text-success fw-bold mt-2";
  else if (type === "error") p.className = "text-danger mt-2";
  else if (type === "warning") p.className = "text-warning mt-2";
  else p.className = "text-light mb-1 border-bottom border-secondary pb-1";

  logContainer.appendChild(p);
  logContainer.scrollTop = logContainer.scrollHeight;
}

async function checkState() {
  while (isPaused) {
    if (isReset) throw new Error("Reset");
    await sleep(100);
  }
  if (isReset) throw new Error("Reset");
}

async function startRegionGrowing() {
  let visited = Array.from({ length: rows }, () => Array(cols).fill(false));
  let queue = [{ r: seedR, c: seedC }];
  visited[seedR][seedC] = true;

  writeLog(
    `[INIT] Titik Benih (Seed) ditetapkan pada koordinat (${seedR}, ${seedC}) dengan nilai <b>${seedVal}</b>.`,
    "warning",
  );

  // Inisialisasi UI: Set isi tabel yang bukan seed menjadi ?
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      if (i === seedR && j === seedC) continue;
      document.getElementById(`out-${i}-${j}`).innerText = "?";
    }
  }

  while (queue.length > 0) {
    let current = queue.shift();
    writeLog(
      `<br><b>>>> Mengekspansi dari piksel (${current.r}, ${current.c}) bernilai ${matrix[current.r][current.c]}</b>`,
      "warning",
    );

    for (let dir of directions) {
      await checkState();
      let nr = current.r + dir[0];
      let nc = current.c + dir[1];

      // 1. Cek apakah koordinat berada di luar batas matriks
      if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
        writeLog(
          `Memeriksa tetangga (${nr}, ${nc}): <span class="text-secondary" style="font-size: 0.9em;">Di luar batas matriks.</span>`,
        );
        await sleep(animSpeed / 4); // Jeda singkat agar log bisa diikuti mata
        continue;
      }

      // 2. Cek apakah koordinat sudah pernah dikunjungi/diperiksa sebelumnya
      if (visited[nr][nc]) {
        writeLog(
          `Memeriksa tetangga (${nr}, ${nc}): <span class="text-secondary" style="font-size: 0.9em;">Sudah diperiksa sebelumnya.</span>`,
        );
        await sleep(animSpeed / 4); // Jeda singkat agar log bisa diikuti mata
        continue;
      }

      // 3. Jika valid dan belum dikunjungi, jalankan logika utama
      visited[nr][nc] = true;
      let neighborVal = matrix[nr][nc];

      // Sorot UI (Kuning saat dicek)
      const inCell = document.getElementById(`in-${nr}-${nc}`);
      const outCell = document.getElementById(`out-${nr}-${nc}`);
      inCell.classList.add("bg-checking");
      outCell.classList.add("bg-checking");

      let diff = Math.abs(neighborVal - seedVal);
      writeLog(
        `Memeriksa tetangga (${nr}, ${nc}) = ${neighborVal}. |${neighborVal} - ${seedVal}| = <b>${diff}</b>.`,
      );
      await sleep(animSpeed);
      await checkState();

      inCell.classList.remove("bg-checking");
      outCell.classList.remove("bg-checking");

      if (diff <= threshold) {
        writeLog(
          `↳ <span class="text-success">Memenuhi (\u2264 2). Diberi label 1 (Hitam).</span>`,
        );
        inCell.classList.add("bg-accepted");
        outCell.classList.add("bg-accepted");
        outCell.innerText = "1";
        queue.push({ r: nr, c: nc });
      } else {
        writeLog(
          `↳ <span class="text-danger">Ditolak (> 2). Diberi label 0 (Putih).</span>`,
        );
        inCell.classList.add("bg-rejected");
        outCell.classList.add("bg-rejected");
        outCell.innerText = "0";
      }
      await sleep(animSpeed / 2);
    }
  }

  // Akhir simulasi: ubah semua sisa '?' menjadi label '0' secara otomatis
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      if (!visited[i][j]) {
        const outC = document.getElementById(`out-${i}-${j}`);
        outC.innerText = "0";
        outC.classList.add("bg-rejected");
        document.getElementById(`in-${i}-${j}`).classList.add("bg-rejected");
      }
    }
  }

  writeLog(
    `<br><span class="text-success fw-bold fs-5"><i class="fa-solid fa-check-circle me-2"></i> Proses Segmentasi Region Growing Selesai!</span>`,
    "success",
  );
  uiFinished();
}

function startAnimation() {
  if (!isPlaying) {
    document.getElementById("log-placeholder")?.remove();
    logContainer.innerHTML = "";
    isPlaying = true;
    isReset = false;
    isPaused = false;
    toggleButtons(true, false);

    startRegionGrowing().catch((e) => {
      if (e.message !== "Reset") console.error(e);
    });
  } else if (isPaused) {
    isPaused = false;
    toggleButtons(true, false);
    writeLog("<i>Melanjutkan simulasi...</i>", "warning");
  }
}

function pauseAnimation() {
  isPaused = true;
  toggleButtons(false, true);
  writeLog("<i>Simulasi dijeda.</i>", "warning");
}

function resetAnimation() {
  isReset = true;
  isPlaying = false;
  isPaused = false;

  logContainer.innerHTML =
    '<div class="text-secondary text-center mt-5" id="log-placeholder">Menunggu inisiasi proses... Klik \'Mulai\'.</div>';

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const inCell = document.getElementById(`in-${i}-${j}`);
      const outCell = document.getElementById(`out-${i}-${j}`);

      inCell.className = "";
      outCell.className = "";

      if (i === seedR && j === seedC) {
        inCell.classList.add("bg-accepted");
        outCell.classList.add("bg-accepted");
        outCell.innerText = "1";
      } else {
        outCell.innerText = "?";
      }
    }
  }
  toggleButtons(false, false);
}

function uiFinished() {
  isPlaying = false;
  btnPlay.style.display = "none";
  btnPause.style.display = "none";
  btnReset.disabled = false;
}

function toggleButtons(playing, paused) {
  if (playing) {
    btnPlay.style.display = "none";
    btnPause.style.display = "block";
    btnReset.disabled = false;
  } else if (paused) {
    btnPlay.style.display = "block";
    btnPlay.innerHTML = '<i class="fa-solid fa-play me-1"></i> Lanjut';
    btnPause.style.display = "none";
  } else {
    btnPlay.style.display = "block";
    btnPlay.innerHTML = '<i class="fa-solid fa-play me-1"></i> Mulai';
    btnPause.style.display = "none";
    btnReset.disabled = true;
  }
}

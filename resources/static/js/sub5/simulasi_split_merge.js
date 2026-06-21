// Data Matriks 8x8
const matrix = [
  [5, 6, 6, 6, 7, 7, 6, 6],
  [6, 7, 6, 7, 5, 5, 4, 7],
  [6, 6, 4, 4, 3, 2, 5, 6],
  [5, 4, 5, 4, 2, 3, 4, 6],
  [0, 3, 2, 3, 3, 2, 4, 7],
  [0, 0, 0, 0, 2, 2, 5, 6],
  [1, 1, 0, 1, 0, 3, 4, 4],
  [1, 0, 1, 0, 2, 3, 5, 4],
];

const threshold = 3;
let isPlaying = false;
let isPaused = false;
let isReset = false;
let animSpeed = 1800; // ms

const btnPlay = document.getElementById("btn-play");
const btnPause = document.getElementById("btn-pause");
const btnReset = document.getElementById("btn-reset");
const logContainer = document.getElementById("process-log-container");

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Render awal matriks
function initMatrixUI() {
  const container = document.getElementById("matrix-container");
  container.innerHTML = "";

  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const cell = document.createElement("div");
      cell.className = "matrix-cell";
      cell.id = `cell-${r}-${c}`;
      cell.innerText = matrix[r][c];
      container.appendChild(cell);
    }
  }
}

function createLabel(id, text, rStart, rEnd, cStart, cEnd) {
  const container = document.getElementById("matrix-container");
  let label = document.createElement("div");
  label.id = "label-" + id;
  label.className = "region-label";
  label.innerText = text;

  label.style.gridRow = `${rStart + 1} / ${rEnd + 2}`;
  label.style.gridColumn = `${cStart + 1} / ${cEnd + 2}`;

  container.appendChild(label);
}

function removeLabel(id) {
  const label = document.getElementById("label-" + id);
  if (label) label.remove();
}

function writeLog(message, type = "normal") {
  const p = document.createElement("div");
  p.innerHTML = message;
  if (type === "success") p.className = "text-success fw-bold mt-2";
  else if (type === "error") p.className = "text-danger mt-2";
  else if (type === "warning") p.className = "text-warning mt-2";
  else if (type === "title")
    p.className =
      "text-info fw-bold mt-3 mb-1 border-bottom border-secondary pb-1 fs-6";
  else p.className = "text-light mb-1";

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

function getMinMax(rStart, rEnd, cStart, cEnd) {
  let min = Infinity,
    max = -Infinity;
  for (let r = rStart; r <= rEnd; r++) {
    for (let c = cStart; c <= cEnd; c++) {
      if (matrix[r][c] > max) max = matrix[r][c];
      if (matrix[r][c] < min) min = matrix[r][c];
    }
  }
  return { min, max };
}

function highlightRegion(
  rStart,
  rEnd,
  cStart,
  cEnd,
  className,
  remove = false,
) {
  for (let r = rStart; r <= rEnd; r++) {
    for (let c = cStart; c <= cEnd; c++) {
      const cell = document.getElementById(`cell-${r}-${c}`);
      if (remove) cell.classList.remove(className);
      else cell.classList.add(className);
    }
  }
}

function highlightMinMaxCells(blocks, minVal, maxVal) {
  blocks.forEach((blk) => {
    for (let r = blk.rs; r <= blk.re; r++) {
      for (let c = blk.cs; c <= blk.ce; c++) {
        let cell = document.getElementById(`cell-${r}-${c}`);
        if (matrix[r][c] === minVal) cell.classList.add("bg-min");
        if (matrix[r][c] === maxVal) cell.classList.add("bg-max");
      }
    }
  });
}

function clearMinMaxCells() {
  document.querySelectorAll(".bg-min, .bg-max").forEach((el) => {
    el.classList.remove("bg-min", "bg-max");
  });
}

function drawSplitLines() {
  for (let i = 0; i < 8; i++) {
    document.getElementById(`cell-3-${i}`).classList.add("border-bottom-thick");
    document.getElementById(`cell-${i}-3`).classList.add("border-right-thick");
  }
}

function drawSubSplitLines(rOffset, cOffset) {
  for (let i = 0; i < 4; i++) {
    document
      .getElementById(`cell-${rOffset + 1}-${cOffset + i}`)
      .classList.add("border-bottom-thick");
    document
      .getElementById(`cell-${rOffset + i}-${cOffset + 1}`)
      .classList.add("border-right-thick");
  }
}

// --- LOGIKA UTAMA SIMULASI ---
async function runSimulation() {
  writeLog("Memulai Proses Split and Merge...", "title");
  createLabel("ALL", "CITRA AWAL", 0, 7, 0, 7);
  await sleep(1000);

  // --- TAHAP 1: SEGMENTASI AWAL ---
  writeLog("<b>TAHAP 1: Menentukan Segmentasi Awal</b>", "title");
  let all = getMinMax(0, 7, 0, 7);
  highlightRegion(0, 7, 0, 7, "bg-checking");
  highlightMinMaxCells([{ rs: 0, re: 7, cs: 0, ce: 7 }], all.min, all.max);

  writeLog(
    `Cek seluruh citra. T<sub>max</sub> = <span class="text-warning">${all.max}</span>, T<sub>min</sub> = <span class="text-info">${all.min}</span>`,
  );
  await checkState();
  await sleep(animSpeed);

  let diff = all.max - all.min;
  writeLog(`|${all.max} - ${all.min}| = ${diff}`);
  if (diff > threshold) {
    writeLog(`Karena ${diff} > 3, Q(R<sub>i</sub>) = FALSE.`, "error");
    writeLog("Membagi citra menjadi 4 Region (A, B, C, D).", "warning");
    drawSplitLines();
  }

  clearMinMaxCells();
  highlightRegion(0, 7, 0, 7, "bg-checking", true);
  removeLabel("ALL");

  createLabel("A", "A", 0, 3, 0, 3);
  createLabel("B", "B", 0, 3, 4, 7);
  createLabel("C", "C", 4, 7, 0, 3);
  createLabel("D", "D", 4, 7, 4, 7);
  await checkState();
  await sleep(animSpeed);

  // --- TAHAP 2: SPLITTING ---
  writeLog("<b>TAHAP 2: Proses Splitting per Region</b>", "title");

  // Region A
  writeLog("<b>Mengecek Region (A):</b>");
  highlightRegion(0, 3, 0, 3, "bg-checking");
  let regA = getMinMax(0, 3, 0, 3);
  highlightMinMaxCells([{ rs: 0, re: 3, cs: 0, ce: 3 }], regA.min, regA.max);
  writeLog(
    `T<sub>max</sub> = <span class="text-warning">${regA.max}</span>, T<sub>min</sub> = <span class="text-info">${regA.min}</span> &rarr; Selisih = ${regA.max - regA.min}`,
  );
  await checkState();
  await sleep(animSpeed);
  writeLog(`&le; 3. Region A Homogen. Tidak perlu split.`, "success");
  clearMinMaxCells();
  highlightRegion(0, 3, 0, 3, "bg-checking", true);
  highlightRegion(0, 3, 0, 3, "bg-homogen");
  await checkState();
  await sleep(animSpeed);

  // Region B
  writeLog("<b>Mengecek Region (B):</b>");
  highlightRegion(0, 3, 4, 7, "bg-checking");
  let regB = getMinMax(0, 3, 4, 7);
  highlightMinMaxCells([{ rs: 0, re: 3, cs: 4, ce: 7 }], regB.min, regB.max);
  writeLog(
    `T<sub>max</sub> = <span class="text-warning">${regB.max}</span>, T<sub>min</sub> = <span class="text-info">${regB.min}</span> &rarr; Selisih = ${regB.max - regB.min}`,
  );
  await checkState();
  await sleep(animSpeed);
  writeLog(
    `> 3. Region B Tidak Homogen! Membagi ke (B1, B2, B3, B4).`,
    "error",
  );
  clearMinMaxCells();
  highlightRegion(0, 3, 4, 7, "bg-checking", true);
  highlightRegion(0, 3, 4, 7, "bg-heterogen");
  drawSubSplitLines(0, 4);

  removeLabel("B");
  createLabel("B1", "B1", 0, 1, 4, 5);
  createLabel("B2", "B2", 0, 1, 6, 7);
  createLabel("B3", "B3", 2, 3, 4, 5);
  createLabel("B4", "B4", 2, 3, 6, 7);
  await checkState();
  await sleep(animSpeed);

  // Region C
  writeLog("<b>Mengecek Region (C):</b>");
  highlightRegion(4, 7, 0, 3, "bg-checking");
  let regC = getMinMax(4, 7, 0, 3);
  highlightMinMaxCells([{ rs: 4, re: 7, cs: 0, ce: 3 }], regC.min, regC.max);
  writeLog(
    `T<sub>max</sub> = <span class="text-warning">${regC.max}</span>, T<sub>min</sub> = <span class="text-info">${regC.min}</span> &rarr; Selisih = ${regC.max - regC.min}`,
  );
  await checkState();
  await sleep(animSpeed);
  writeLog(`&le; 3. Region C Homogen. Tidak perlu split.`, "success");
  clearMinMaxCells();
  highlightRegion(4, 7, 0, 3, "bg-checking", true);
  highlightRegion(4, 7, 0, 3, "bg-homogen");
  await checkState();
  await sleep(animSpeed);

  // Region D
  writeLog("<b>Mengecek Region (D):</b>");
  highlightRegion(4, 7, 4, 7, "bg-checking");
  let regD = getMinMax(4, 7, 4, 7);
  highlightMinMaxCells([{ rs: 4, re: 7, cs: 4, ce: 7 }], regD.min, regD.max);
  writeLog(
    `T<sub>max</sub> = <span class="text-warning">${regD.max}</span>, T<sub>min</sub> = <span class="text-info">${regD.min}</span> &rarr; Selisih = ${regD.max - regD.min}`,
  );
  await checkState();
  await sleep(animSpeed);
  writeLog(
    `> 3. Region D Tidak Homogen! Membagi ke (D1, D2, D3, D4).`,
    "error",
  );
  clearMinMaxCells();
  highlightRegion(4, 7, 4, 7, "bg-checking", true);
  highlightRegion(4, 7, 4, 7, "bg-heterogen");
  drawSubSplitLines(4, 4);

  removeLabel("D");
  createLabel("D1", "D1", 4, 5, 4, 5);
  createLabel("D2", "D2", 4, 5, 6, 7);
  createLabel("D3", "D3", 6, 7, 4, 5);
  createLabel("D4", "D4", 6, 7, 6, 7);
  await checkState();
  await sleep(animSpeed);

  // --- PERUBAHAN DISINI: FUNGSI CEK SUB-REGION ---
  async function checkSubRegion(name, rStart, rEnd, cStart, cEnd) {
    writeLog(`<b>Mengecek Sub-region (${name}):</b>`);
    highlightRegion(rStart, rEnd, cStart, cEnd, "bg-checking");
    let reg = getMinMax(rStart, rEnd, cStart, cEnd);
    highlightMinMaxCells(
      [{ rs: rStart, re: rEnd, cs: cStart, ce: cEnd }],
      reg.min,
      reg.max,
    );

    let diff = reg.max - reg.min;
    writeLog(
      `T<sub>max</sub> = <span class="text-warning">${reg.max}</span>, T<sub>min</sub> = <span class="text-info">${reg.min}</span> &rarr; Selisih = ${diff}`,
    );

    await checkState();
    await sleep(animSpeed / 1.5); // Dipercepat sedikit agar animasi tidak terlalu membosankan

    if (diff <= threshold) {
      writeLog(`&le; 3. Sub-region ${name} Homogen.`, "success");
    } else {
      writeLog(`> 3. Sub-region ${name} Heterogen!`, "error");
    }

    clearMinMaxCells();
    highlightRegion(rStart, rEnd, cStart, cEnd, "bg-checking", true);

    // Setel sebagai homogen karena berdasarkan matriks Anda, sub-region ini bernilai homogen
    highlightRegion(rStart, rEnd, cStart, cEnd, "bg-homogen");
    await checkState();
    await sleep(animSpeed / 2);
  }

  // Hapus warna merah (heterogen) dari Region B dan D sebelum mulai mengecek satu per satu
  highlightRegion(0, 3, 4, 7, "bg-heterogen", true);
  highlightRegion(4, 7, 4, 7, "bg-heterogen", true);

  writeLog("<b>Mengecek Sub-region dari B secara detail:</b>", "title");
  await checkSubRegion("B1", 0, 1, 4, 5);
  await checkSubRegion("B2", 0, 1, 6, 7);
  await checkSubRegion("B3", 2, 3, 4, 5);
  await checkSubRegion("B4", 2, 3, 6, 7);

  writeLog("<b>Mengecek Sub-region dari D secara detail:</b>", "title");
  await checkSubRegion("D1", 4, 5, 4, 5);
  await checkSubRegion("D2", 4, 5, 6, 7);
  await checkSubRegion("D3", 6, 7, 4, 5);
  await checkSubRegion("D4", 6, 7, 6, 7);
  // --- AKHIR PERUBAHAN ---

  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      document.getElementById(`cell-${r}-${c}`).classList.remove("bg-homogen");
    }
  }

  // --- TAHAP 3: MERGING ---
  writeLog(
    "<b>TAHAP 3: Pengecekan Dua Region Bertetangga (Merging)</b>",
    "title",
  );

  let currentMergedBlocks = [{ rs: 0, re: 3, cs: 0, ce: 3, id: "A" }];
  highlightRegion(0, 3, 0, 3, "bg-merged");

  async function tryMerge(rStart, rEnd, cStart, cEnd, targetName) {
    writeLog(`<b>Pengecekan Region Gabungan dengan Region ${targetName}</b>`);
    highlightRegion(rStart, rEnd, cStart, cEnd, "bg-checking");

    let blocksToCheck = [
      ...currentMergedBlocks,
      { rs: rStart, re: rEnd, cs: cStart, ce: cEnd },
    ];
    let min = Infinity,
      max = -Infinity;

    blocksToCheck.forEach((blk) => {
      let mm = getMinMax(blk.rs, blk.re, blk.cs, blk.ce);
      if (mm.max > max) max = mm.max;
      if (mm.min < min) min = mm.min;
    });

    highlightMinMaxCells(blocksToCheck, min, max);

    let diff = max - min;
    writeLog(
      `T<sub>max</sub> gabungan = <span class="text-warning">${max}</span>, T<sub>min</sub> gabungan = <span class="text-info">${min}</span>`,
    );
    writeLog(`|${max} - ${min}| = ${diff}`);
    await checkState();
    await sleep(animSpeed);

    if (diff <= threshold) {
      writeLog(
        `<span class="text-success">Memenuhi (\u2264 3). Proses MERGE dilakukan.</span>`,
      );
      highlightRegion(rStart, rEnd, cStart, cEnd, "bg-checking", true);
      highlightRegion(rStart, rEnd, cStart, cEnd, "bg-merged");
      currentMergedBlocks.push({
        rs: rStart,
        re: rEnd,
        cs: cStart,
        ce: cEnd,
        id: targetName,
      });
      document.getElementById("label-" + targetName).style.color =
        "rgba(0, 64, 133, 0.4)";
      document.getElementById("label-A").style.color = "rgba(0, 64, 133, 0.4)";
    } else {
      writeLog(
        `<span class="text-danger">Tidak Memenuhi (> 3). TIDAK dapat di merge.</span>`,
      );
      highlightRegion(rStart, rEnd, cStart, cEnd, "bg-checking", true);
    }

    clearMinMaxCells();
    await checkState();
    await sleep(animSpeed / 2);
  }

  await tryMerge(0, 1, 4, 5, "B1");
  await tryMerge(0, 1, 6, 7, "B2");
  await tryMerge(2, 3, 4, 5, "B3");
  await tryMerge(2, 3, 6, 7, "B4");
  await tryMerge(4, 7, 0, 3, "C");
  await tryMerge(4, 5, 4, 5, "D1");
  await tryMerge(4, 5, 6, 7, "D2");
  await tryMerge(6, 7, 4, 5, "D3");
  await tryMerge(6, 7, 6, 7, "D4");

  writeLog(
    '<br><span class="text-success fs-5"><i class="fa-solid fa-check-circle"></i> Segmentasi Selesai!</span>',
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

    initMatrixUI();
    runSimulation().catch((e) => {
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
    '<div class="text-secondary text-center mt-5" id="log-placeholder">Menunggu inisiasi proses... Klik \'Mulai Simulasi\'.</div>';
  initMatrixUI();
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
    btnPause.style.display = "inline-block";
    btnReset.disabled = false;
  } else if (paused) {
    btnPlay.style.display = "inline-block";
    btnPlay.innerHTML = '<i class="fa-solid fa-play me-1"></i> Lanjut';
    btnPause.style.display = "none";
  } else {
    btnPlay.style.display = "inline-block";
    btnPlay.innerHTML = '<i class="fa-solid fa-play me-1"></i> Mulai Simulasi';
    btnPause.style.display = "none";
    btnReset.disabled = true;
  }
}

window.onload = initMatrixUI;

// 🔥 9 WARNA GELAP (FIX)
const fixedColors = [
  "#020617",
  "#1e293b",
  "#334155",
  "#450a0a",
  "#7f1d1d",
  "#991b1b",
  "#052e16",
  "#14532d",
  "#166534",
];

// ===============================
// 🔥 CREATE INPUT GRID
// ===============================
function createInputGrid() {
  const grid = document.getElementById("inputGrid");
  grid.innerHTML = "";

  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "repeat(3, 100px)";
  grid.style.gap = "15px";
  grid.style.justifyContent = "center";

  let index = 0;

  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      const wrapper = document.createElement("div");

      wrapper.innerHTML = `
        <label class="small text-muted d-block text-center">(${i},${j})</label>
        <input 
          type="number" 
          min="0" 
          max="255" 
          class="form-control text-center pixel-input"
          placeholder="0-255"
          data-index="${index}"
        >
      `;

      grid.appendChild(wrapper);
      index++;
    }
  }

  // 🔥 EVENT: warna input mengikuti fixed color
  document.querySelectorAll(".pixel-input").forEach((input) => {
    input.addEventListener("input", function () {
      const value = parseInt(this.value);
      const idx = parseInt(this.dataset.index);

      if (!isNaN(value) && value >= 0 && value <= 255) {
        this.style.background = fixedColors[idx];
        this.style.color = "white";
      } else {
        this.style.background = "";
        this.style.color = "";
      }
    });
  });
}

// ===============================
// 🔥 CREATE PIXEL GRID
// ===============================
function createPixelGrid() {
  const grid = document.getElementById("pixelGrid");
  grid.innerHTML = "";

  let container = document.createElement("div");
  container.style.display = "grid";
  container.style.gridTemplateColumns = "repeat(3, 70px)";
  container.style.gap = "12px";
  container.style.justifyContent = "center";

  for (let i = 0; i < 9; i++) {
    let box = document.createElement("div");
    box.className = "pixel-box";
    box.id = "pixel-" + i;
    container.appendChild(box);
  }

  grid.appendChild(container);
}

// ===============================
// 🔥 VALIDASI
// ===============================
function validateInputs(inputs) {
  for (let input of inputs) {
    let val = input.value;

    if (val === "") return "Semua input harus diisi!";
    if (isNaN(val)) return "Hanya angka yang diperbolehkan!";
    if (val < 0 || val > 255) return "Nilai harus antara 0–255!";
  }
  return null;
}

// ===============================
// 🔥 SIMULASI
// ===============================
function startSimulation() {
  const inputs = document.querySelectorAll(".pixel-input");
  const error = document.getElementById("errorMsg");

  error.innerHTML = "";

  const validation = validateInputs(inputs);
  if (validation) {
    error.innerHTML = "⚠️ " + validation;
    return;
  }

  createPixelGrid();

  inputs.forEach((input, index) => {
    const value = parseInt(input.value);
    const target = document.getElementById("pixel-" + index);

    const color = fixedColors[index];

    setTimeout(() => {
      target.classList.remove("show");

      setTimeout(() => {
        target.style.background = color;
        target.style.color = "white";

        target.innerHTML = `<span class="pixel-text text-center">${value}</span>`;

        target.classList.add("show");
      }, 80);
    }, index * 150);
  });
}

// ===============================
// 🔥 INIT
// ===============================
window.onload = function () {
  createInputGrid();
};

// Simulasi Matriks Citra dengan MathJax
function generateMatrixMathJax() {
  const M = parseInt(document.getElementById("inputM").value);
  const N = parseInt(document.getElementById("inputN").value);

  const output = document.getElementById("outputUkuran");
  const mathOutput = document.getElementById("mathjaxOutput");
  const narasi = document.getElementById("narasiMatrix");

  if (!M || !N || M <= 0 || N <= 0) {
    output.innerHTML = "⚠️ Input tidak valid";
    return;
  }

  output.innerHTML = `Ukuran citra: <strong>${M} × ${N}</strong>`;

  let matrix = "";

  for (let i = 0; i < M; i++) {
    let row = [];
    for (let j = 0; j < N; j++) {
      let value = `f(${i},${j})`;

      // 🔥 HIGHLIGHT BAGIAN PENTING
      if (i === 0 && j === 0) {
        value = `\\color{red}{f(0,0)}`; // pojok kiri atas
      } else if (i === 0 && j === N - 1) {
        value = `\\color{red}{f(0,${N - 1})}`; // ujung baris pertama
      } else if (i === M - 1 && j === 0) {
        value = `\\color{green}{f(${M - 1},0)}`; // awal baris terakhir
      } else if (i === M - 1 && j === N - 1) {
        value = `\\color{green}{f(${M - 1},${N - 1})}`; // pojok kanan bawah
      }

      row.push(value);
    }

    matrix += row.join(" & ");
    if (i < M - 1) matrix += " \\\\ ";
  }

  const latex = `
    \\[
    f(x,y)=
    \\begin{bmatrix}
    ${matrix}
    \\end{bmatrix}
    \\]
  `;

  mathOutput.innerHTML = latex;

  // 🔥 NARASI DINAMIS
  narasi.innerHTML = `
    <div class="card border-0 bg-light p-3">
      <p>
        Pada matriks citra digital tersebut terdapat dua ukuran utama, yaitu 
        <strong>M = ${M}</strong> dan <strong>N = ${N}</strong>. 
        Nilai M menunjukkan jumlah baris, sedangkan N menunjukkan jumlah kolom.
        Ukuran citra dituliskan sebagai <strong>${M} × ${N}</strong>.
      </p>

      <p>
        Indeks koordinat dimulai dari <strong>0</strong>, sehingga piksel pertama berada pada 
        <span class="text-danger fw-bold">f(0,0)</span>.
      </p>

      <p>
        Piksel pada baris pertama: 
        <span class="text-danger">f(0,0)</span> hingga 
        <span class="text-danger">f(0,${N - 1})</span>.
      </p>

      <p>
        Piksel pada baris terakhir: 
        <span class="text-success">f(${M - 1},0)</span> hingga 
        <span class="text-success">f(${M - 1},${N - 1})</span>.
      </p>
    </div>
  `;

  // 🔥 render MathJax ulang
  if (window.MathJax) {
    MathJax.typesetPromise([mathOutput]);
  }
}


let soalData = [];
let indexSoal = 0;
let sudahBenar = false;

/* LOAD DARI DATABASE */
const activityId = document.getElementById("quizContainer").dataset.activity;
async function loadSoal() {
  const res = await fetch(`/api/soal/${activityId}`); // activity id
  soalData = await res.json();

  tampilSoal();
}

/* SHUFFLE */
function shuffle(array) {
  return array.sort(() => Math.random() - 0.5);
}

/* TAMPILKAN SOAL */
function tampilSoal() {
  const data = soalData[indexSoal];

  const container = document.getElementById("quizContainer");
  const progress = document.getElementById("quizProgress");
  const feedback = document.getElementById("feedback");

  progress.innerHTML = `Pertanyaan ${indexSoal + 1} dari ${soalData.length}`;

  sudahBenar = false;
  feedback.innerHTML = "";
  document.getElementById("nextBtn").disabled = true;

  let opsi = shuffle(Object.entries(data.opsi));

  let html = `<h6 class="mb-3 fw-semibold">${data.soal}</h6>`;

  opsi.forEach(([key, val]) => {
    html += `
      <div class="option-box" data-key="${key}">
        ${val}
      </div>
    `;
  });

  container.innerHTML = html;
  if (window.MathJax) {
    MathJax.typesetPromise();
  }
  document.querySelectorAll(".option-box").forEach((el) => {
    el.addEventListener("click", () => pilihJawaban(el));
  });
}

/* PILIH JAWABAN */
function pilihJawaban(el) {
  if (sudahBenar) return;

  const pilihan = el.dataset.key;
  const data = soalData[indexSoal];
  const feedback = document.getElementById("feedback");

  if (pilihan === data.jawaban) {
    el.classList.add("correct");
    feedback.innerHTML = "✅ Jawaban benar!";
    feedback.style.color = "#16a34a";

    sudahBenar = true;

    document.querySelectorAll(".option-box").forEach((o) => {
      o.style.pointerEvents = "none";
      o.style.opacity = "0.8";
    });

    document.getElementById("nextBtn").disabled = false;
  } else {
    el.classList.add("wrong");
    feedback.innerHTML = "❌ Jawaban salah, coba lagi!";
    feedback.style.color = "#dc2626";
  }
}

/* NEXT */
document.getElementById("nextBtn").addEventListener("click", () => {
  if (!sudahBenar) return;

  indexSoal++;

  if (indexSoal < soalData.length) {
    tampilSoal();
  } else {
    selesaiQuiz();
  }
});

/* SELESAI */
function selesaiQuiz() {
  document.getElementById("quizContainer").innerHTML = `
    <h5 class="text-success">Aktivitas selesai!</h5>
    <p class="text-muted">Kamu telah menyelesaikan semua soal.</p>
  `;

  document.getElementById("feedback").innerHTML = "";
  document.getElementById("nextBtn").style.display = "none";
  document.getElementById("ulangBtn").classList.remove("d-none");
}

/* ULANG */
document.getElementById("ulangBtn").addEventListener("click", () => {
  indexSoal = 0;

  document.getElementById("nextBtn").style.display = "inline-block";
  document.getElementById("ulangBtn").classList.add("d-none");

  tampilSoal();
});

/* INIT */
loadSoal();

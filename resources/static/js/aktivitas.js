let soalData = [];
let indexSoal = 0;
let sudahBenar = false;

/* =========================
   LOAD SOAL DARI API
========================= */
const quizContainer = document.getElementById("quizContainer");
const activityId = quizContainer.dataset.activity;

async function loadSoal() {
  try {
    const res = await fetch(`/api/soal/${activityId}`);
    soalData = await res.json();
    console.log("Data soal:", soalData);
    if (!soalData || soalData.length === 0) {
      quizContainer.innerHTML = `
        <div class="alert alert-warning">
          Soal belum tersedia.
        </div>
      `;
      return;
    }

    tampilSoal();
  } catch (err) {
    console.error(err);

    quizContainer.innerHTML = `
      <div class="alert alert-danger">
        Gagal memuat soal.
      </div>
    `;
  }
}

/* =========================
   SHUFFLE OPSI
========================= */
function shuffle(array) {
  return [...array].sort(() => Math.random() - 0.5);
}

/* =========================
   TAMPILKAN SOAL
========================= */
/* =========================
   TAMPILKAN SOAL
========================= */
function tampilSoal() {
  const data = soalData[indexSoal];

  const progress = document.getElementById("quizProgress");
  const feedback = document.getElementById("feedback");
  const nextBtn = document.getElementById("nextBtn");

  progress.innerHTML = `Pertanyaan ${indexSoal + 1} dari ${soalData.length}`;

  feedback.innerHTML = "";
  sudahBenar = false;
  nextBtn.disabled = true;

  let html = `
    <div class="mb-4">
        <h5 class="quiz-question-text fw-semibold">
          ${data.soal}
        </h5>
    </div>
  `;

  if (data.URL) {
    html += `
      <div class="text-center mb-4">
        <img
          src="${data.URL}"
          alt="Gambar ilustrasi soal"
          class="img-fluid shadow-sm border img-soal"
        >
      </div>
    `;
  }

  let opsi = shuffle(Object.entries(data.opsi));

  html += `<div class="d-flex flex-column gap-3">`;

  // Tambahkan 'index' ke dalam forEach
  opsi.forEach(([key, value], index) => {
    // Mengubah index (0, 1, 2...) menjadi huruf (A, B, C...)
    let huruf = String.fromCharCode(65 + index);

    html += `
      <div class="option-box p-3 rounded-4" data-key="${key}">
        <div class="option-letter">${huruf}</div>
        <div class="option-text">${value}</div>
      </div>
    `;
  });

  html += `</div>`;

  quizContainer.innerHTML = html;

  if (window.MathJax) {
    MathJax.typesetPromise();
  }

  document.querySelectorAll(".option-box").forEach((item) => {
    item.addEventListener("click", function () {
      if (!sudahBenar && !this.classList.contains("disabled")) {
        pilihJawaban(this);
      }
    });
  });
}

/* =========================
   PILIH JAWABAN
========================= */
function pilihJawaban(el) {
  if (sudahBenar) return;

  const pilihan = el.dataset.key;
  const data = soalData[indexSoal];

  const feedback = document.getElementById("feedback");
  const nextBtn = document.getElementById("nextBtn");

  /* RESET SALAH SEBELUMNYA */
  document.querySelectorAll(".option-box").forEach((o) => {
    o.classList.remove("wrong");
  });

  /* JAWABAN BENAR */
  if (pilihan === data.jawaban) {
    sudahBenar = true;
    el.classList.add("correct");
    nextBtn.disabled = false;

    // Feedback Modern untuk Jawaban Benar
    feedback.innerHTML = `
      <div class="feedback-alert correct-alert">
        <i class="fa-solid fa-circle-check feedback-icon"></i>
        <div>
          <span class="d-block fw-bold">Tepat Sekali!</span>
          <span class="text-muted" style="font-size: 0.95rem;">Jawabanmu sudah benar. Silakan lanjut ke soal berikutnya.</span>
        </div>
      </div>
    `;

    document.querySelectorAll(".option-box").forEach((o) => {
      o.classList.add("disabled");
    });
  } else {
    /* JAWABAN SALAH */
    el.classList.add("wrong");

    // Feedback Modern untuk Jawaban Salah
    feedback.innerHTML = `
      <div class="feedback-alert wrong-alert">
        <i class="fa-solid fa-circle-xmark feedback-icon"></i>
        <div>
          <span class="d-block fw-bold">Yah, Masih Kurang Tepat!</span>
          <span class="text-muted" style="font-size: 0.95rem;">Jangan menyerah, coba pilih opsi yang lain.</span>
        </div>
      </div>
    `;
  }
}

/* =========================
   NEXT SOAL
========================= */
document.getElementById("nextBtn").addEventListener("click", () => {
  if (!sudahBenar) return;

  indexSoal++;

  if (indexSoal < soalData.length) {
    tampilSoal();
  } else {
    selesaiQuiz();
  }
});

/* =========================
   SELESAI QUIZ
========================= */
function selesaiQuiz() {
  // =========================
  // UPDATE PROGRESS
  // =========================
  fetch("/update-progress", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      activity_id: activityId,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      Swal.fire({
        icon: "success",
        title: "Aktivitas Selesai!",
        text: "Progress belajar berhasil diperbarui.",
        confirmButtonColor: "#0d6efd",
        confirmButtonText: "Lanjut",
      }).then(() => {
        // reload halaman agar progress langsung update
        location.reload();
      });
    })
    .catch((err) => {
      console.error("Gagal update progress:", err);

      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Gagal memperbarui progress.",
      });
    });

  // =========================
  // TAMPILAN SELESAI
  // =========================
  document.getElementById("quizContainer").innerHTML = `
    <div class="text-center py-5">

      <div class="mb-4">
        <i class="fa-solid fa-circle-check text-success"
           style="font-size:70px;"></i>
      </div>

      <h3 class="fw-bold text-success">
        Aktivitas Selesai!
      </h3>

      <p class="text-muted">
        Kamu telah menyelesaikan semua soal.
      </p>

    </div>
  `;

  document.getElementById("feedback").innerHTML = "";

  document.getElementById("nextBtn").style.display = "none";

  document.getElementById("ulangBtn").classList.remove("d-none");
}
/* =========================
   ULANG QUIZ
========================= */
document.getElementById("ulangBtn").addEventListener("click", () => {
  indexSoal = 0;

  document.getElementById("nextBtn").style.display = "inline-block";

  document.getElementById("ulangBtn").classList.add("d-none");

  tampilSoal();
});

/* =========================
   INIT
========================= */
loadSoal();

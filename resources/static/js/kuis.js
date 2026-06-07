// ================= AMBIL DATA DARI HTML =================
const formEl = document.getElementById("quizForm");
const activityTitle = formEl.dataset.title;
const activityId = formEl.dataset.id;

// 🔥 KEY (Menggunakan variabel JS murni)
const STORAGE_KEY = `aktivitas_${activityId}`;
const SESSION_FLAG = `is_exam_${activityId}`;

let questions = [];
let currentIdx = 1;
const timerEl = document.getElementById("timer");
let duration = parseInt(timerEl.dataset.duration); // menit dari backend
let timeLeft = duration * 60;
let correctMap = {}; // 🔥 WAJIB

// ================= STATE =================
let userAnswers = {};
let raguState = {};
let questionOrder = [];

// ================= SESSION GUARD =================
if (!sessionStorage.getItem(SESSION_FLAG)) {
  localStorage.removeItem(STORAGE_KEY);
}
sessionStorage.setItem(SESSION_FLAG, "active");

// ================= DETEKSI BACK / FORWARD =================
window.addEventListener("pageshow", function (event) {
  if (event.persisted) {
    localStorage.removeItem(STORAGE_KEY);
    location.reload();
  }
});

// ================= TIMER =================
let timerInterval = null;

function startTimer() {
  const tEl = document.getElementById("timer");

  tEl.innerText = formatTime(timeLeft);

  timerInterval = setInterval(() => {
    if (timeLeft <= 0) return;

    timeLeft--;
    tEl.innerText = formatTime(timeLeft);
    saveState();
  }, 1000);
}

function formatTime(seconds) {
  let m = Math.floor(seconds / 60);
  let s = seconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

// ================= LOAD =================
async function loadQuestions() {
  try {
    const res = await fetch(`/api/kuis/${encodeURIComponent(activityTitle)}`);

    if (!res.ok) {
      throw new Error(`Data tidak ditemukan (Status: ${res.status})`);
    }

    const data = await res.json();
    const mapData = {};

    data.forEach((q) => {
      mapData[q.id] = q;
      correctMap[q.id] = q.correct_key; // SIMPAN KUNCI JAWABAN
    });

    const saved = localStorage.getItem(STORAGE_KEY);

    if (saved) {
      const parsed = JSON.parse(saved);

      questionOrder = parsed.order || [];
      userAnswers = parsed.answers || {};
      raguState = parsed.ragu || {};
      currentIdx = parsed.current || 1;
      timeLeft = parsed.time || duration * 60;

      questions = questionOrder.map((id) => mapData[id]).filter((q) => q);

      if (questions.length !== questionOrder.length) {
        resetQuestions(data, mapData);
      }
    } else {
      resetQuestions(data, mapData);
    }

    renderNav();
    showQuestion(currentIdx);
    startTimer();
  } catch (error) {
    console.error("Gagal memuat soal:", error);
    document.getElementById("questionContainer").innerHTML = `
      <div class="alert alert-danger text-center fw-semibold">
        Terjadi kesalahan saat memuat soal ujian.
      </div>
    `;
  }
}

// ================= RESET =================
function resetQuestions(data, mapData) {
  questionOrder = data.map((q) => q.id);
  questionOrder.sort(() => Math.random() - 0.5);

  questions = questionOrder.map((id) => mapData[id]).filter((q) => q);

  userAnswers = {};
  raguState = {};
  currentIdx = 1;
  timeLeft = duration * 60;

  saveState();
}

// ================= SAVE =================
function saveState() {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      order: questionOrder,
      answers: userAnswers,
      ragu: raguState,
      current: currentIdx,
      time: timeLeft,
    }),
  );
}

// ================= NAV =================
function renderNav() {
  const nav = document.getElementById("navContainer");
  nav.innerHTML = "";

  questions.forEach((q, i) => {
    if (!q) return;

    let statusClass = "";
    if (userAnswers[q.id]) statusClass = "answered";
    if (raguState[q.id]) statusClass = "ragu";

    nav.innerHTML += `
        <div class="q-nav ${i === currentIdx - 1 ? "active" : ""} ${statusClass}" 
            id="nav${i + 1}"
            onclick="showQuestion(${i + 1})">
            ${i + 1}
        </div>
        `;
  });
}

// ================= SHOW =================
function showQuestion(n) {
  const q = questions[n - 1];
  if (!q) return;

  document.getElementById("displayNum").innerText = n;

  let html = `
  <div class="fs-5 mb-4 question-text">
    ${q.text}
  </div>
`;

  // =========================
  // TAMPILKAN GAMBAR SOAL
  // =========================
  if (q.URL) {
    html += `
    <div class="text-center mb-4">
      <img
        src="${q.URL}"
        alt="gambar soal"
        class="img-fluid rounded-4 shadow-sm border"
        style="
          max-height: 380px;
          object-fit: contain;
          background: white;
          padding: 10px;
        "
      >
    </div>
  `;
  }

  q.options.forEach((opt) => {
    const checked = userAnswers[q.id] === opt.key ? "checked" : "";

    html += `
        <label class="answer-item ${checked ? "selected" : ""}">
            <input type="radio" name="q${q.id}" value="${opt.key}"
                ${checked}
                onclick="markAnswered(${n}, this)">
            <span>${opt.key}. ${opt.text}</span>
        </label>
        `;
  });

  document.getElementById("questionContainer").innerHTML = html;

  if (window.MathJax) {
    MathJax.typesetPromise();
  }

  currentIdx = n;

  renderNav();
  saveState();
}

// ================= ANSWER =================
function markAnswered(idx, el) {
  const q = questions[idx - 1];
  if (!q) return;

  userAnswers[q.id] = el.value;

  // Render ulang soal agar class "selected" teraplikasi
  showQuestion(idx);

  saveState();
  renderNav();
}

// ================= RAGU =================
function toggleRagu() {
  const q = questions[currentIdx - 1];
  if (!q) return;

  raguState[q.id] = !raguState[q.id];

  saveState();
  renderNav();
}

// ================= NAVIGASI =================
function changeQuestion(step) {
  let target = currentIdx + step;

  if (target >= 1 && target <= questions.length) {
    showQuestion(target);
  }
}

// ================= AUTO SUBMIT & SUBMIT VALIDATION =================
setInterval(() => {
  if (timeLeft <= 0) {
    // Force submit jika waktu habis (mengabaikan validasi ragu/kosong)
    document.getElementById("quizForm").submit();
  }
}, 1000);

document.getElementById("quizForm").addEventListener("submit", function (e) {
  e.preventDefault(); // ❗ tahan submit manual dulu

  const formElement = this;
  let belumDijawab = [];
  let masihRagu = [];

  // 🔥 DETEKSI SOAL KOSONG & RAGU-RAGU BERDASARKAN NOMOR TAMPILAN (1, 2, 3...)
  questions.forEach((q, index) => {
    let nomorSoal = index + 1;

    // Cek apakah belum dijawab
    if (!userAnswers[q.id]) {
      belumDijawab.push(nomorSoal);
    }

    // Cek apakah ditandai ragu-ragu
    if (raguState[q.id] === true) {
      masihRagu.push(nomorSoal);
    }
  });

  // Jika ada soal yang kosong ATAU ragu-ragu, hentikan proses dan beri tahu user
  if (belumDijawab.length > 0 || masihRagu.length > 0) {
    let errorHTML = `<p class="mb-3">Kamu belum bisa menyelesaikan ujian ini karena:</p><div class="text-start" style="background: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; font-size: 0.95rem;">`;

    if (belumDijawab.length > 0) {
      errorHTML += `<div class="mb-2"><strong class="text-danger"><i class="fa-solid fa-circle-xmark me-1"></i> Belum dijawab:</strong> <br> Soal nomor <b>${belumDijawab.join(", ")}</b></div>`;
    }

    if (masihRagu.length > 0) {
      errorHTML += `<div><strong class="text-warning" style="color: #d97706 !important;"><i class="fa-solid fa-triangle-exclamation me-1"></i> Masih ragu-ragu:</strong> <br> Soal nomor <b>${masihRagu.join(", ")}</b></div>`;
    }

    errorHTML += `</div><p class="mt-3 mb-0 small text-muted">Silakan lengkapi dan hilangkan tanda ragu-ragu pada nomor tersebut.</p>`;

    Swal.fire({
      title: "Peringatan!",
      html: errorHTML,
      icon: "warning",
      confirmButtonColor: "#3b82f6",
      confirmButtonText: "Kembali Mengerjakan",
    });

    return; // Hentikan fungsi di sini
  }

  // Jika aman (semua dijawab & tidak ada ragu-ragu), tampilkan konfirmasi
  Swal.fire({
    title: "Selesai Ujian?",
    text: "Jawaban yang sudah dikirim tidak bisa diubah lagi!",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#22c55e",
    cancelButtonColor: "#d33",
    confirmButtonText: "Ya, Selesai!",
    cancelButtonText: "Batal",
  }).then((result) => {
    if (result.isConfirmed) {
      // 🔥 ANSWERS
      let input = document.createElement("input");
      input.type = "hidden";
      input.name = "answers";
      input.value = JSON.stringify(userAnswers);
      formElement.appendChild(input);

      // 🔥 CORRECT MAP
      let correctInput = document.createElement("input");
      correctInput.type = "hidden";
      correctInput.name = "correct_map";
      correctInput.value = JSON.stringify(correctMap);
      formElement.appendChild(correctInput);

      // 🔥 TIME
      let timeInput = document.createElement("input");
      timeInput.type = "hidden";
      timeInput.name = "time_left";
      timeInput.value = timeLeft;
      formElement.appendChild(timeInput);

      localStorage.removeItem(STORAGE_KEY);
      sessionStorage.removeItem(SESSION_FLAG);

      formElement.submit(); // ✅ baru submit setelah konfirmasi
    }
  });
});

// ================= EXIT FIX =================
window.addEventListener("pagehide", function () {
  const navType = performance.getEntriesByType("navigation")[0]?.type;

  if (navType !== "reload") {
    sessionStorage.removeItem(SESSION_FLAG);
  }
});

// ================= LOAD =================
window.onload = () => {
  loadQuestions();
};

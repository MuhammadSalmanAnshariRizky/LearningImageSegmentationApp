document.addEventListener("DOMContentLoaded", () => {
  const sliderR = document.getElementById("slider-r");
  const sliderG = document.getElementById("slider-g");
  const sliderB = document.getElementById("slider-b");

  const valR = document.getElementById("val-r");
  const valG = document.getElementById("val-g");
  const valB = document.getElementById("val-b");

  const colorPreview = document.getElementById("color-preview");
  const rgbOutput = document.getElementById("rgb-output");

  const feedbackText = document.getElementById("feedback-text");
  const feedbackPanel = document.getElementById("feedback-panel");
  const feedbackIcon = document.getElementById("feedback-icon");

  // Fungsi Utama untuk mengupdate simulasi
  function updateColor() {
    const r = parseInt(sliderR.value);
    const g = parseInt(sliderG.value);
    const b = parseInt(sliderB.value);

    // Update Label Angka
    valR.innerText = r;
    valG.innerText = g;
    valB.innerText = b;

    // Update Warna Background Preview
    colorPreview.style.backgroundColor = `RGB(${r}, ${g}, ${b})`;
    rgbOutput.innerText = `RGB(${r}, ${g}, ${b})`;

    // Mengatur Kontras Teks (Jika warna terang, teks jadi hitam, dan sebaliknya)
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    if (luminance > 0.5) {
      rgbOutput.classList.remove("text-white-50");
      rgbOutput.classList.add("text-muted");
    } else {
      rgbOutput.classList.remove("text-muted");
      rgbOutput.classList.add("text-white-50");
    }

    // ==========================================
    // LOGIKA FEEDBACK DINAMIS
    // ==========================================
    let msg = "";
    let borderColor = "#64748b";
    let iconClass = "fa-circle-info text-secondary";

    if (r === 0 && g === 0 && b === 0) {
      msg =
        "Tiga kanal bernilai 0 menghasilkan warna <strong>Hitam Pekat</strong> (ketiadaan cahaya).";
      borderColor = "#000000";
    } else if (r === 255 && g === 255 && b === 255) {
      msg =
        "Tiga kanal bernilai maksimal (255) bercampur menjadi cahaya <strong>Putih Murni</strong>.";
      borderColor = "#e2e8f0";
      iconClass = "fa-sun text-warning";
    } else if (r === g && g === b) {
      msg = `Karena nilai R, G, dan B seimbang (masing-masing <strong>${r}</strong>), kombinasi ini menghasilkan warna <strong>Abu-abu (Grayscale)</strong>.`;
      borderColor = "#94a3b8";
    } else if (r > 200 && g < 50 && b < 50) {
      msg =
        "Kanal Merah sangat dominan dan mendekati maksimal, menghasilkan warna <strong>Merah Kuat</strong>.";
      borderColor = "#dc2626";
      iconClass = "fa-droplet text-danger";
    } else if (g > 200 && r < 50 && b < 50) {
      msg =
        "Kanal Hijau sangat dominan dan mendekati maksimal, menghasilkan warna <strong>Hijau Kuat</strong>.";
      borderColor = "#16a34a";
      iconClass = "fa-leaf text-success";
    } else if (b > 200 && r < 50 && g < 50) {
      msg =
        "Kanal Biru sangat dominan dan mendekati maksimal, menghasilkan warna <strong>Biru Kuat</strong>.";
      borderColor = "#2563eb";
      iconClass = "fa-water text-primary";
    } else if (r > 200 && g > 200 && b < 50) {
      msg =
        "Percampuran intensitas tinggi dari Merah dan Hijau menciptakan warna <strong>Kuning (Yellow)</strong>.";
      borderColor = "#eab308";
      iconClass = "fa-bolt text-warning";
    } else if (r > 200 && b > 200 && g < 50) {
      msg =
        "Percampuran intensitas tinggi dari Merah dan Biru menciptakan warna <strong>Magenta</strong>.";
      borderColor = "#d946ef";
      iconClass = "fa-wand-magic-sparkles text-fuchsia";
    } else if (g > 200 && b > 200 && r < 50) {
      msg =
        "Percampuran intensitas tinggi dari Hijau dan Biru menciptakan warna <strong>Cyan</strong>.";
      borderColor = "#06b6d4";
      iconClass = "fa-snowflake text-info";
    } else {
      // Analisis Dominasi General
      const maxVal = Math.max(r, g, b);
      if (maxVal === r) {
        msg =
          "Intensitas Merah (R) memimpin campuran, memberikan karakteristik rona <strong>kemerahan/hangat</strong> pada hasil.";
        borderColor = "#f87171";
      } else if (maxVal === g) {
        msg =
          "Intensitas Hijau (G) memimpin campuran, memberikan karakteristik rona <strong>kehijauan</strong> pada hasil.";
        borderColor = "#4ade80";
      } else if (maxVal === b) {
        msg =
          "Intensitas Biru (B) memimpin campuran, memberikan karakteristik rona <strong>kebiruan/dingin</strong> pada hasil.";
        borderColor = "#60a5fa";
      }
    }

    // Terapkan Feedback ke UI
    feedbackText.innerHTML = msg;
    feedbackPanel.style.borderLeftColor = borderColor;
    feedbackIcon.className = `fa-solid fs-5 mt-1 me-3 ${iconClass}`;
  }

  // Pasang Event Listener ke ketiga slider
  sliderR.addEventListener("input", updateColor);
  sliderG.addEventListener("input", updateColor);
  sliderB.addEventListener("input", updateColor);

  // Jalankan sekali saat halaman dimuat
  updateColor();
});

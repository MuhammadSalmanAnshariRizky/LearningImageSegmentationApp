const btnRangkuman = document.getElementById("btnSelesaiRangkuman");

if (btnRangkuman) {
  btnRangkuman.addEventListener("click", function () {
    const idTopic = this.dataset.topic;
    const idSubtopic = this.dataset.subtopic;

    // Ubah teks tombol jadi loading biar user tidak klik berkali-kali
    const originalText = this.innerHTML;
    this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Menyimpan...';
    this.disabled = true;

    fetch("/update-progress", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id_topic: idTopic,
        id_subtopic: idSubtopic,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          // ==========================================
          // 1. UPDATE TAMPILAN PROGRESS TANPA REFRESH
          // ==========================================
          if (data.new_progress !== undefined) {
            // A. Update Progress Bar (Hanya lebarnya saja, tanpa teks di dalamnya)
            const progressBar = document.querySelector(".progress-bar");
            if (progressBar) {
              progressBar.style.width = data.new_progress + "%";
              progressBar.setAttribute("aria-valuenow", data.new_progress);
              // Baris innerText dihapus di sini agar tidak ada teks di dalam batang
            }

            // B. Update Teks Progress di pojok kanan
            const progressText = document.getElementById("progressText");
            if (progressText) {
              // Menambahkan ".0%" menyesuaikan format di gambar (misal 12.0%)
              progressText.innerText = data.new_progress + ".0%";
            }
          }

          // ==========================================
          // 2. BUKA KUNCI TOMBOL NEXT MATERI (Jika Ada)
          // ==========================================
          const btnNext = document.getElementById("btnNextMateri");
          if (btnNext) {
            btnNext.classList.remove("disabled-link");
            btnNext.style.backgroundColor = "#1e293b";
          }

          // ==========================================
          // 3. TAMPILKAN SWEETALERT & UBAH TOMBOL
          // ==========================================
          Swal.fire({
            icon: "success",
            title: "Rangkuman Selesai!",
            text: "Progress belajar berhasil diperbarui.",
            confirmButtonColor: "#198754",
            confirmButtonText: "OK",
          });

          // Ubah tampilan tombol rangkuman menjadi tanda selesai
          this.innerHTML = '<i class="fa-solid fa-check"></i> Selesai';
          this.classList.replace("btn-primary", "btn-success");
        } else {
          // Kembalikan tombol ke semula jika response dari server gagal
          this.innerHTML = originalText;
          this.disabled = false;
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: data.message || "Gagal memperbarui progress.",
          });
        }
      })
      .catch((err) => {
        console.error(err);
        // Kembalikan tombol ke semula jika ada error jaringan
        this.innerHTML = originalText;
        this.disabled = false;

        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Terjadi kesalahan sistem.",
        });
      });
  });
}

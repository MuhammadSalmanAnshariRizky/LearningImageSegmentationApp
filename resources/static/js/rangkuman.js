const btnRangkuman = document.getElementById("btnSelesaiRangkuman");

if (btnRangkuman) {
  btnRangkuman.addEventListener("click", function () {
    const idTopic = this.dataset.topic;
    const idSubtopic = this.dataset.subtopic;

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
        Swal.fire({
          icon: "success",
          title: "Rangkuman Selesai!",
          text: "Progress belajar berhasil diperbarui.",
          confirmButtonColor: "#198754",
          confirmButtonText: "OK",
        }).then(() => {
          location.reload();
        });
      })
      .catch((err) => {
        console.error(err);

        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Gagal memperbarui progress.",
        });
      });
  });
}

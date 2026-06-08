document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".sidebar-sub");
  const scrollContainer = document.querySelector(".sidebar-scroll"); // Pastikan class ini sesuai dengan wadah scroll sidebar Anda

  let currentPath = window.location.pathname.replace(/\/$/, "");
  let activeLink = null;

  // =========================
  // 1. SET ACTIVE LINK & BUKA ACCORDION
  // =========================
  links.forEach((link) => {
    let linkPath = link.getAttribute("href").replace(/\/$/, "");

    // Jika URL saat ini cocok dengan href pada link sidebar
    if (linkPath === currentPath) {
      activeLink = link;
      link.classList.add("active");

      // Cari elemen accordion yang membungkus link ini
      const collapse = link.closest(".accordion-collapse");

      if (collapse) {
        // Buka isi accordion
        collapse.classList.add("show");

        // Ubah status tombol accordion parent menjadi terbuka
        const button =
          collapse.previousElementSibling?.querySelector(".accordion-button");
        if (button) {
          button.classList.remove("collapsed");
          button.setAttribute("aria-expanded", "true");
        }
      }
    }
  });

  // =========================
  // 2. AUTO SCROLL KE MENU YANG AKTIF
  // =========================
  if (activeLink && scrollContainer) {
    // Jeda sedikit agar transisi accordion selesai sebelum scroll
    setTimeout(() => {
      activeLink.scrollIntoView({
        behavior: "smooth",
        block: "center", // Posisikan elemen di tengah layar sidebar
      });
    }, 300);
  }
});

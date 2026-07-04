// pagination konten
let currentPage = 0;
let maxUnlockedPage = 0; // Tambahan: Melacak halaman terjauh yang terbuka

// key unik tiap halaman
const pageKey = "lastPage_" + window.location.pathname.replace(/\//g, "_");
const maxPageKey = "maxPage_" + window.location.pathname.replace(/\//g, "_"); // Key untuk menyimpan progress unlock

function showPage(index) {
  const pages = document.querySelectorAll(".page-section");

  if (!pages[index]) return; // biar aman

  // Cegah akses jika halaman belum di-unlock
  if (index > maxUnlockedPage) {
    alert("Silakan baca halaman sebelumnya terlebih dahulu!");
    return;
  }

  pages.forEach((p) => p.classList.remove("active"));
  pages[index].classList.add("active");

  currentPage = index;
  localStorage.setItem(pageKey, index);

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });

  updatePagination();
}

function nextPage() {
  const pages = document.querySelectorAll(".page-section");

  if (currentPage === pages.length - 1) {
    window.location.href = "/materi1/jeniscitra";
    return;
  }

  const targetPage = currentPage + 1;

  // Unlock halaman berikutnya ketika tombol Next ditekan
  if (targetPage > maxUnlockedPage) {
    maxUnlockedPage = targetPage;
    localStorage.setItem(maxPageKey, maxUnlockedPage);
  }

  showPage(targetPage);
}

function prevPage() {
  if (currentPage <= 0) return;
  showPage(currentPage - 1);
}

function goPage(index) {
  // Hanya panggil showPage, karena validasi kunci sudah ada di dalam showPage
  showPage(index);
}

function updatePagination() {
  const items = document.querySelectorAll(".custom-pagination .page-item");
  const pages = document.querySelectorAll(".page-section");

  items.forEach((item) => {
    item.classList.remove("active");
    item.classList.remove("locked"); // Hapus class locked sebelumnya
  });

  const activeIndex = currentPage + 1;

  // Set active class
  if (items[activeIndex]) {
    items[activeIndex].classList.add("active");
  }

  // Disable visual untuk nomor halaman yang belum di-unlock
  // Asumsi: items[0] itu Prev, items[length-1] itu Next. Sisanya adalah angka halaman.
  for (let i = 1; i <= pages.length; i++) {
    let pageIndex = i - 1;
    if (pageIndex > maxUnlockedPage && items[i]) {
      items[i].classList.add("locked");
    }
  }

  const prev = document.getElementById("prevPageItem");
  if (prev) {
    prev.style.display = currentPage === 0 ? "none" : "block";
  }

  const next = document.getElementById("nextPageItem");
  if (next) {
    next.style.display = currentPage === pages.length - 1 ? "none" : "block";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const savedPage = localStorage.getItem(pageKey);
  const savedMaxPage = localStorage.getItem(maxPageKey);

  // Ambil history halaman terjauh
  if (savedMaxPage !== null && !isNaN(savedMaxPage)) {
    maxUnlockedPage = parseInt(savedMaxPage);
  }

  // Ambil halaman terakhir yang dibaca
  if (savedPage !== null && !isNaN(savedPage)) {
    let parsedPage = parseInt(savedPage);
    // Pastikan halaman yang tersimpan tidak melebihi batas unlock (mencegah bug manipulasi localStorage)
    currentPage = parsedPage > maxUnlockedPage ? maxUnlockedPage : parsedPage;
  }

  showPage(currentPage);
});

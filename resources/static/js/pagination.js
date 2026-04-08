// pagination konten
let currentPage = 0;

// key unik tiap halaman
const pageKey = "lastPage_" + window.location.pathname.replace(/\//g, "_");

function showPage(index) {
  const pages = document.querySelectorAll(".page-section");

  if (!pages[index]) return; // biar aman

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

  showPage(currentPage + 1);
}

function prevPage() {
  if (currentPage <= 0) return;
  showPage(currentPage - 1);
}

function goPage(index) {
  showPage(index);
}

function updatePagination() {
  const items = document.querySelectorAll(".custom-pagination .page-item");
  const pages = document.querySelectorAll(".page-section");

  items.forEach((item) => item.classList.remove("active"));

  const activeIndex = currentPage + 1;

  // biar gak error kalau index gak ada
  if (items[activeIndex]) {
    items[activeIndex].classList.add("active");
  }

  const prev = document.getElementById("prevPageItem");
  if (prev) {
    prev.style.display = currentPage === 0 ? "none" : "block";
  }

  const next = document.getElementById("nextPageItem");

  // FIX: disable kalau halaman terakhir
  if (next) {
    next.style.display = currentPage === pages.length - 1 ? "none" : "block";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const savedPage = localStorage.getItem(pageKey);

  // validasi biar gak error
  if (savedPage !== null && !isNaN(savedPage)) {
    currentPage = parseInt(savedPage);
  }

  showPage(currentPage);
});

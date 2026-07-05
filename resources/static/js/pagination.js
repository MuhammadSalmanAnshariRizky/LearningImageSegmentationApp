// pagination konten
let currentPage = 0;
let maxUnlockedPage = 0; // Melacak halaman terjauh yang terbuka

// key unik tiap halaman
const pageKey = "lastPage_" + window.location.pathname.replace(/\//g, "_");
const maxPageKey = "maxPage_" + window.location.pathname.replace(/\//g, "_");

function showPage(index) {
  const pages = document.querySelectorAll(".page-section");

  if (!pages[index]) return;

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
  showPage(index);
}

function updatePagination() {
  const items = document.querySelectorAll(".custom-pagination .page-item");
  const pages = document.querySelectorAll(".page-section");

  items.forEach((item) => {
    item.classList.remove("active");
    item.classList.remove("locked");
  });

  const activeIndex = currentPage + 1;

  // Set active class
  if (items[activeIndex]) {
    items[activeIndex].classList.add("active");
  }

  // Disable visual untuk nomor halaman yang belum di-unlock
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
  const pages = document.querySelectorAll(".page-section");
  const totalPages = pages.length;

  const savedPage = localStorage.getItem(pageKey);
  const savedMaxPage = localStorage.getItem(maxPageKey);

  // 1. TANGKAP STATUS DARI HTML DATA ATTRIBUTE
  const dataContainer = document.getElementById("materi-data");
  let isCompletedFromBackend = false;

  if (dataContainer) {
    // dataset.isCompleted otomatis mengambil nilai dari atribut data-is-completed
    isCompletedFromBackend = dataContainer.dataset.isCompleted === "true";
  }

  // 2. LOGIKA UNLOCK
  if (isCompletedFromBackend) {
    maxUnlockedPage = totalPages - 1; // Unlock maksimal
    localStorage.setItem(maxPageKey, maxUnlockedPage);
  } else {
    if (savedMaxPage !== null && !isNaN(savedMaxPage)) {
      maxUnlockedPage = parseInt(savedMaxPage);
    }
  }

  // 3. LOGIKA HALAMAN SAAT INI
  if (savedPage !== null && !isNaN(savedPage)) {
    let parsedPage = parseInt(savedPage);
    currentPage = parsedPage > maxUnlockedPage ? maxUnlockedPage : parsedPage;
  }

  showPage(currentPage);
});

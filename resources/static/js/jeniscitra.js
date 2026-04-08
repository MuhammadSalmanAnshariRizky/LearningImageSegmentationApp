//pagination konten
let currentPage = 0;
function showPage(index) {
  const pages = document.querySelectorAll(".page-section");

  pages.forEach((p) => p.classList.remove("active"));

  pages[index].classList.add("active");

  currentPage = index;

  localStorage.setItem("lastPage", index);

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });

  updatePagination();
}
function nextPage() {
  const pages = document.querySelectorAll(".page-section");

  // kalau di halaman terakhir → pindah halaman
  if (currentPage === pages.length - 1) {
    window.location.href = "#";
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
  items[activeIndex].classList.add("active");

  const prev = document.getElementById("prevPageItem");
  if (currentPage === 0) {
    prev.style.display = "none";
  } else {
    prev.style.display = "block";
  }

  const next = document.getElementById("nextPageItem");

  if (currentPage === pages.length - 1) {
    next.classList.remove("disabled"); 
  } else {
    next.classList.remove("disabled");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const savedPage = localStorage.getItem("lastPage");

  if (savedPage !== null) {
    currentPage = parseInt(savedPage);
  }

  showPage(currentPage);
});

document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".sidebar-sub");
  const sidebar = document.querySelector(".sidebar");
  let currentPath = window.location.pathname.replace(/\/$/, "");

  let activeLink = null;

  // =========================
  // AMBIL DATA ACCORDION
  // =========================
  let activeAccordions =
    JSON.parse(localStorage.getItem("activeAccordions")) || [];

  // =========================
  // BUKA ACCORDION
  // =========================
  activeAccordions.forEach((id) => {
    const el = document.querySelector(id);
    if (el) {
      el.classList.add("show");

      const button =
        el.previousElementSibling.querySelector(".accordion-button");
      if (button) {
        button.classList.remove("collapsed");
        button.setAttribute("aria-expanded", "true");
      }
    }
  });

  // =========================
  // ACTIVE LINK
  // =========================
  links.forEach((link) => {
    let linkPath = link.getAttribute("href").replace(/\/$/, "");

    if (linkPath === currentPath) {
      activeLink = link;

      setTimeout(() => {
        link.classList.add("active");
      }, 150);

      const collapse = link.closest(".accordion-collapse");
      if (collapse) {
        collapse.classList.add("show");

        const id = "#" + collapse.id;

        if (!activeAccordions.includes(id)) {
          activeAccordions.push(id);
          localStorage.setItem(
            "activeAccordions",
            JSON.stringify(activeAccordions),
          );
        }

        const button =
          collapse.previousElementSibling.querySelector(".accordion-button");
        if (button) {
          button.classList.remove("collapsed");
          button.setAttribute("aria-expanded", "true");
        }
      }
    }
  });

  // =========================
  // SAVE ACCORDION CLICK
  // =========================
  document.querySelectorAll(".accordion-button").forEach((btn) => {
    btn.addEventListener("click", function () {
      const target = this.getAttribute("data-bs-target");

      let activeAccordions =
        JSON.parse(localStorage.getItem("activeAccordions")) || [];

      if (activeAccordions.includes(target)) {
        activeAccordions = activeAccordions.filter((id) => id !== target);
      } else {
        activeAccordions.push(target);
      }

      localStorage.setItem(
        "activeAccordions",
        JSON.stringify(activeAccordions),
      );
    });
  });

  // =========================
  // AUTO SCROLL KE ACTIVE LINK
  // =========================
  if (activeLink) {
    setTimeout(() => {
      activeLink.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }, 300); // tunggu accordion kebuka dulu
  }
});

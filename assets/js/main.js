document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".site-header");
  var navToggle = document.querySelector(".nav-toggle");
  if (navToggle && header) {
    navToggle.addEventListener("click", function () {
      var isOpen = header.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    header.querySelectorAll(".site-header__nav a").forEach(function (link) {
      link.addEventListener("click", function () {
        header.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var submenus = document.querySelectorAll(".has-submenu");
  submenus.forEach(function (item) {
    var toggle = item.querySelector(".has-submenu__toggle");
    if (!toggle) return;
    toggle.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      var isOpen = item.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  });

  function fecharSubmenus() {
    submenus.forEach(function (item) {
      item.classList.remove("is-open");
      var toggle = item.querySelector(".has-submenu__toggle");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    });
  }

  document.addEventListener("click", function (event) {
    if (!event.target.closest(".has-submenu")) fecharSubmenus();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") fecharSubmenus();
  });

  document.querySelectorAll(".faq-item").forEach(function (item) {
    var question = item.querySelector(".faq-item__q");
    question.addEventListener("click", function () {
      var wasOpen = item.classList.contains("is-open");
      item.parentElement.querySelectorAll(".faq-item").forEach(function (other) {
        other.classList.remove("is-open");
        other.querySelector(".faq-item__q").setAttribute("aria-expanded", "false");
      });
      if (!wasOpen) {
        item.classList.add("is-open");
        question.setAttribute("aria-expanded", "true");
      }
    });
  });
});

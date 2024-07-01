function toggleMenu() {
    var menuToggle = document.querySelector('.menu-toggle');
    var sidebar = document.querySelector('.sidebar');
    if (sidebar.style.left === "-250px") {
      sidebar.style.left = "0";
      menuToggle.classList.add('open');
    } else {
      sidebar.style.left = "-250px";
      menuToggle.classList.remove('open');
    }
  }
  
window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.home__navigation-wrapper');
    if (window.scrollY > 100) {
      navbar.classList.add('navbar-scrolled');
    } else {
      navbar.classList.remove('navbar-scrolled');
    }
  });
  
document.querySelectorAll('.lazy-link').forEach(link => {
  link.addEventListener('click', function(event) {
      event.preventDefault();
      const content = link.getAttribute('data-content');
      const section = document.getElementById('section1');
      section.innerHTML = content;
  });
});

document.querySelectorAll('.dropdown-btn').forEach(button => {
  button.addEventListener('click', function() {
      this.classList.toggle('active');
      const dropdownContent = this.nextElementSibling;
      if (dropdownContent.classList.contains('show')) {
          dropdownContent.classList.remove('show');
          dropdownContent.classList.add('hide');
          setTimeout(() => {
              dropdownContent.classList.remove('hide');
          }, 300);
      } else {
          dropdownContent.classList.add('show');
      }
  });
});
document.querySelector('.toggle-menu').addEventListener('click', function() {
    const sidebar = document.querySelector('.sidebar');
    const menuButton = document.querySelector('.toggle-menu');
    sidebar.classList.toggle('show');
    menuButton.classList.toggle('change');
});

document.querySelectorAll('.menu > li > a').forEach(menuItem => {
    menuItem.addEventListener('click', function() {
        const submenu = menuItem.nextElementSibling;
        if (submenu && submenu.classList.contains('submenu')) {
            submenu.classList.toggle('show');
        }
    });
});

function handleScroll() {
    const cards = document.querySelectorAll('.card');
    const triggerBottom = window.innerHeight / 5 * 4;

    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;

        if (cardTop < triggerBottom) {
            card.classList.add('visible');
        } else {
            card.classList.remove('visible');
        }
    });
}

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll);

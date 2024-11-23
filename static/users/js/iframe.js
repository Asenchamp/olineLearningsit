document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.sidebar-link');
    const iframe = document.getElementById('content-frame');

    links.forEach(link => {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        iframe.src = this.href;
      });
    });
  });
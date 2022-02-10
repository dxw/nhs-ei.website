document.getElementById("toggle-menu").addEventListener("click", function (e) {
    e.preventDefault();

    const nav = document.getElementById("mega-menu")
    nav.style.display = nav.style.display === 'block' ? 'none' : 'block';
}, false);

/*
JS:        packages/mega-menu-expander.js
CSS:       packages/custom-styles/_megamenu.scss
Templates: cms/templates/partials/megamenu
*/

document.addEventListener("DOMContentLoaded", () => {
    const toggleMenu = document.getElementsByClassName("toggle-menu-expand");

    for (const link of toggleMenu) {
        link.addEventListener("click", (event) => {
            // Add listener here
            event.preventDefault();
        });
    }
});
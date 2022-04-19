/*
JS:        packages/mega-menu.js
CSS:       packages/custom-styles/_megamenu.scss
Templates: cms/templates/partials/megamenu
*/

/* ******************** Burger Menu ******************** */

const show = function (elem) {
    elem.classList.add('is-visible');
};

const hide = function (elem) {
    elem.classList.remove('is-visible');
};

const toggle = function (elem, timing) {
    if (elem.classList.contains('is-visible')) {
        hide(elem);
        return;
    }
    show(elem);
};

document.getElementById("toggle-menu").addEventListener("click", function (e) {
    e.preventDefault();
    toggle(document.getElementById("mega-menu"));
}, false);
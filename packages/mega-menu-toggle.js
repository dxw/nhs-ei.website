const show = function (elem) {
    const getHeight = function () {
        elem.style.display = 'block';
        const height = elem.scrollHeight + 'px';
        elem.style.display = '';
        return height;
    };

    const height = getHeight();
    elem.classList.add('is-visible');
    elem.style.height = height;

    window.setTimeout(function () {
        elem.style.height = '';
    }, 350);

};

const hide = function (elem) {
    elem.style.height = elem.scrollHeight + 'px';

    window.setTimeout(function () {
        elem.style.height = '0';
    }, 1);

    window.setTimeout(function () {
        elem.classList.remove('is-visible');
    }, 350);
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

document.addEventListener("DOMContentLoaded", () => {
    if (location.hash.replace('#','') === "open") {
        toggle(document.getElementById("mega-menu"))
    }
});
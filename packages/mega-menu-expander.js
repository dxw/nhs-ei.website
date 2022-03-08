const showHideSubmenu = (submenuId, submenuDepth) => {
    const menus = document.getElementsByClassName("toggle-menu");
    console.log(submenuId, submenuDepth);
    document.getElementById(submenuId).style.display = "block";
    // debugger;
}

document.addEventListener("DOMContentLoaded", () => {
    const toggleMenu = document.getElementsByClassName("toggle-menu");

    for (const link of toggleMenu) {
        link.addEventListener("click", (event) => {
            console.log(event.target);
            event.preventDefault();
            const target = event.target;
            const submenuId = target.getAttribute("data-submenu")
            const submenuDepth = target.getAttribute("data-depth")
            showHideSubmenu(submenuId, submenuDepth);
        });
    }
});
window.onload = init();
let toolbarStatus = 'file';

function init() {
    let toolbarSubMenuButtons = document.querySelectorAll('.toolbar-btn');

    for (let button of toolbarSubMenuButtons) {
        button.addEventListener('click', function () {
            toolbarStatus = button.getAttribute('state');
            loadSubmenuToolbar(toolbarStatus);
        });
    }
}

function loadSubmenuToolbar(state) {
    switch (state) {
        case "file":
            break;
        case "file":
            break;
        case "file":
            break;
        case "file":
            break;
    }
}
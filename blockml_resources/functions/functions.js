window.onload = init();
let toolbarStatus = 'file';
let submenuToolbar = {
    "file": [
        { "name": "",  },
        { "name": "",  },
        { "name": "",  }
    ],
    "edit": [
        { "": "" },
        { "": "" },
        { "": "" }
    ],
    "view": [
        { "": "" },
        { "": "" },
        { "": "" }
    ],
    "tools": [
        { "": "" },
        { "": "" },
        { "": "" }
    ]
};

function init() {
    let toolbarSubMenuButtons = document.querySelectorAll('.toolbar-btn');

    for (let button of toolbarSubMenuButtons) {
        button.addEventListener('click', function () {
            toolbarStatus = button.getAttribute('state');
            loadSubmenuToolbar(toolbarStatus);
        });
    }

    loadSubmenuToolbar('file');

}

function loadSubmenuToolbar(state) {
    let parentElement = document.querySelector('.toolbar-submenu');
    switch (state) {
        default:
        case "file":
            break;
        case "edit":
            break;
        case "view":
            break;
        case "tools":
            break;

    }
}
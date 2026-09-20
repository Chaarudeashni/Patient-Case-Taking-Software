/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   Common Application Layout
   Clinical Records removed
   ========================================================= */


/* =========================================================
   PAGE CONFIGURATION
   ========================================================= */

const PAGE_CONFIG = {

    dashboard: {
        title: "Dashboard",
        subtitle: "Overview of your clinical workspace"
    },

    patients: {
        title: "Patients",
        subtitle: "Manage patient information and records"
    },

    "new-case": {
        title: "New Case",
        subtitle: "Create a new patient clinical case"
    },

    "follow-ups": {
        title: "Follow-ups",
        subtitle: "Manage patient follow-up records"
    },

    appointments: {
        title: "Appointments",
        subtitle: "Manage patient appointments"
    },

    reports: {
        title: "Reports",
        subtitle: "View clinical and patient reports"
    },

    settings: {
        title: "Settings",
        subtitle: "Manage your application settings"
    }

};


/* =========================================================
   NAVIGATION
   Clinical Records completely removed
   ========================================================= */

const NAV_ITEMS = [

    {
        section: "Main",

        items: [

            {
                page: "dashboard",
                label: "Dashboard",
                icon: "⌂",
                url: "index.html"
            },

            {
                page: "patients",
                label: "Patients",
                icon: "♙",
                url: "patients.html"
            },

            {
                page: "new-case",
                label: "New Case",
                icon: "＋",
                url: "new-case.html"
            },

            {
                page: "follow-ups",
                label: "Follow-ups",
                icon: "↻",
                url: "follow-ups.html"
            },

            {
                page: "appointments",
                label: "Appointments",
                icon: "□",
                url: "appointments.html"
            },

            {
                page: "reports",
                label: "Reports",
                icon: "▤",
                url: "reports.html"
            }

        ]
    },

    {
        section: "System",

        items: [

            {
                page: "settings",
                label: "Settings",
                icon: "⚙",
                url: "settings.html"
            }

        ]
    }

];


/* =========================================================
   AUTHENTICATION
   ========================================================= */

function isLoggedIn() {

    if (
        typeof window.getStoredUser === "function"
    ) {

        try {

            const user =
                window.getStoredUser();

            return !!user;

        } catch (error) {

            console.warn(
                "getStoredUser() failed:",
                error
            );
        }
    }


    const possibleKeys = [

        "loggedInUser",
        "currentUser",
        "user",
        "clinician",
        "authUser"

    ];


    for (
        const key of possibleKeys
    ) {

        const value =
            localStorage.getItem(key);


        if (!value) {
            continue;
        }


        try {

            const parsed =
                JSON.parse(value);


            if (parsed) {
                return true;
            }

        } catch (error) {

            if (
                String(value).trim() !== ""
            ) {

                return true;
            }
        }
    }


    return false;
}


/* =========================================================
   GET CURRENT USER
   ========================================================= */

function getCurrentStoredUser() {

    if (
        typeof window.getStoredUser === "function"
    ) {

        try {

            return window.getStoredUser();

        } catch (error) {

            console.warn(
                "getStoredUser() failed:",
                error
            );
        }
    }


    const possibleKeys = [

        "loggedInUser",
        "currentUser",
        "user",
        "clinician",
        "authUser"

    ];


    for (
        const key of possibleKeys
    ) {

        const value =
            localStorage.getItem(key);


        if (!value) {
            continue;
        }


        try {

            const parsed =
                JSON.parse(value);


            if (parsed) {
                return parsed;
            }

        } catch (error) {

            return {
                username: value
            };
        }
    }


    return null;
}


/* =========================================================
   CLEAR LOGIN
   ========================================================= */

function clearCurrentLoggedInUser() {

    if (
        typeof window.clearLoggedInUser === "function"
    ) {

        try {

            window.clearLoggedInUser();

            return;

        } catch (error) {

            console.warn(
                "clearLoggedInUser() failed:",
                error
            );
        }
    }


    const possibleKeys = [

        "loggedInUser",
        "currentUser",
        "user",
        "clinician",
        "authUser"

    ];


    possibleKeys.forEach(
        key => localStorage.removeItem(key)
    );
}


/* =========================================================
   INITIALIZATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);


function initializeApplication() {

    const currentPage =
        document.body.dataset.page;


    /*
     * Login page does not use the application shell.
     */

    if (currentPage === "login") {

        return;
    }


    /*
     * All other pages require login.
     */

    if (!isLoggedIn()) {

        window.location.href =
            "login.html";

        return;
    }


    buildApplicationLayout();

    setupSidebar();

    setupLogout();

    setupMobileMenu();

    updateUserInformation();
}


/* =========================================================
   BUILD APPLICATION LAYOUT
   ========================================================= */

function buildApplicationLayout() {

    const app =
        document.getElementById("app");


    if (!app) {

        return;
    }


    const currentPage =
        document.body.dataset.page;


    const config =
        PAGE_CONFIG[currentPage] ||
        PAGE_CONFIG.dashboard;


    let pageContentHTML =
        app.innerHTML.trim();


    /*
     * If the page has no existing content,
     * show the common loading indicator.
     */

    if (!pageContentHTML) {

        pageContentHTML =
            getPageLoadingContent();
    }


    /*
     * Remove any old common-shell elements if
     * this function is ever called more than once.
     */

    app.innerHTML = `

        <div class="app-layout">

            <!-- ================= SIDEBAR ================= -->

            <aside
                class="sidebar"
                id="sidebar"
            >

                <div class="sidebar-brand">

                    <div class="brand-icon">
                        +
                    </div>

                    <div>

                        <h2>
                            Patient Case Taking
                        </h2>

                        <span>
                            Clinical Management
                        </span>

                    </div>

                </div>


                <nav
                    class="sidebar-nav"
                    id="sidebarNav"
                >

                    ${buildNavigation(currentPage)}

                </nav>


                <div class="sidebar-footer">

                    <div class="user-mini">

                        <div
                            class="user-avatar"
                            id="sidebarUserAvatar"
                        >
                            C
                        </div>

                        <div class="user-mini-info">

                            <strong
                                id="sidebarUsername"
                            >
                                Clinician
                            </strong>

                            <span>
                                Clinician
                            </span>

                        </div>

                    </div>


                    <button
                        class="sidebar-link"
                        id="logoutButton"
                        type="button"
                    >

                        <span class="sidebar-icon">
                            ⇥
                        </span>

                        <span>
                            Logout
                        </span>

                    </button>

                </div>

            </aside>


            <!-- ================= MAIN ================= -->

            <main class="main-content">

                <header class="topbar">

                    <div
                        style="
                            display:flex;
                            align-items:center;
                            gap:12px;
                        "
                    >

                        <button
                            class="mobile-menu-button"
                            id="mobileMenuButton"
                            type="button"
                        >
                            ☰
                        </button>


                        <div class="page-heading">

                            <h1>
                                ${escapeHtml(config.title)}
                            </h1>

                            <p>
                                ${escapeHtml(config.subtitle)}
                            </p>

                        </div>

                    </div>


                    <div class="topbar-actions">

                        <span
                            class="badge badge-primary"
                        >
                            Clinical Workspace
                        </span>

                    </div>

                </header>


                <section
                    class="page-content"
                    id="pageContent"
                >

                    ${pageContentHTML}

                </section>

            </main>

        </div>


        <div
            class="toast-container"
            id="toastContainer"
        ></div>

    `;
}


/* =========================================================
   NAVIGATION HTML
   ========================================================= */

function buildNavigation(currentPage) {

    let html = "";


    NAV_ITEMS.forEach(section => {

        html += `

            <div class="sidebar-section-title">

                ${escapeHtml(section.section)}

            </div>

        `;


        section.items.forEach(item => {

            const active =
                item.page === currentPage
                    ? "active"
                    : "";


            html += `

                <button
                    class="sidebar-link ${active}"
                    type="button"
                    data-url="${escapeHtml(item.url)}"
                >

                    <span class="sidebar-icon">

                        ${item.icon}

                    </span>

                    <span>

                        ${escapeHtml(item.label)}

                    </span>

                </button>

            `;
        });

    });


    return html;
}


/* =========================================================
   PAGE LOADING CONTENT
   ========================================================= */

function getPageLoadingContent() {

    return `

        <div class="loading">

            <div class="spinner"></div>

            <span>
                Loading...
            </span>

        </div>

    `;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

function setupSidebar() {

    const links =
        document.querySelectorAll(
            ".sidebar-link[data-url]"
        );


    links.forEach(link => {

        link.addEventListener(
            "click",
            function () {

                const url =
                    this.dataset.url;


                if (url) {

                    window.location.href =
                        url;
                }

            }
        );

    });
}


/* =========================================================
   LOGOUT
   ========================================================= */

function setupLogout() {

    const logoutButton =
        document.getElementById(
            "logoutButton"
        );


    if (!logoutButton) {

        return;
    }


    logoutButton.addEventListener(
        "click",
        function () {

            const confirmed =
                window.confirm(
                    "Are you sure you want to logout?"
                );


            if (!confirmed) {

                return;
            }


            clearCurrentLoggedInUser();


            window.location.href =
                "login.html";

        }
    );
}


/* =========================================================
   USER INFORMATION
   ========================================================= */

function updateUserInformation() {

    const user =
        getCurrentStoredUser();


    if (!user) {

        return;
    }


    const username =
        user.username ||
        user.name ||
        "Clinician";


    const usernameElement =
        document.getElementById(
            "sidebarUsername"
        );


    if (usernameElement) {

        usernameElement.textContent =
            username;
    }


    const avatarElement =
        document.getElementById(
            "sidebarUserAvatar"
        );


    if (avatarElement) {

        avatarElement.textContent =
            username
                .charAt(0)
                .toUpperCase();
    }
}


/* =========================================================
   MOBILE SIDEBAR
   ========================================================= */

function setupMobileMenu() {

    const menuButton =
        document.getElementById(
            "mobileMenuButton"
        );


    const sidebar =
        document.getElementById(
            "sidebar"
        );


    if (
        !menuButton ||
        !sidebar
    ) {

        return;
    }


    menuButton.addEventListener(
        "click",
        function () {

            sidebar.classList.toggle(
                "mobile-open"
            );

        }
    );


    const navigationLinks =
        document.querySelectorAll(
            ".sidebar-link[data-url]"
        );


    navigationLinks.forEach(link => {

        link.addEventListener(
            "click",
            function () {

                sidebar.classList.remove(
                    "mobile-open"
                );

            }
        );

    });
}


/* =========================================================
   TOAST NOTIFICATIONS
   ========================================================= */

function showToast(
    message,
    type = "success"
) {

    const container =
        document.getElementById(
            "toastContainer"
        );


    if (!container) {

        return;
    }


    const toast =
        document.createElement(
            "div"
        );


    toast.className =
        `toast ${type}`;


    toast.textContent =
        message;


    container.appendChild(
        toast
    );


    setTimeout(
        () => {

            toast.style.opacity =
                "0";


            toast.style.transform =
                "translateX(20px)";


            setTimeout(
                () => toast.remove(),
                250
            );

        },
        3000
    );
}


/* =========================================================
   ALERT HELPER
   ========================================================= */

function showAlert(
    container,
    message,
    type = "info"
) {

    if (!container) {

        return;
    }


    container.innerHTML = `

        <div class="alert alert-${escapeHtml(type)}">

            ${escapeHtml(message)}

        </div>

    `;
}


/* =========================================================
   HTML ESCAPE
   ========================================================= */

function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }


    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


/* =========================================================
   DATE FORMAT
   ========================================================= */

function formatDate(value) {

    if (!value) {

        return "-";
    }


    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return value;
    }


    return date.toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}


/* =========================================================
   DATE + TIME FORMAT
   ========================================================= */

function formatDateTime(value) {

    if (!value) {

        return "-";
    }


    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return value;
    }


    return date.toLocaleString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}


/* =========================================================
   EMPTY VALUE
   ========================================================= */

function displayValue(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "-";
    }


    return escapeHtml(value);
}


/* =========================================================
   GLOBAL EXPORTS
   ========================================================= */

window.PAGE_CONFIG =
    PAGE_CONFIG;


window.isLoggedIn =
    isLoggedIn;


window.getCurrentStoredUser =
    getCurrentStoredUser;


window.showToast =
    showToast;


window.showAlert =
    showAlert;


window.escapeHtml =
    escapeHtml;


window.formatDate =
    formatDate;


window.formatDateTime =
    formatDateTime;


window.displayValue =
    displayValue;

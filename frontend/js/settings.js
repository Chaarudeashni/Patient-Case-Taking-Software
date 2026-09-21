/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   Settings
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeSettings
);


function initializeSettings() {

    var pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        return;
    }

    renderSettingsPage();
    setupSettingsEvents();
    loadCurrentUser();
}


/* =========================================================
   PAGE
   ========================================================= */

function renderSettingsPage() {

    var pageContent =
        document.getElementById("pageContent");

    pageContent.innerHTML =
        '<div class="content-card">' +

            '<div class="card-header">' +
                '<div>' +
                    '<h3>Clinician Profile</h3>' +
                    '<p>View your current account information.</p>' +
                '</div>' +
            '</div>' +

            '<div class="settings-profile">' +

                '<div class="settings-avatar" id="settingsAvatar">' +
                    'C' +
                '</div>' +

                '<div class="settings-profile-info">' +
                    '<h3 id="settingsUsername">Clinician</h3>' +
                    '<span id="settingsRole">Clinician</span>' +
                '</div>' +

            '</div>' +

            '<div class="form-grid">' +

                '<div class="form-group">' +
                    '<label>Username</label>' +
                    '<input type="text" id="settingsUsernameInput" readonly>' +
                '</div>' +

                '<div class="form-group">' +
                    '<label>Role</label>' +
                    '<input type="text" id="settingsRoleInput" readonly>' +
                '</div>' +

            '</div>' +

        '</div>' +


        '<div class="content-card">' +

            '<div class="card-header">' +
                '<div>' +
                    '<h3>Application Settings</h3>' +
                    '<p>Application and connection status.</p>' +
                '</div>' +
            '</div>' +

            '<div class="settings-list">' +

                '<div class="settings-row">' +
                    '<div>' +
                        '<strong>Clinical Workspace</strong>' +
                        '<p>Patient case management workspace</p>' +
                    '</div>' +
                    '<span class="badge badge-success">Active</span>' +
                '</div>' +

                '<div class="settings-row">' +
                    '<div>' +
                        '<strong>Backend API</strong>' +
'<p>https://patient-case-taking-software-8sfq.onrender.com</p>'
                    '</div>' +
                    '<span class="badge badge-primary" id="apiStatusBadge">' +
                        'Checking...' +
                    '</span>' +
                '</div>' +

                '<div class="settings-row">' +
                    '<div>' +
                        '<strong>Database</strong>' +
                        '<p>Patient clinical database</p>' +
                    '</div>' +
                    '<span class="badge badge-success">Connected</span>' +
                '</div>' +

            '</div>' +

        '</div>' +


        '<div class="content-card">' +

            '<div class="card-header">' +
                '<div>' +
                    '<h3>Session</h3>' +
                    '<p>Manage your current application session.</p>' +
                '</div>' +
            '</div>' +

            '<div class="settings-list">' +

                '<div class="settings-row">' +

                    '<div>' +
                        '<strong>Current Session</strong>' +
                        '<p>You are currently signed in.</p>' +
                    '</div>' +

                    '<button ' +
                        'type="button" ' +
                        'class="secondary-button" ' +
                        'id="settingsLogoutButton">' +
                        'Logout' +
                    '</button>' +

                '</div>' +

                '<div class="settings-row">' +

                    '<div>' +
                        '<strong>Local Session Data</strong>' +
                        '<p>Clear the locally stored login session.</p>' +
                    '</div>' +

                    '<button ' +
                        'type="button" ' +
                        'class="danger-button" ' +
                        'id="clearSessionButton">' +
                        'Clear Session' +
                    '</button>' +

                '</div>' +

            '</div>' +

        '</div>' +


        '<div class="content-card">' +

            '<div class="card-header">' +
                '<div>' +
                    '<h3>About</h3>' +
                    '<p>Patient Case Taking Software</p>' +
                '</div>' +
            '</div>' +

            '<div class="about-content">' +

                '<div class="about-icon">+</div>' +

                '<div>' +

                    '<h3>Patient Case Taking Software</h3>' +

                    '<p>' +
                        'Clinical case management system for patient ' +
                        'information, clinical records, consultations, ' +
                        'appointments and follow-up management.' +
                    '</p>' +

                    '<span class="about-version">SIH26047</span>' +

                '</div>' +

            '</div>' +

        '</div>';
}


/* =========================================================
   USER
   ========================================================= */

function loadCurrentUser() {

    var user = null;

    try {

        if (
            typeof window.getStoredUser === "function"
        ) {
            user =
                window.getStoredUser();
        }

    } catch (error) {

        console.error(
            "Unable to load user:",
            error
        );
    }


    if (!user) {
        return;
    }


    var username =
        user.username ||
        user.name ||
        "Clinician";


    var role =
        user.role ||
        "Clinician";


    var usernameHeading =
        document.getElementById(
            "settingsUsername"
        );


    var roleHeading =
        document.getElementById(
            "settingsRole"
        );


    var usernameInput =
        document.getElementById(
            "settingsUsernameInput"
        );


    var roleInput =
        document.getElementById(
            "settingsRoleInput"
        );


    var avatar =
        document.getElementById(
            "settingsAvatar"
        );


    if (usernameHeading) {
        usernameHeading.textContent =
            username;
    }


    if (roleHeading) {
        roleHeading.textContent =
            role;
    }


    if (usernameInput) {
        usernameInput.value =
            username;
    }


    if (roleInput) {
        roleInput.value =
            role;
    }


    if (avatar) {
        avatar.textContent =
            username
                .charAt(0)
                .toUpperCase();
    }
}


/* =========================================================
   EVENTS
   ========================================================= */

function setupSettingsEvents() {

    var logoutButton =
        document.getElementById(
            "settingsLogoutButton"
        );


    if (logoutButton) {

        logoutButton.addEventListener(
            "click",
            handleSettingsLogout
        );
    }


    var clearSessionButton =
        document.getElementById(
            "clearSessionButton"
        );


    if (clearSessionButton) {

        clearSessionButton.addEventListener(
            "click",
            handleClearSession
        );
    }


    checkApiStatus();
}


/* =========================================================
   LOGOUT
   ========================================================= */

function handleSettingsLogout() {

    var confirmed =
        window.confirm(
            "Are you sure you want to logout?"
        );


    if (!confirmed) {
        return;
    }


    if (
        typeof window.clearStoredUser === "function"
    ) {

        window.clearStoredUser();

    } else {

        localStorage.removeItem(
            "currentUser"
        );
    }


    window.location.href =
        "login.html";
}


function handleClearSession() {

    var confirmed =
        window.confirm(
            "Clear the current local session?"
        );


    if (!confirmed) {
        return;
    }


    if (
        typeof window.clearStoredUser === "function"
    ) {

        window.clearStoredUser();

    } else {

        localStorage.removeItem(
            "currentUser"
        );
    }


    if (
        typeof window.showToast === "function"
    ) {

        window.showToast(
            "Session cleared.",
            "success"
        );
    }


    setTimeout(
        function () {

            window.location.href =
                "login.html";

        },
        700
    );
}


/* =========================================================
   API STATUS
   ========================================================= */

function checkApiStatus() {

    var badge =
        document.getElementById(
            "apiStatusBadge"
        );


    if (!badge) {
        return;
    }


    fetch(
        "http://127.0.0.1:8000/health"
    )

    .then(
        function (response) {

            if (response.ok) {

                badge.textContent =
                    "Online";

                badge.className =
                    "badge badge-success";

            } else {

                badge.textContent =
                    "Unavailable";

                badge.className =
                    "badge badge-danger";
            }
        }
    )

    .catch(
        function (error) {

            console.error(
                "API status error:",
                error
            );

            badge.textContent =
                "Offline";

            badge.className =
                "badge badge-danger";
        }
    );
}

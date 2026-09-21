// =========================================================
// LOGIN
// =========================================================

const LOGIN_API_URL = "https://patient-case-taking-software-8sfq.onrender.com/login";

window.isLoggedIn = function () {
    return localStorage.getItem("currentUser") !== null;
};

window.getCurrentUser = function () {
    try {
        return JSON.parse(localStorage.getItem("currentUser"));
    } catch (error) {
        return null;
    }
};

window.saveCurrentUser = function (user) {
    localStorage.setItem("currentUser", JSON.stringify(user));
};

document.addEventListener("DOMContentLoaded", function () {

    // If already logged in, go to application
    if (window.isLoggedIn()) {
        window.location.href = "index.html";
        return;
    }

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        console.error("loginForm not found");
        return;
    }

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const usernameElement = document.getElementById("username");
        const passwordElement = document.getElementById("password");
        const errorElement = document.getElementById("loginError");
        const loginButton = loginForm.querySelector(
            "button[type='submit']"
        );

        const username = usernameElement
            ? usernameElement.value.trim()
            : "";

        const password = passwordElement
            ? passwordElement.value
            : "";

        // Clear previous error
        if (errorElement) {
            errorElement.textContent = "";
            errorElement.style.display = "none";
        }

        if (!username || !password) {
            showLoginError("Please enter username and password.");
            return;
        }

        try {
            if (loginButton) {
                loginButton.disabled = true;
                loginButton.textContent = "Logging in...";
            }

            /*
             * FastAPI endpoint:
             *
             * POST /login
             * username: str
             * password: str
             */

            const body = new URLSearchParams();

            body.append("username", username);
            body.append("password", password);

            const loginUrl =
    LOGIN_API_URL +
    "?username=" + encodeURIComponent(username) +
    "&password=" + encodeURIComponent(password);

const response = await fetch(loginUrl, {
    method: "POST"
});

            const responseText = await response.text();

            let data = null;

            try {
                data = JSON.parse(responseText);
            } catch (error) {
                data = null;
            }

            console.log("Login response:", data);

            // Backend returned an error
            if (!response.ok) {

                let message = "Invalid username or password.";

                if (data) {
                    if (typeof data.detail === "string") {
                        message = data.detail;
                    } else if (Array.isArray(data.detail)) {
                        message = data.detail
                            .map(function (item) {
                                if (typeof item === "string") {
                                    return item;
                                }

                                if (item && item.msg) {
                                    return item.msg;
                                }

                                return JSON.stringify(item);
                            })
                            .join(", ");
                    } else if (typeof data.message === "string") {
                        message = data.message;
                    }
                }

                showLoginError(message);
                return;
            }

            // Make sure we received the expected login response
            if (
                !data ||
                data.authenticated !== true
            ) {
                showLoginError(
                    "Login failed. Invalid response from server."
                );
                return;
            }

            /*
             * Backend returns:
             *
             * {
             *   authenticated: true,
             *   user_id: 1,
             *   username: "...",
             *   role: "..."
             * }
             */

            const currentUser = {
                id: data.user_id,
                user_id: data.user_id,
                username: data.username,
                role: data.role,
                authenticated: true
            };

            // Save user
            window.saveCurrentUser(currentUser);

            // Also save individual values for compatibility
            localStorage.setItem(
                "user_id",
                String(data.user_id)
            );

            localStorage.setItem(
                "username",
                data.username || ""
            );

            localStorage.setItem(
                "role",
                data.role || ""
            );

            localStorage.setItem(
                "isLoggedIn",
                "true"
            );

            console.log(
                "Login successful:",
                currentUser
            );

            // Go to application
            window.location.href = "index.html";

        } catch (error) {

            console.error(
                "Login connection error:",
                error
            );

            showLoginError(
                "Unable to connect to the backend. " +
                "Make sure the backend server is running."
            );

        } finally {

            if (loginButton) {
                loginButton.disabled = false;
                loginButton.textContent = "Login";
            }
        }
    });

    // =====================================================
    // PASSWORD SHOW / HIDE
    // =====================================================

    const togglePassword =
        document.getElementById("togglePassword");

    if (togglePassword) {

        togglePassword.addEventListener(
            "click",
            function () {

                const passwordElement =
                    document.getElementById("password");

                if (!passwordElement) {
                    return;
                }

                if (
                    passwordElement.type === "password"
                ) {
                    passwordElement.type = "text";
                    togglePassword.textContent = "Hide";
                } else {
                    passwordElement.type = "password";
                    togglePassword.textContent = "Show";
                }
            }
        );
    }
});


// =========================================================
// SHOW LOGIN ERROR
// =========================================================

function showLoginError(message) {

    const errorElement =
        document.getElementById("loginError");

    if (errorElement) {

        errorElement.textContent =
            String(message);

        errorElement.style.display = "block";

    } else {

        alert(String(message));
    }
}

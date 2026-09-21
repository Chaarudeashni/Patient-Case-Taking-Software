// =========================================================
// API CONFIGURATION
// =========================================================

const API_BASE_URL = "https://patient-case-taking-software-8sfq.onrender.com";


// =========================================================
// STORED USER HELPERS
// =========================================================

function getStoredUser() {
    try {
        const stored = localStorage.getItem("currentUser");

        if (!stored) {
            return null;
        }

        return JSON.parse(stored);

    } catch (error) {
        console.error("Unable to read stored user:", error);
        return null;
    }
}


function saveStoredUser(user) {
    localStorage.setItem(
        "currentUser",
        JSON.stringify(user)
    );
}


function clearStoredUser() {
    localStorage.removeItem("currentUser");
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    localStorage.removeItem("isLoggedIn");
}


function isLoggedIn() {
    return getStoredUser() !== null;
}


// =========================================================
// GENERIC API REQUEST
// =========================================================

async function apiRequest(endpoint, options = {}) {

    const response = await fetch(
        API_BASE_URL + endpoint,
        {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        }
    );

    const text = await response.text();

    let data;

    try {
        data = text ? JSON.parse(text) : null;
    } catch {
        data = text;
    }

    if (!response.ok) {

        let message = "API request failed";

        if (data) {

            if (typeof data.detail === "string") {
                message = data.detail;

            } else if (Array.isArray(data.detail)) {

                message = data.detail
                    .map(item => {
                        if (typeof item === "string") {
                            return item;
                        }

                        return item.msg ||
                            JSON.stringify(item);
                    })
                    .join(", ");

            } else if (
                typeof data.message === "string"
            ) {
                message = data.message;
            }
        }

        throw new Error(message);
    }

    return data;
}


// =========================================================
// PATIENTS
// =========================================================

async function getPatients() {
    return await apiRequest("/patients");
}


async function getPatient(patientId) {
    return await apiRequest(
        `/patients/${patientId}`
    );
}


async function createPatient(patientData) {
    return await apiRequest(
        "/patients",
        {
            method: "POST",
            body: JSON.stringify(patientData)
        }
    );
}


// =========================================================
// CASES
// =========================================================

async function getCases() {
    return await apiRequest("/cases");
}


async function getCase(caseId) {
    return await apiRequest(
        `/cases/${caseId}`
    );
}


async function getPatientCases(patientId) {
    try {
        const cases = await getCases();

        if (!Array.isArray(cases)) {
            return [];
        }

        return cases.filter(function (caseItem) {
            return String(caseItem.patient_id) === String(patientId);
        });

    } catch (error) {
        console.error("Failed to get patient cases:", error);
        return [];
    }
}


async function deleteCase(caseId) {
    return await apiRequest(
        `/cases/${caseId}`,
        {
            method: "DELETE"
        }
    );
}


// =========================================================
// APPOINTMENTS
// =========================================================

async function getAppointments() {
    return await apiRequest("/appointments");
}


async function createAppointment(data) {
    return await apiRequest(
        "/appointments",
        {
            method: "POST",
            body: JSON.stringify(data)
        }
    );
}


async function deleteAppointment(appointmentId) {
    return await apiRequest(
        `/appointments/${appointmentId}`,
        {
            method: "DELETE"
        }
    );
}


// =========================================================
// FOLLOWUPS
// =========================================================

async function getFollowups() {
    return await apiRequest("/followups");
}


async function createFollowup(data) {
    return await apiRequest(
        "/followups",
        {
            method: "POST",
            body: JSON.stringify(data)
        }
    );
}


// =========================================================
// USERS
// =========================================================

async function getUsers() {
    return await apiRequest("/users");
}


// =========================================================
// HEALTH
// =========================================================

async function checkBackendHealth() {
    return await apiRequest("/health");
}


// =========================================================
// LOGIN
// =========================================================

async function login(username, password) {

    const url =
        API_BASE_URL +
        "/login" +
        "?username=" +
        encodeURIComponent(username) +
        "&password=" +
        encodeURIComponent(password);

    const response = await fetch(url, {
        method: "POST"
    });

    const text = await response.text();

    let data;

    try {
        data = text ? JSON.parse(text) : null;
    } catch {
        data = null;
    }

    if (!response.ok) {

        let message = "Invalid username or password.";

        if (data) {

            if (typeof data.detail === "string") {
                message = data.detail;

            } else if (Array.isArray(data.detail)) {

                message = data.detail
                    .map(item => {
                        if (typeof item === "string") {
                            return item;
                        }

                        return item.msg ||
                            JSON.stringify(item);
                    })
                    .join(", ");
            }
        }

        throw new Error(message);
    }

    return data;
}


// =========================================================
// WINDOW EXPORTS
// =========================================================

window.apiRequest = apiRequest;

window.getStoredUser = getStoredUser;
window.saveStoredUser = saveStoredUser;
window.clearStoredUser = clearStoredUser;
window.isLoggedIn = isLoggedIn;

window.getPatients = getPatients;
window.getPatient = getPatient;
window.createPatient = createPatient;

window.getCases = getCases;
window.getCase = getCase;
window.getPatientCases = getPatientCases;
window.deleteCase = deleteCase;

window.getAppointments = getAppointments;
window.createAppointment = createAppointment;
window.deleteAppointment = deleteAppointment;

window.getFollowups = getFollowups;
window.createFollowup = createFollowup;

window.getUsers = getUsers;

window.checkBackendHealth = checkBackendHealth;

window.login = login;

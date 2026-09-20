/* ============================================================
   FILE: frontend_web/js/home.js
   ============================================================ */

const API_URL =
    localStorage.getItem("api_url") ||
    "http://127.0.0.1:8000";


const username =
    localStorage.getItem("username") ||
    "Doctor";


if (
    localStorage.getItem("loggedIn") !== "true"
) {
    window.location.href = "login.html";
}


document.getElementById(
    "doctorName"
).textContent = username;


document.getElementById(
    "welcomeDoctor"
).textContent = username;



/* DATE */

const today =
    new Date();


document.getElementById(
    "currentDate"
).textContent =
    today.toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        }
    );



/* LOGOUT */

document.getElementById(
    "logoutButton"
).addEventListener(
    "click",
    () => {

        localStorage.removeItem(
            "loggedIn"
        );

        localStorage.removeItem(
            "username"
        );

        localStorage.removeItem(
            "user"
        );

        window.location.href =
            "login.html";
    }
);



/* ============================================================
   LOAD PATIENTS
   ============================================================ */

async function loadPatients() {

    try {

        const response =
            await fetch(
                `${API_URL}/patients`
            );


        if (!response.ok) {
            throw new Error(
                "Unable to load patients."
            );
        }


        const patients =
            await response.json();


        document.getElementById(
            "totalPatients"
        ).textContent =
            patients.length;


        const table =
            document.getElementById(
                "recentPatientsTable"
            );


        if (!patients.length) {

            table.innerHTML = `
                <tr>
                    <td colspan="5">
                        No patients found.
                    </td>
                </tr>
            `;

            return;
        }


        const recent =
            patients.slice(0, 5);


        table.innerHTML =
            recent.map(
                patient => {

                    const name =
                        `${patient.first_name || ""} ${patient.last_name || ""}`
                        .trim();


                    return `
                        <tr>

                            <td>
                                <strong>
                                    ${patient.patient_id || "-"}
                                </strong>
                            </td>

                            <td>
                                ${name || "-"}
                            </td>

                            <td>
                                ${patient.gender || "-"}
                            </td>

                            <td>
                                ${patient.date_of_birth || "-"}
                            </td>

                            <td>
                                <span class="status-badge status-active">
                                    Active
                                </span>
                            </td>

                        </tr>
                    `;

                }
            ).join("");


    } catch (error) {

        document.getElementById(
            "recentPatientsTable"
        ).innerHTML = `
            <tr>
                <td colspan="5">
                    Unable to load patients.
                </td>
            </tr>
        `;

    }

}



/* ============================================================
   LOAD CASES
   ============================================================ */

async function loadCases() {

    try {

        const response =
            await fetch(
                `${API_URL}/cases`
            );


        if (!response.ok) {
            throw new Error();
        }


        const cases =
            await response.json();


        const active =
            cases.filter(
                item =>
                    !item.status ||
                    item.status.toLowerCase() ===
                    "active"
            );


        document.getElementById(
            "activeCases"
        ).textContent =
            active.length;


    } catch (_) {

        document.getElementById(
            "activeCases"
        ).textContent =
            "—";

    }

}



/* ============================================================
   LOAD APPOINTMENTS
   ============================================================ */

async function loadAppointments() {

    const container =
        document.getElementById(
            "appointmentList"
        );


    try {

        const response =
            await fetch(
                `${API_URL}/appointments`
            );


        if (!response.ok) {
            throw new Error();
        }


        const appointments =
            await response.json();


        const todayString =
            new Date()
                .toISOString()
                .split("T")[0];


        const todayAppointments =
            appointments.filter(
                appointment => {

                    if (
                        !appointment.appointment_date
                    ) {
                        return true;
                    }

                    return appointment
                        .appointment_date
                        .startsWith(
                            todayString
                        );
                }
            );


        document.getElementById(
            "todayAppointments"
        ).textContent =
            todayAppointments.length;


        if (!todayAppointments.length) {

            container.innerHTML = `
                <div class="loading-state">
                    No appointments scheduled.
                </div>
            `;

            return;
        }


        container.innerHTML =
            todayAppointments
                .slice(0, 5)
                .map(
                    appointment => `

                    <div class="appointment-item">

                        <div class="appointment-time">
                            ${
                                appointment.appointment_time ||
                                "—"
                            }
                        </div>

                        <div class="appointment-info">

                            <strong>
                                Patient
                                ${
                                    appointment.patient_id ||
                                    ""
                                }
                            </strong>

                            <span>
                                ${
                                    appointment.appointment_type ||
                                    "Clinical consultation"
                                }
                            </span>

                        </div>

                        <span class="appointment-status">
                            ${
                                appointment.status ||
                                "Scheduled"
                            }
                        </span>

                    </div>

                `
                )
                .join("");


    } catch (_) {

        container.innerHTML = `
            <div class="loading-state">
                Unable to load appointments.
            </div>
        `;

        document.getElementById(
            "todayAppointments"
        ).textContent = "—";

    }

}



/* ============================================================
   LOAD FOLLOW UPS
   ============================================================ */

async function loadFollowups() {

    try {

        const response =
            await fetch(
                `${API_URL}/followups`
            );


        if (!response.ok) {
            throw new Error();
        }


        const followups =
            await response.json();


        document.getElementById(
            "pendingFollowups"
        ).textContent =
            followups.length;


    } catch (_) {

        document.getElementById(
            "pendingFollowups"
        ).textContent =
            "—";

    }

}



/* ============================================================
   SEARCH
   ============================================================ */

document.getElementById(
    "globalSearch"
).addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {

            const query =
                event.target.value.trim();

            if (query) {

                window.location.href =
                    `patients.html?search=${encodeURIComponent(query)}`;

            }

        }

    }
);



/* ============================================================
   INITIAL LOAD
   ============================================================ */

loadPatients();
loadCases();
loadAppointments();
loadFollowups();
/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   Dashboard
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);


async function initializeDashboard() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        return;
    }

    try {

        const [
            patients,
            cases,
            followups,
            appointments
        ] = await Promise.all([
            getPatients(),
            getCases(),
            getFollowups(),
            getAppointments()
        ]);


        renderDashboard({
            patients,
            cases,
            followups,
            appointments
        });

    } catch (error) {

        console.error(
            "Dashboard loading error:",
            error
        );

        renderDashboardError(
            error.message
        );
    }
}


/* =========================================================
   RENDER DASHBOARD
   ========================================================= */

function renderDashboard(data) {

    const pageContent =
        document.getElementById("pageContent");

    const patients =
        Array.isArray(data.patients)
            ? data.patients
            : [];

    const cases =
        Array.isArray(data.cases)
            ? data.cases
            : [];

    const followups =
        Array.isArray(data.followups)
            ? data.followups
            : [];

    const appointments =
        Array.isArray(data.appointments)
            ? data.appointments
            : [];


    const activeCases =
        cases.filter(
            item =>
                String(item.status || "")
                    .toLowerCase() === "active"
        );


    const upcomingAppointments =
        appointments.filter(
            item => !isPastDate(
                item.appointment_date ||
                item.date ||
                item.scheduled_at
            )
        );


    pageContent.innerHTML = `

        <!-- Welcome -->

        <div class="welcome-banner">

            <div>

                <span class="eyebrow">
                    Clinical Workspace
                </span>

                <h2>
                    Welcome back, ${escapeHtml(getClinicianName())}
                </h2>

                <p>
                    Manage patients, clinical cases,
                    consultations and follow-ups
                    from one centralized workspace.
                </p>

            </div>

            <br>

        </div>


        <!-- Statistics -->

        <div class="stats-grid">

            <div class="stat-card">

                <div class="stat-card-icon">
                    ♙
                </div>

                <div class="stat-card-content">

                    <span>
                        Total Patients
                    </span>

                    <strong>
                        ${patients.length}
                    </strong>

                    <small>
                        Registered patients
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    ▣
                </div>

                <div class="stat-card-content">

                    <span>
                        Total Cases
                    </span>

                    <strong>
                        ${cases.length}
                    </strong>

                    <small>
                        Clinical cases
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    +
                </div>

                <div class="stat-card-content">

                    <span>
                        Active Cases
                    </span>

                    <strong>
                        ${activeCases.length}
                    </strong>

                    <small>
                        Currently active
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    □
                </div>

                <div class="stat-card-content">

                    <span>
                        Appointments
                    </span>

                    <strong>
                        ${upcomingAppointments.length}
                    </strong>

                    <small>
                        Upcoming appointments
                    </small>

                </div>

            </div>

        </div>


        <!-- Dashboard Columns -->

        <div class="dashboard-grid">


            <!-- Recent Patients -->

            <div class="content-card">

                <div class="card-header">

                    <div>

                        <h3>
                            Recent Patients
                        </h3>

                        <p>
                            Recently registered patients
                        </p>

                    </div>

                    <button
                        class="text-button"
                        type="button"
                        id="viewPatientsButton"
                    >
                        View All
                    </button>

                </div>


                <div
                    class="table-wrapper"
                    id="recentPatients"
                >

                    ${renderRecentPatients(patients)}

                </div>

            </div>


            <!-- Upcoming Appointments -->

            <div class="content-card">

                <div class="card-header">

                    <div>

                        <h3>
                            Upcoming Appointments
                        </h3>

                        <p>
                            Scheduled patient visits
                        </p>

                    </div>

                    <button
                        class="text-button"
                        type="button"
                        id="viewAppointmentsButton"
                    >
                        View All
                    </button>

                </div>


                <div
                    class="appointment-list"
                    id="upcomingAppointments"
                >

                    ${renderUpcomingAppointments(
                        upcomingAppointments
                    )}

                </div>

            </div>

        </div>


        <!-- Recent Cases -->

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Recent Clinical Cases
                    </h3>

                    <p>
                        Latest cases in the system
                    </p>

                </div>

                <button
                    class="text-button"
                    type="button"
                    id="viewCasesButton"
                >
                    View Records
                </button>

            </div>


            <div class="table-wrapper">

                ${renderRecentCases(cases)}

            </div>

        </div>


        <!-- Follow-up Summary -->

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Follow-up Summary
                    </h3>

                    <p>
                        Current follow-up records
                    </p>

                </div>

                <button
                    class="text-button"
                    type="button"
                    id="viewFollowupsButton"
                >
                    View Follow-ups
                </button>

            </div>


            <div class="summary-row">

                <div class="summary-item">

                    <span>
                        Total Follow-ups
                    </span>

                    <strong>
                        ${followups.length}
                    </strong>

                </div>


                <div class="summary-item">

                    <span>
                        Upcoming
                    </span>

                    <strong>
                        ${
                            followups.filter(
                                item =>
                                    !isPastDate(
                                        item.followup_date ||
                                        item.date ||
                                        item.scheduled_at
                                    )
                            ).length
                        }
                    </strong>

                </div>


                <div class="summary-item">

                    <span>
                        Completed
                    </span>

                    <strong>
                        ${
                            followups.filter(
                                item =>
                                    String(
                                        item.status || ""
                                    ).toLowerCase() ===
                                    "completed"
                            ).length
                        }
                    </strong>

                </div>

            </div>

        </div>

    `;


    setupDashboardNavigation();
}


/* =========================================================
   RECENT PATIENTS
   ========================================================= */

function renderRecentPatients(patients) {

    if (!patients.length) {

        return `
            <div class="empty-state">
                <div class="empty-state-icon">♙</div>
                <h3>No patients found</h3>
                <p>
                    Add your first patient to get started.
                </p>
            </div>
        `;
    }


    const recent =
        [...patients]
            .sort(
                (a, b) =>
                    Number(b.id || 0) -
                    Number(a.id || 0)
            )
            .slice(0, 5);


    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Patient
                    </th>

                    <th>
                        Patient ID
                    </th>

                    <th>
                        Gender
                    </th>

                    <th>
                        Contact
                    </th>

                </tr>

            </thead>

            <tbody>

                ${recent.map(patient => `

                    <tr>

                        <td>
                            <strong>
                                ${escapeHtml(
                                    patient.name ||
                                    patient.full_name ||
                                    "-"
                                )}
                            </strong>
                        </td>

                        <td>
                            ${escapeHtml(
                                patient.patient_id ||
                                "-"
                            )}
                        </td>

                        <td>
                            ${escapeHtml(
                                patient.gender ||
                                "-"
                            )}
                        </td>

                        <td>
                            ${escapeHtml(
                                patient.phone ||
                                patient.contact_number ||
                                "-"
                            )}
                        </td>

                    </tr>

                `).join("")}

            </tbody>

        </table>
    `;
}


/* =========================================================
   UPCOMING APPOINTMENTS
   ========================================================= */

function renderUpcomingAppointments(appointments) {

    if (!appointments.length) {

        return `
            <div class="empty-state">
                <div class="empty-state-icon">□</div>
                <h3>No upcoming appointments</h3>
                <p>
                    No scheduled appointments found.
                </p>
            </div>
        `;
    }


    const upcoming =
        [...appointments]
            .sort(
                (a, b) =>
                    getDateValue(a) -
                    getDateValue(b)
            )
            .slice(0, 5);


    return upcoming.map(item => {

        const date =
            item.appointment_date ||
            item.date ||
            item.scheduled_at;

        const patientName =
            item.patient_name ||
            item.patient ||
            item.name ||
            "Patient";


        return `

            <div class="appointment-item">

                <div class="appointment-date">

                    <strong>
                        ${formatDate(date)}
                    </strong>

                    ${
                        item.appointment_time ||
                        item.time
                            ? `
                                <span>
                                    ${
                                        item.appointment_time ||
                                        item.time
                                    }
                                </span>
                              `
                            : ""
                    }

                </div>


                <div class="appointment-info">

                    <strong>
                        ${escapeHtml(patientName)}
                    </strong>

                    <span>
                        ${
                            escapeHtml(
                                item.reason ||
                                item.purpose ||
                                item.type ||
                                "Clinical appointment"
                            )
                        }
                    </span>

                </div>

            </div>
        `;

    }).join("");
}


/* =========================================================
   RECENT CASES
   ========================================================= */

function renderRecentCases(cases) {

    if (!cases.length) {

        return `
            <div class="empty-state">
                <div class="empty-state-icon">▣</div>
                <h3>No clinical cases found</h3>
                <p>
                    Create a new case to begin.
                </p>
            </div>
        `;
    }


    const recent =
        [...cases]
            .sort(
                (a, b) =>
                    Number(b.id || 0) -
                    Number(a.id || 0)
            )
            .slice(0, 5);


    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Case ID
                    </th>

                    <th>
                        Patient
                    </th>

                    <th>
                        Case Date
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>

            <tbody>

                ${recent.map(item => `

                    <tr>

                        <td>
                            <strong>
                                ${escapeHtml(
                                    item.case_id ||
                                    item.id ||
                                    "-"
                                )}
                            </strong>
                        </td>

                        <td>
                            ${escapeHtml(
                                item.patient_name ||
                                item.patient ||
                                item.patient_id ||
                                "-"
                            )}
                        </td>

                        <td>
                            ${formatDate(
                                item.case_date ||
                                item.date ||
                                item.created_at
                            )}
                        </td>

                        <td>

                            <span class="
                                badge
                                ${
                                    String(
                                        item.status || ""
                                    ).toLowerCase() ===
                                    "active"
                                        ? "badge-success"
                                        : "badge-secondary"
                                }
                            ">

                                ${escapeHtml(
                                    item.status ||
                                    "Unknown"
                                )}

                            </span>

                        </td>

                    </tr>

                `).join("")}

            </tbody>

        </table>
    `;
}


/* =========================================================
   NAVIGATION
   ========================================================= */

function setupDashboardNavigation() {

    document
        .querySelectorAll(
            "[data-action-url]"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                function () {

                    window.location.href =
                        this.dataset.actionUrl;
                }
            );
        });


    const navigationMap = {

        viewPatientsButton:
            "patients.html",

        viewAppointmentsButton:
            "appointments.html",

        viewCasesButton:
            "clinical-records.html",

        viewFollowupsButton:
            "follow-ups.html"
    };


    Object.entries(navigationMap)
        .forEach(([id, url]) => {

            const button =
                document.getElementById(id);

            if (!button) {
                return;
            }

            button.addEventListener(
                "click",
                function () {

                    window.location.href =
                        url;
                }
            );
        });
}


/* =========================================================
   CLINICIAN NAME
   ========================================================= */

function getClinicianName() {

    const user =
        getStoredUser();

    if (!user) {
        return "Clinician";
    }

    return (
        user.full_name ||
        user.name ||
        user.username ||
        "Clinician"
    );
}


/* =========================================================
   DATE HELPERS
   ========================================================= */

function getDateValue(item) {

    const value =
        item.appointment_date ||
        item.followup_date ||
        item.date ||
        item.scheduled_at ||
        item.created_at;


    if (!value) {
        return Number.MAX_SAFE_INTEGER;
    }


    const date =
        new Date(value);

    const time =
        date.getTime();

    return Number.isNaN(time)
        ? Number.MAX_SAFE_INTEGER
        : time;
}


function isPastDate(value) {

    if (!value) {
        return false;
    }


    const date =
        new Date(value);


    if (Number.isNaN(
        date.getTime()
    )) {
        return false;
    }


    const today =
        new Date();

    today.setHours(
        0, 0, 0, 0
    );


    date.setHours(
        0, 0, 0, 0
    );


    return date < today;
}


/* =========================================================
   ERROR STATE
   ========================================================= */

function renderDashboardError(message) {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    if (!pageContent) {
        return;
    }


    pageContent.innerHTML = `

        <div class="content-card">

            <div class="alert alert-error">

                Unable to load dashboard data.

                <br><br>

                ${escapeHtml(
                    message ||
                    "Unknown error"
                )}

            </div>


            <button
                class="primary-button"
                type="button"
                onclick="window.location.reload()"
            >
                Retry
            </button>

        </div>

    `;
}
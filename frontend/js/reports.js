/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   Reports
   ========================================================= */

let reportPatients = [];
let reportCases = [];
let reportFollowups = [];
let reportAppointments = [];


document.addEventListener(
    "DOMContentLoaded",
    initializeReports
);


async function initializeReports() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        return;
    }


    renderReportsLoading();


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


        reportPatients =
            Array.isArray(patients)
                ? patients
                : [];


        reportCases =
            Array.isArray(cases)
                ? cases
                : [];


        reportFollowups =
            Array.isArray(followups)
                ? followups
                : [];


        reportAppointments =
            Array.isArray(appointments)
                ? appointments
                : [];


        renderReportsPage();

        setupReportEvents();

    } catch (error) {

        console.error(
            "Reports loading error:",
            error
        );

        renderReportsError(
            error.message
        );
    }
}


/* =========================================================
   PAGE
   ========================================================= */

function renderReportsPage() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="section-header">

            <div>

                <h2>
                    Clinical Reports
                </h2>

                <p>
                    View a summary of patients,
                    cases, appointments and follow-ups.
                </p>

            </div>

<br>
            <button
                type="button"
                class="secondary-button"
                id="refreshReportsButton"
            >
                ↻ Refresh
            </button>

        </div>

<br>
        <!-- Summary Cards -->

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
                        ${reportPatients.length}
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
                        ${reportCases.length}
                    </strong>

                    <small>
                        Clinical cases
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
                        ${reportAppointments.length}
                    </strong>

                    <small>
                        Appointment records
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    ↻
                </div>

                <div class="stat-card-content">

                    <span>
                        Follow-ups
                    </span>

                    <strong>
                        ${reportFollowups.length}
                    </strong>

                    <small>
                        Follow-up records
                    </small>

                </div>

            </div>

        </div>


        <!-- Case Status -->

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Case Status Overview
                    </h3>

                    <p>
                        Current distribution of clinical cases.
                    </p>

                </div>

            </div>


            <div class="report-summary-grid">

                <div class="report-summary-item">

                    <span class="report-label">
                        Active Cases
                    </span>

                    <strong>
                        ${countCaseStatus("active")}
                    </strong>

                </div>


                <div class="report-summary-item">

                    <span class="report-label">
                        Completed Cases
                    </span>

                    <strong>
                        ${countCaseStatus("completed")}
                    </strong>

                </div>


                <div class="report-summary-item">

                    <span class="report-label">
                        Closed Cases
                    </span>

                    <strong>
                        ${countCaseStatus("closed")}
                    </strong>

                </div>


                <div class="report-summary-item">

                    <span class="report-label">
                        Other
                    </span>

                    <strong>
                        ${countOtherCaseStatuses()}
                    </strong>

                </div>

            </div>

        </div>


        <!-- Appointment Status -->

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Appointment Overview
                    </h3>

                    <p>
                        Appointment status distribution.
                    </p>

                </div>

            </div>


            <div class="report-summary-grid">

                <div class="report-summary-item">

                    <span class="report-label">
                        Scheduled
                    </span>

                    <strong>
                        ${countAppointmentStatus(
                            "scheduled"
                        )}
                    </strong>

                </div>


                <div class="report-summary-item">

                    <span class="report-label">
                        Confirmed
                    </span>

                    <strong>
                        ${countAppointmentStatus(
                            "confirmed"
                        )}
                    </strong>

                </div>


                <div class="report-summary-item">

                    <span class="report-label">
                        Completed
                    </span>

                    <strong>
                        ${countAppointmentStatus(
                            "completed"
                        )}
                    </strong>

                </div>


                <div class="report-summary-item">

                    <span class="report-label">
                        Cancelled
                    </span>

                    <strong>
                        ${countAppointmentStatus(
                            "cancelled"
                        )}
                    </strong>

                </div>

            </div>

        </div>


        <!-- Recent Patients -->

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Recent Patients
                    </h3>

                    <p>
                        Recently added patient records.
                    </p>

                </div>

                <button
                    type="button"
                    class="text-button"
                    id="viewAllPatientsButton"
                >
                    View Patients →
                </button>

            </div>


            <div
                class="table-wrapper"
                id="recentPatientsTable"
            >

                ${renderRecentPatients()}

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
                        Latest clinical case records.
                    </p>

                </div>

                <button
                    type="button"
                    class="text-button"
                    id="viewClinicalRecordsButton"
                >
                    View Records →
                </button>

            </div>


            <div
                class="table-wrapper"
                id="recentCasesTable"
            >

                ${renderRecentCases()}

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
                        Scheduled future appointments.
                    </p>

                </div>

                <button
                    type="button"
                    class="text-button"
                    id="viewAppointmentsButton"
                >
                    View Appointments →
                </button>

            </div>


            <div
                class="table-wrapper"
                id="upcomingAppointmentsTable"
            >

                ${renderUpcomingAppointments()}

            </div>

        </div>

    `;
}


/* =========================================================
   RECENT PATIENTS
   ========================================================= */

function renderRecentPatients() {

    if (!reportPatients.length) {

        return renderReportEmpty(
            "No patient records available."
        );
    }


    const patients =
        [...reportPatients]
            .sort(
                (a, b) =>
                    getDateValue(
                        b.created_at ||
                        b.createdAt
                    ) -
                    getDateValue(
                        a.created_at ||
                        a.createdAt
                    )
            )
            .slice(0, 5);


    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Patient ID
                    </th>

                    <th>
                        Name
                    </th>

                    <th>
                        Gender
                    </th>

                    <th>
                        Date of Birth
                    </th>

                    <th>
                        Contact
                    </th>

                </tr>

            </thead>


            <tbody>

                ${patients.map(
                    patient => `

                        <tr>

                            <td>
                                <strong>
                                    ${escapeHtml(
                                        patient.patient_id ||
                                        "-"
                                    )}
                                </strong>
                            </td>


                            <td>
                                ${escapeHtml(
                                    patient.name ||
                                    patient.full_name ||
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
                                ${formatDate(
                                    patient.date_of_birth ||
                                    patient.dob
                                )}
                            </td>


                            <td>
                                ${escapeHtml(
                                    patient.phone ||
                                    patient.mobile ||
                                    "-"
                                )}
                            </td>

                        </tr>

                    `
                ).join("")}

            </tbody>

        </table>

    `;
}


/* =========================================================
   RECENT CASES
   ========================================================= */

function renderRecentCases() {

    if (!reportCases.length) {

        return renderReportEmpty(
            "No clinical case records available."
        );
    }


    const cases =
        [...reportCases]
            .sort(
                (a, b) =>
                    getDateValue(
                        b.case_date ||
                        b.created_at
                    ) -
                    getDateValue(
                        a.case_date ||
                        a.created_at
                    )
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

                ${cases.map(
                    clinicalCase => `

                        <tr>

                            <td>

                                <strong>
                                    ${escapeHtml(
                                        clinicalCase.case_id ||
                                        "-"
                                    )}
                                </strong>

                            </td>


                            <td>

                                ${escapeHtml(
                                    getCasePatientName(
                                        clinicalCase
                                    )
                                )}

                            </td>


                            <td>

                                ${formatDate(
                                    clinicalCase.case_date ||
                                    clinicalCase.created_at
                                )}

                            </td>


                            <td>

                                <span class="
                                    badge
                                    ${getCaseStatusClass(
                                        clinicalCase.status
                                    )}
                                ">

                                    ${escapeHtml(
                                        clinicalCase.status ||
                                        "Active"
                                    )}

                                </span>

                            </td>

                        </tr>

                    `
                ).join("")}

            </tbody>

        </table>

    `;
}


/* =========================================================
   UPCOMING APPOINTMENTS
   ========================================================= */

function renderUpcomingAppointments() {

    const upcoming =
        reportAppointments
            .filter(
                appointment => {

                    const date =
                        appointment.appointment_date ||
                        appointment.date ||
                        appointment.scheduled_at;


                    if (!date) {
                        return false;
                    }


                    const status =
                        String(
                            appointment.status || ""
                        ).toLowerCase();


                    if (
                        status === "completed" ||
                        status === "cancelled"
                    ) {

                        return false;
                    }


                    return !isPastDate(date);
                }
            )
            .sort(
                (a, b) =>
                    getDateValue(
                        a.scheduled_at ||
                        a.appointment_date ||
                        a.date
                    ) -
                    getDateValue(
                        b.scheduled_at ||
                        b.appointment_date ||
                        b.date
                    )
            )
            .slice(0, 5);


    if (!upcoming.length) {

        return renderReportEmpty(
            "No upcoming appointments."
        );
    }


    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Patient
                    </th>

                    <th>
                        Date
                    </th>

                    <th>
                        Time
                    </th>

                    <th>
                        Purpose
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                ${upcoming.map(
                    appointment => `

                        <tr>

                            <td>

                                ${escapeHtml(
                                    getAppointmentPatientName(
                                        appointment
                                    )
                                )}

                            </td>


                            <td>

                                ${formatDate(
                                    appointment.appointment_date ||
                                    appointment.date ||
                                    appointment.scheduled_at
                                )}

                            </td>


                            <td>

                                ${escapeHtml(
                                    getAppointmentTime(
                                        appointment
                                    )
                                )}

                            </td>


                            <td>

                                ${escapeHtml(
                                    appointment.purpose ||
                                    appointment.reason ||
                                    "-"
                                )}

                            </td>


                            <td>

                                <span class="
                                    badge
                                    ${getAppointmentStatusClass(
                                        appointment.status
                                    )}
                                ">

                                    ${escapeHtml(
                                        appointment.status ||
                                        "Scheduled"
                                    )}

                                </span>

                            </td>

                        </tr>

                    `
                ).join("")}

            </tbody>

        </table>

    `;
}


/* =========================================================
   CASE / APPOINTMENT HELPERS
   ========================================================= */

function getCasePatientName(
    clinicalCase
) {

    if (
        clinicalCase.patient_name
    ) {

        return clinicalCase.patient_name;
    }


    if (
        clinicalCase.patient
    ) {

        if (
            typeof clinicalCase.patient ===
            "object"
        ) {

            return (
                clinicalCase.patient.name ||
                clinicalCase.patient.full_name ||
                "Patient"
            );
        }

        return clinicalCase.patient;
    }


    if (
        clinicalCase.patient_id
    ) {

        const patient =
            reportPatients.find(
                item =>
                    Number(item.id) ===
                    Number(
                        clinicalCase.patient_id
                    )
            );


        if (patient) {

            return (
                patient.name ||
                patient.full_name ||
                "Patient"
            );
        }
    }


    return "Patient";
}


function getAppointmentPatientName(
    appointment
) {

    if (
        appointment.patient_name
    ) {

        return appointment.patient_name;
    }


    if (
        appointment.patient
    ) {

        if (
            typeof appointment.patient ===
            "object"
        ) {

            return (
                appointment.patient.name ||
                appointment.patient.full_name ||
                "Patient"
            );
        }

        return appointment.patient;
    }


    if (
        appointment.patient_id
    ) {

        const patient =
            reportPatients.find(
                item =>
                    Number(item.id) ===
                    Number(
                        appointment.patient_id
                    )
            );


        if (patient) {

            return (
                patient.name ||
                patient.full_name ||
                "Patient"
            );
        }
    }


    return "Patient";
}


function getAppointmentTime(
    appointment
) {

    if (
        appointment.appointment_time
    ) {

        return appointment.appointment_time;
    }


    if (
        appointment.time
    ) {

        return appointment.time;
    }


    if (
        appointment.scheduled_at
    ) {

        const date =
            new Date(
                appointment.scheduled_at
            );


        if (
            !Number.isNaN(
                date.getTime()
            )
        ) {

            return date.toLocaleTimeString(
                "en-IN",
                {
                    hour: "2-digit",
                    minute: "2-digit"
                }
            );
        }
    }


    return "-";
}


/* =========================================================
   COUNTS
   ========================================================= */

function countCaseStatus(status) {

    return reportCases.filter(
        clinicalCase =>
            String(
                clinicalCase.status || ""
            ).toLowerCase() ===
            status
    ).length;
}


function countOtherCaseStatuses() {

    return reportCases.filter(
        clinicalCase => {

            const status =
                String(
                    clinicalCase.status || ""
                ).toLowerCase();


            return (
                status !== "active" &&
                status !== "completed" &&
                status !== "closed"
            );
        }
    ).length;
}


function countAppointmentStatus(
    status
) {

    return reportAppointments.filter(
        appointment =>
            String(
                appointment.status || ""
            ).toLowerCase() ===
            status
    ).length;
}


/* =========================================================
   STATUS CLASSES
   ========================================================= */

function getCaseStatusClass(status) {

    const value =
        String(
            status || ""
        ).toLowerCase();


    if (value === "completed") {
        return "badge-success";
    }


    if (value === "closed") {
        return "badge-secondary";
    }


    if (value === "cancelled") {
        return "badge-danger";
    }


    return "badge-primary";
}


function getAppointmentStatusClass(
    status
) {

    const value =
        String(
            status || ""
        ).toLowerCase();


    if (
        value === "completed" ||
        value === "confirmed"
    ) {

        return "badge-success";
    }


    if (value === "cancelled") {
        return "badge-danger";
    }


    return "badge-primary";
}


/* =========================================================
   EVENTS
   ========================================================= */

function setupReportEvents() {

    document
        .getElementById(
            "refreshReportsButton"
        )
        .addEventListener(
            "click",
            () => window.location.reload()
        );


    document
        .getElementById(
            "viewAllPatientsButton"
        )
        .addEventListener(
            "click",
            () => {
                window.location.href =
                    "patients.html";
            }
        );


    document
        .getElementById(
            "viewClinicalRecordsButton"
        )
        .addEventListener(
            "click",
            () => {
                window.location.href =
                    "clinical-records.html";
            }
        );


    document
        .getElementById(
            "viewAppointmentsButton"
        )
        .addEventListener(
            "click",
            () => {
                window.location.href =
                    "appointments.html";
            }
        );
}


/* =========================================================
   UTILITIES
   ========================================================= */

function getDateValue(value) {

    if (!value) {
        return 0;
    }


    const timestamp =
        new Date(value).getTime();


    return Number.isNaN(timestamp)
        ? 0
        : timestamp;
}


function isPastDate(value) {

    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return false;
    }


    return date < new Date();
}


function renderReportEmpty(
    message
) {

    return `

        <div class="empty-state">

            <div class="empty-state-icon">
                ▤
            </div>

            <p>
                ${escapeHtml(message)}
            </p>

        </div>

    `;
}


/* =========================================================
   LOADING / ERROR
   ========================================================= */

function renderReportsLoading() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="loading">

            <div class="spinner"></div>

            <span>
                Loading reports...
            </span>

        </div>

    `;
}


function renderReportsError(
    message
) {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="content-card">

            <div class="alert alert-error">

                Unable to load reports.

                <br><br>

                ${escapeHtml(
                    message ||
                    "Unknown error"
                )}

            </div>


            <button
                type="button"
                class="primary-button"
                onclick="window.location.reload()"
            >
                Retry
            </button>

        </div>

    `;
}
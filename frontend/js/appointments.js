/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   Appointments
   ========================================================= */

let allAppointments = [];
let appointmentPatients = [];


document.addEventListener(
    "DOMContentLoaded",
    initializeAppointments
);


async function initializeAppointments() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        return;
    }

    renderAppointmentsLoading();

    try {

        const [
            appointments,
            patients
        ] = await Promise.all([
            getAppointments(),
            getPatients()
        ]);

        allAppointments =
            Array.isArray(appointments)
                ? appointments
                : [];

        appointmentPatients =
            Array.isArray(patients)
                ? patients
                : [];

        renderAppointmentsPage();

        setupAppointmentEvents();

    } catch (error) {

        console.error(
            "Appointments loading error:",
            error
        );

        renderAppointmentsError(
            error.message
        );
    }
}


/* =========================================================
   PAGE
   ========================================================= */

function renderAppointmentsPage() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );

    pageContent.innerHTML = `

        <div class="section-header">

            <div>

                <h2>
                    Appointment Management
                </h2>

                <p>
                    Schedule and manage patient appointments.
                </p>

            </div>
<br>
            <button
                type="button"
                class="primary-button"
                id="addAppointmentButton"
            >
                + New Appointment
            </button>

        </div>
<br>

        <div class="stats-grid">

            <div class="stat-card">

                <div class="stat-card-icon">
                    □
                </div>

                <div class="stat-card-content">

                    <span>
                        Total Appointments
                    </span>

                    <strong>
                        ${allAppointments.length}
                    </strong>

                    <small>
                        All records
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    ◷
                </div>

                <div class="stat-card-content">

                    <span>
                        Upcoming
                    </span>

                    <strong>
                        ${countUpcomingAppointments()}
                    </strong>

                    <small>
                        Future appointments
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    ✓
                </div>

                <div class="stat-card-content">

                    <span>
                        Completed
                    </span>

                    <strong>
                        ${countAppointmentsByStatus(
                            "completed"
                        )}
                    </strong>

                    <small>
                        Completed visits
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    !
                </div>

                <div class="stat-card-content">

                    <span>
                        Cancelled
                    </span>

                    <strong>
                        ${countAppointmentsByStatus(
                            "cancelled"
                        )}
                    </strong>

                    <small>
                        Cancelled appointments
                    </small>

                </div>

            </div>

        </div>


        <div class="content-card">

            <div class="search-toolbar">

                <div class="search-box">

                    <span>⌕</span>

                    <input
                        type="text"
                        id="appointmentSearch"
                        placeholder="Search by patient, date or purpose..."
                    >

                </div>


                <select
                    id="appointmentStatusFilter"
                    class="toolbar-select"
                >

                    <option value="">
                        All statuses
                    </option>

                    <option value="scheduled">
                        Scheduled
                    </option>

                    <option value="confirmed">
                        Confirmed
                    </option>

                    <option value="completed">
                        Completed
                    </option>

                    <option value="cancelled">
                        Cancelled
                    </option>

                </select>

            </div>


            <div
                class="table-wrapper"
                id="appointmentsTable"
            >
                ${renderAppointmentsTable(
                    allAppointments
                )}
            </div>

        </div>


        <div
            class="modal"
            id="appointmentModal"
            style="display:none"
        >

            <div class="modal-overlay"></div>

            <div class="modal-content">

                <div class="modal-header">

                    <div>

                        <h2>
                            New Appointment
                        </h2>

                        <p>
                            Schedule a patient appointment.
                        </p>

                    </div>

                    <button
                        type="button"
                        class="modal-close"
                        id="closeAppointmentModal"
                    >
                        ×
                    </button>

                </div>


                <form id="appointmentForm">

                    <div class="form-grid">

                        <div class="form-group">

                            <label for="appointmentPatient">
                                Patient
                            </label>

                            <select
                                id="appointmentPatient"
                                required
                            >

                                <option value="">
                                    Select patient
                                </option>

                                ${appointmentPatients
                                    .map(patient => `

                                        <option
                                            value="${patient.id}"
                                        >

                                            ${escapeHtml(
                                                patient.patient_id ||
                                                "-"
                                            )}
                                            -
                                            ${escapeHtml(
                                                patient.name ||
                                                patient.full_name ||
                                                "Patient"
                                            )}

                                        </option>

                                    `)
                                    .join("")}

                            </select>

                        </div>


                        <div class="form-group">

                            <label for="appointmentDate">
                                Appointment Date
                            </label>

                            <input
                                type="date"
                                id="appointmentDate"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="appointmentTime">
                                Appointment Time
                            </label>

                            <input
                                type="time"
                                id="appointmentTime"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="appointmentStatus">
                                Status
                            </label>

                            <select
                                id="appointmentStatus"
                            >

                                <option value="scheduled">
                                    Scheduled
                                </option>

                                <option value="confirmed">
                                    Confirmed
                                </option>

                                <option value="completed">
                                    Completed
                                </option>

                                <option value="cancelled">
                                    Cancelled
                                </option>

                            </select>

                        </div>


                        <div class="form-group form-grid-full">

                            <label for="appointmentPurpose">
                                Purpose
                            </label>

                            <input
                                type="text"
                                id="appointmentPurpose"
                                placeholder="e.g. Initial consultation, follow-up..."
                            >

                        </div>


                        <div class="form-group form-grid-full">

                            <label for="appointmentNotes">
                                Notes
                            </label>

                            <textarea
                                id="appointmentNotes"
                                rows="4"
                                placeholder="Additional appointment notes..."
                            ></textarea>

                        </div>

                    </div>


                    <div
                        id="appointmentFormError"
                        class="form-error"
                        style="display:none"
                    ></div>


                    <div class="modal-footer">

                        <button
                            type="button"
                            class="secondary-button"
                            id="cancelAppointmentButton"
                        >
                            Cancel
                        </button>


                        <button
                            type="submit"
                            class="primary-button"
                            id="saveAppointmentButton"
                        >
                            Save Appointment
                        </button>

                    </div>

                </form>

            </div>

        </div>

    `;
}


/* =========================================================
   TABLE
   ========================================================= */

function renderAppointmentsTable(
    appointments
) {

    if (!appointments.length) {

        return `

            <div class="empty-state">

                <div class="empty-state-icon">
                    □
                </div>

                <h3>
                    No appointments found
                </h3>

                <p>
                    Create an appointment to get started.
                </p>

            </div>

        `;
    }


    const sorted =
        [...appointments].sort(
            (a, b) =>
                getAppointmentDateValue(a) -
                getAppointmentDateValue(b)
        );


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

                ${sorted.map(
                    appointment => `

                        <tr>

                            <td>

                                <strong>
                                    ${escapeHtml(
                                        getAppointmentPatientName(
                                            appointment
                                        )
                                    )}
                                </strong>

                                <small>
                                    ${escapeHtml(
                                        getAppointmentPatientId(
                                            appointment
                                        )
                                    )}
                                </small>

                            </td>


                            <td>
                                ${formatDate(
                                    appointment.appointment_date ||
                                    appointment.date ||
                                    appointment.scheduled_date
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
                                    appointment.notes ||
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
   EVENTS
   ========================================================= */

function setupAppointmentEvents() {

    document
        .getElementById(
            "addAppointmentButton"
        )
        .addEventListener(
            "click",
            openAppointmentModal
        );


    document
        .getElementById(
            "closeAppointmentModal"
        )
        .addEventListener(
            "click",
            closeAppointmentModal
        );


    document
        .getElementById(
            "cancelAppointmentButton"
        )
        .addEventListener(
            "click",
            closeAppointmentModal
        );


    document
        .getElementById(
            "appointmentForm"
        )
        .addEventListener(
            "submit",
            saveAppointmentRecord
        );


    document
        .getElementById(
            "appointmentSearch"
        )
        .addEventListener(
            "input",
            applyAppointmentFilters
        );


    document
        .getElementById(
            "appointmentStatusFilter"
        )
        .addEventListener(
            "change",
            applyAppointmentFilters
        );


    document
        .querySelector(
            "#appointmentModal .modal-overlay"
        )
        .addEventListener(
            "click",
            closeAppointmentModal
        );
}


/* =========================================================
   FILTER
   ========================================================= */

function applyAppointmentFilters() {

    const search =
        document
            .getElementById(
                "appointmentSearch"
            )
            .value
            .trim()
            .toLowerCase();


    const status =
        document
            .getElementById(
                "appointmentStatusFilter"
            )
            .value
            .toLowerCase();


    const filtered =
        allAppointments.filter(
            appointment => {

                const searchable = [

                    getAppointmentPatientName(
                        appointment
                    ),

                    getAppointmentPatientId(
                        appointment
                    ),

                    appointment.purpose,

                    appointment.reason,

                    appointment.notes,

                    appointment.status,

                    appointment.appointment_date,

                    appointment.date

                ]
                    .join(" ")
                    .toLowerCase();


                const matchesSearch =
                    !search ||
                    searchable.includes(search);


                const matchesStatus =
                    !status ||
                    String(
                        appointment.status || ""
                    ).toLowerCase() ===
                    status;


                return (
                    matchesSearch &&
                    matchesStatus
                );
            }
        );


    document
        .getElementById(
            "appointmentsTable"
        )
        .innerHTML =
            renderAppointmentsTable(
                filtered
            );
}


/* =========================================================
   MODAL
   ========================================================= */

function openAppointmentModal() {

    const modal =
        document.getElementById(
            "appointmentModal"
        );


    document
        .getElementById(
            "appointmentForm"
        )
        .reset();


    clearAppointmentFormError();


    document
        .getElementById(
            "appointmentDate"
        )
        .value =
            getTodayDate();


    document
        .getElementById(
            "appointmentTime"
        )
        .value =
            "10:00";


    modal.style.display =
        "flex";
}


function closeAppointmentModal() {

    document
        .getElementById(
            "appointmentModal"
        )
        .style.display =
            "none";
}


/* =========================================================
   SAVE
   ========================================================= */

async function saveAppointmentRecord(
    event
) {

    event.preventDefault();


    const patientId =
        document
            .getElementById(
                "appointmentPatient"
            )
            .value;


    const date =
        document
            .getElementById(
                "appointmentDate"
            )
            .value;


    const time =
        document
            .getElementById(
                "appointmentTime"
            )
            .value;


    const status =
        document
            .getElementById(
                "appointmentStatus"
            )
            .value;


    const purpose =
        document
            .getElementById(
                "appointmentPurpose"
            )
            .value
            .trim();


    const notes =
        document
            .getElementById(
                "appointmentNotes"
            )
            .value
            .trim();


    if (!patientId) {

        showAppointmentFormError(
            "Please select a patient."
        );

        return;
    }


    if (!date) {

        showAppointmentFormError(
            "Please select an appointment date."
        );

        return;
    }


    if (!time) {

        showAppointmentFormError(
            "Please select an appointment time."
        );

        return;
    }


    const button =
        document.getElementById(
            "saveAppointmentButton"
        );


    button.disabled =
        true;

    button.textContent =
        "Saving...";


    clearAppointmentFormError();


    try {

        const appointmentDateTime =
            `${date}T${time}:00`;


        const data = {

            patient_id:
                Number(patientId),

            appointment_date:
                date,

            appointment_time:
                time,

            scheduled_at:
                appointmentDateTime,

            status:
                status,

            purpose:
                purpose || null,

            notes:
                notes || null

        };


        await createAppointment(
            data
        );


        showToast(
            "Appointment created successfully.",
            "success"
        );


        closeAppointmentModal();


        allAppointments =
            await getAppointments();


        if (!Array.isArray(
            allAppointments
        )) {

            allAppointments = [];
        }


        renderAppointmentsTableInPage();


    } catch (error) {

        console.error(
            "Appointment save error:",
            error
        );


        showAppointmentFormError(
            error.message ||
            "Unable to save appointment."
        );

    } finally {

        button.disabled =
            false;

        button.textContent =
            "Save Appointment";
    }
}


/* =========================================================
   RE-RENDER
   ========================================================= */

function renderAppointmentsTableInPage() {

    const searchElement =
        document.getElementById(
            "appointmentSearch"
        );


    const statusElement =
        document.getElementById(
            "appointmentStatusFilter"
        );


    if (!searchElement ||
        !statusElement) {

        return;
    }


    searchElement.value =
        "";

    statusElement.value =
        "";


    document
        .getElementById(
            "appointmentsTable"
        )
        .innerHTML =
            renderAppointmentsTable(
                allAppointments
            );


    updateAppointmentStats();
}


/* =========================================================
   STATS
   ========================================================= */

function updateAppointmentStats() {

    const values =
        document.querySelectorAll(
            ".stats-grid .stat-card strong"
        );


    if (values.length < 4) {
        return;
    }


    values[0].textContent =
        allAppointments.length;


    values[1].textContent =
        countUpcomingAppointments();


    values[2].textContent =
        countAppointmentsByStatus(
            "completed"
        );


    values[3].textContent =
        countAppointmentsByStatus(
            "cancelled"
        );
}


function countUpcomingAppointments() {

    return allAppointments.filter(
        appointment => {

            const value =
                appointment.appointment_date ||
                appointment.date ||
                appointment.scheduled_at;


            if (!value) {
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


            return !isPastAppointment(
                value
            );
        }
    ).length;
}


function countAppointmentsByStatus(
    status
) {

    return allAppointments.filter(
        appointment =>
            String(
                appointment.status || ""
            ).toLowerCase() ===
            status.toLowerCase()
    ).length;
}


/* =========================================================
   PATIENT
   ========================================================= */

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
            appointmentPatients.find(
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


function getAppointmentPatientId(
    appointment
) {

    if (
        appointment.patient_display_id
    ) {

        return appointment.patient_display_id;
    }


    if (
        appointment.patient_id
    ) {

        const patient =
            appointmentPatients.find(
                item =>
                    Number(item.id) ===
                    Number(
                        appointment.patient_id
                    )
            );


        if (patient) {

            return (
                patient.patient_id ||
                `ID ${patient.id}`
            );
        }


        return `ID ${appointment.patient_id}`;
    }


    return "-";
}


/* =========================================================
   DATE / TIME
   ========================================================= */

function getAppointmentDateValue(
    appointment
) {

    const value =
        appointment.scheduled_at ||
        appointment.appointment_date ||
        appointment.date ||
        appointment.created_at;


    if (!value) {

        return Number.MAX_SAFE_INTEGER;
    }


    const timestamp =
        new Date(value).getTime();


    return Number.isNaN(timestamp)
        ? Number.MAX_SAFE_INTEGER
        : timestamp;
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


function isPastAppointment(
    value
) {

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


function getTodayDate() {

    const now =
        new Date();


    return `${now.getFullYear()}-${
        String(
            now.getMonth() + 1
        ).padStart(2, "0")
    }-${
        String(
            now.getDate()
        ).padStart(2, "0")
    }`;
}


/* =========================================================
   STATUS
   ========================================================= */

function getAppointmentStatusClass(
    status
) {

    const value =
        String(
            status || ""
        ).toLowerCase();


    if (value === "completed") {
        return "badge-success";
    }


    if (value === "cancelled") {
        return "badge-danger";
    }


    if (value === "confirmed") {
        return "badge-success";
    }


    return "badge-primary";
}


/* =========================================================
   FORM ERROR
   ========================================================= */

function clearAppointmentFormError() {

    const error =
        document.getElementById(
            "appointmentFormError"
        );


    if (!error) {
        return;
    }


    error.style.display =
        "none";

    error.textContent =
        "";
}


function showAppointmentFormError(
    message
) {

    const error =
        document.getElementById(
            "appointmentFormError"
        );


    if (!error) {
        return;
    }


    error.textContent =
        message;

    error.style.display =
        "block";
}


/* =========================================================
   LOADING / ERROR
   ========================================================= */

function renderAppointmentsLoading() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="loading">

            <div class="spinner"></div>

            <span>
                Loading appointments...
            </span>

        </div>

    `;
}


function renderAppointmentsError(
    message
) {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="content-card">

            <div class="alert alert-error">

                Unable to load appointments.

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
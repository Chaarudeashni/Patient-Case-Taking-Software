/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   Follow-ups
   ========================================================= */

let allFollowups = [];
let followupPatients = [];


document.addEventListener(
    "DOMContentLoaded",
    initializeFollowups
);


async function initializeFollowups() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        return;
    }


    renderFollowupsLoading();


    try {

        const [
            followups,
            patients
        ] = await Promise.all([
            getFollowups(),
            getPatients()
        ]);


        allFollowups =
            Array.isArray(followups)
                ? followups
                : [];


        followupPatients =
            Array.isArray(patients)
                ? patients
                : [];


        renderFollowupsPage();

        setupFollowupEvents();

    } catch (error) {

        console.error(
            "Follow-ups loading error:",
            error
        );

        renderFollowupsError(
            error.message
        );
    }
}


/* =========================================================
   PAGE
   ========================================================= */

function renderFollowupsPage() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="section-header">

            <div>

                <h2>
                    Follow-up Management
                </h2>

                <p>
                    Schedule and monitor patient
                    follow-up records.
                </p>

            </div>

            <br>
            <button
                type="button"
                class="primary-button"
                id="addFollowupButton"
            >
                + Add Follow-up
            </button>
           
        </div>

 <br>
        <!-- Summary -->

        <div class="stats-grid">

            <div class="stat-card">

                <div class="stat-card-icon">
                    ↻
                </div>

                <div class="stat-card-content">

                    <span>
                        Total Follow-ups
                    </span>

                    <strong>
                        ${allFollowups.length}
                    </strong>

                    <small>
                        All records
                    </small>

                </div>

            </div>


            <div class="stat-card">

                <div class="stat-card-icon">
                    □
                </div>

                <div class="stat-card-content">

                    <span>
                        Upcoming
                    </span>

                    <strong>
                        ${countUpcomingFollowups()}
                    </strong>

                    <small>
                        Future follow-ups
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
                        ${countFollowupsByStatus(
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
                        Pending
                    </span>

                    <strong>
                        ${countPendingFollowups()}
                    </strong>

                    <small>
                        Awaiting follow-up
                    </small>

                </div>

            </div>

        </div>


        <!-- Filter -->

        <div class="content-card">

            <div class="search-toolbar">

                <div class="search-box">

                    <span>⌕</span>

                    <input
                        type="text"
                        id="followupSearch"
                        placeholder="Search by patient, reason or status..."
                    >

                </div>


                <select
                    id="followupStatusFilter"
                    class="toolbar-select"
                >

                    <option value="">
                        All statuses
                    </option>

                    <option value="scheduled">
                        Scheduled
                    </option>

                    <option value="pending">
                        Pending
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
                id="followupsTable"
            >
                ${renderFollowupsTable(
                    allFollowups
                )}
            </div>

        </div>


        <!-- Add Follow-up Modal -->

        <div
            class="modal"
            id="followupModal"
            style="display:none"
        >

            <div class="modal-overlay"></div>

            <div class="modal-content">

                <div class="modal-header">

                    <div>

                        <h2>
                            Add Follow-up
                        </h2>

                        <p>
                            Schedule a patient follow-up.
                        </p>

                    </div>


                    <button
                        type="button"
                        class="modal-close"
                        id="closeFollowupModal"
                    >
                        ×
                    </button>

                </div>


                <form id="followupForm">

                    <div class="form-grid">

                        <div class="form-group">

                            <label for="followupPatient">
                                Patient
                            </label>

                            <select
                                id="followupPatient"
                                required
                            >

                                <option value="">
                                    Select patient
                                </option>

                                ${followupPatients
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

                            <label for="followupDate">
                                Follow-up Date
                            </label>

                            <input
                                type="date"
                                id="followupDate"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label for="followupStatus">
                                Status
                            </label>

                            <select
                                id="followupStatus"
                            >

                                <option value="scheduled">
                                    Scheduled
                                </option>

                                <option value="pending">
                                    Pending
                                </option>

                                <option value="completed">
                                    Completed
                                </option>

                                <option value="cancelled">
                                    Cancelled
                                </option>

                            </select>

                        </div>


                        <div class="form-group">

                            <label for="followupType">
                                Follow-up Type
                            </label>

                            <select
                                id="followupType"
                            >

                                <option value="">
                                    Select type
                                </option>

                                <option value="Clinical Review">
                                    Clinical Review
                                </option>

                                <option value="Treatment Review">
                                    Treatment Review
                                </option>

                                <option value="Progress Review">
                                    Progress Review
                                </option>

                                <option value="Investigation Review">
                                    Investigation Review
                                </option>

                                <option value="Other">
                                    Other
                                </option>

                            </select>

                        </div>


                        <div class="form-group form-grid-full">

                            <label for="followupReason">
                                Reason / Notes
                            </label>

                            <textarea
                                id="followupReason"
                                rows="4"
                                placeholder="Enter reason or clinical notes..."
                            ></textarea>

                        </div>

                    </div>


                    <div
                        id="followupFormError"
                        class="form-error"
                        style="display:none"
                    ></div>


                    <div class="modal-footer">

                        <button
                            type="button"
                            class="secondary-button"
                            id="cancelFollowupButton"
                        >
                            Cancel
                        </button>


                        <button
                            type="submit"
                            class="primary-button"
                            id="saveFollowupButton"
                        >
                            Save Follow-up
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

function renderFollowupsTable(followups) {

    if (!followups.length) {

        return `

            <div class="empty-state">

                <div class="empty-state-icon">
                    ↻
                </div>

                <h3>
                    No follow-ups found
                </h3>

                <p>
                    Add a follow-up record to
                    get started.
                </p>

            </div>

        `;
    }


    const sorted =
        [...followups].sort(
            (a, b) =>
                getFollowupDateValue(a) -
                getFollowupDateValue(b)
        );


    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Patient
                    </th>

                    <th>
                        Follow-up Date
                    </th>

                    <th>
                        Type
                    </th>

                    <th>
                        Reason / Notes
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                ${sorted.map(
                    followup => `

                        <tr>

                            <td>

                                <strong>
                                    ${escapeHtml(
                                        getFollowupPatientName(
                                            followup
                                        )
                                    )}
                                </strong>

                                <small>
                                    ${escapeHtml(
                                        getFollowupPatientId(
                                            followup
                                        )
                                    )}
                                </small>

                            </td>


                            <td>

                                ${formatDate(
                                    followup.followup_date ||
                                    followup.date ||
                                    followup.scheduled_at
                                )}

                            </td>


                            <td>

                                ${escapeHtml(
                                    followup.type ||
                                    followup.followup_type ||
                                    "-"
                                )}

                            </td>


                            <td>

                                ${escapeHtml(
                                    followup.reason ||
                                    followup.notes ||
                                    "-"
                                )}

                            </td>


                            <td>

                                <span class="
                                    badge
                                    ${getStatusBadgeClass(
                                        followup.status
                                    )}
                                ">

                                    ${escapeHtml(
                                        followup.status ||
                                        "Pending"
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

function setupFollowupEvents() {

    document
        .getElementById(
            "addFollowupButton"
        )
        .addEventListener(
            "click",
            openFollowupModal
        );


    document
        .getElementById(
            "closeFollowupModal"
        )
        .addEventListener(
            "click",
            closeFollowupModal
        );


    document
        .getElementById(
            "cancelFollowupButton"
        )
        .addEventListener(
            "click",
            closeFollowupModal
        );


    document
        .getElementById(
            "followupForm"
        )
        .addEventListener(
            "submit",
            saveFollowupRecord
        );


    document
        .getElementById(
            "followupSearch"
        )
        .addEventListener(
            "input",
            applyFollowupFilters
        );


    document
        .getElementById(
            "followupStatusFilter"
        )
        .addEventListener(
            "change",
            applyFollowupFilters
        );


    document
        .querySelector(
            "#followupModal .modal-overlay"
        )
        .addEventListener(
            "click",
            closeFollowupModal
        );
}


/* =========================================================
   FILTER
   ========================================================= */

function applyFollowupFilters() {

    const search =
        document
            .getElementById(
                "followupSearch"
            )
            .value
            .trim()
            .toLowerCase();


    const status =
        document
            .getElementById(
                "followupStatusFilter"
            )
            .value
            .toLowerCase();


    const filtered =
        allFollowups.filter(
            followup => {

                const searchable = [

                    getFollowupPatientName(
                        followup
                    ),

                    getFollowupPatientId(
                        followup
                    ),

                    followup.reason,

                    followup.notes,

                    followup.type,

                    followup.followup_type,

                    followup.status

                ]
                    .join(" ")
                    .toLowerCase();


                const matchesSearch =
                    !search ||
                    searchable.includes(search);


                const matchesStatus =
                    !status ||
                    String(
                        followup.status || ""
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
            "followupsTable"
        )
        .innerHTML =
            renderFollowupsTable(
                filtered
            );
}


/* =========================================================
   MODAL
   ========================================================= */

function openFollowupModal() {

    const modal =
        document.getElementById(
            "followupModal"
        );


    document
        .getElementById(
            "followupForm"
        )
        .reset();


    clearFollowupFormError();


    document
        .getElementById(
            "followupDate"
        )
        .value =
            getTodayDate();


    modal.style.display =
        "flex";
}


function closeFollowupModal() {

    document
        .getElementById(
            "followupModal"
        )
        .style.display =
            "none";
}


/* =========================================================
   SAVE
   ========================================================= */

async function saveFollowupRecord(event) {

    event.preventDefault();


    const patientId =
        document
            .getElementById(
                "followupPatient"
            )
            .value;


    const followupDate =
        document
            .getElementById(
                "followupDate"
            )
            .value;


    const status =
        document
            .getElementById(
                "followupStatus"
            )
            .value;


    const type =
        document
            .getElementById(
                "followupType"
            )
            .value;


    const reason =
        document
            .getElementById(
                "followupReason"
            )
            .value
            .trim();


    if (!patientId) {

        showFollowupFormError(
            "Please select a patient."
        );

        return;
    }


    if (!followupDate) {

        showFollowupFormError(
            "Please select a follow-up date."
        );

        return;
    }


    const button =
        document.getElementById(
            "saveFollowupButton"
        );


    button.disabled =
        true;

    button.textContent =
        "Saving...";


    clearFollowupFormError();


    try {

        const data = {

            patient_id:
                Number(patientId),

            followup_date:
                followupDate,

            status:
                status,

            type:
                type || null,

            reason:
                reason || null

        };


        await createFollowup(
            data
        );


        showToast(
            "Follow-up created successfully.",
            "success"
        );


        closeFollowupModal();


        allFollowups =
            await getFollowups();


        if (!Array.isArray(allFollowups)) {
            allFollowups = [];
        }


        renderFollowupsTableInPage();


    } catch (error) {

        console.error(
            "Follow-up save error:",
            error
        );


        showFollowupFormError(
            error.message ||
            "Unable to save follow-up."
        );

    } finally {

        button.disabled =
            false;

        button.textContent =
            "Save Follow-up";
    }
}


/* =========================================================
   RE-RENDER TABLE
   ========================================================= */

function renderFollowupsTableInPage() {

    const searchElement =
        document.getElementById(
            "followupSearch"
        );


    const statusElement =
        document.getElementById(
            "followupStatusFilter"
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
            "followupsTable"
        )
        .innerHTML =
            renderFollowupsTable(
                allFollowups
            );


    updateFollowupStats();
}


/* =========================================================
   STATS
   ========================================================= */

function updateFollowupStats() {

    const statValues =
        document.querySelectorAll(
            ".stats-grid .stat-card strong"
        );


    if (statValues.length < 4) {
        return;
    }


    statValues[0].textContent =
        allFollowups.length;


    statValues[1].textContent =
        countUpcomingFollowups();


    statValues[2].textContent =
        countFollowupsByStatus(
            "completed"
        );


    statValues[3].textContent =
        countPendingFollowups();
}


function countUpcomingFollowups() {

    return allFollowups.filter(
        followup => {

            const date =
                followup.followup_date ||
                followup.date ||
                followup.scheduled_at;


            return (
                date &&
                !isPastDateValue(date) &&
                String(
                    followup.status || ""
                ).toLowerCase() !==
                "completed" &&
                String(
                    followup.status || ""
                ).toLowerCase() !==
                "cancelled"
            );
        }
    ).length;
}


function countPendingFollowups() {

    return allFollowups.filter(
        followup => {

            const status =
                String(
                    followup.status || ""
                ).toLowerCase();


            return (
                status === "pending" ||
                status === "scheduled" ||
                status === ""
            );
        }
    ).length;
}


function countFollowupsByStatus(status) {

    return allFollowups.filter(
        followup =>
            String(
                followup.status || ""
            ).toLowerCase() ===
            status.toLowerCase()
    ).length;
}


/* =========================================================
   PATIENT INFORMATION
   ========================================================= */

function getFollowupPatientName(
    followup
) {

    if (
        followup.patient_name
    ) {

        return followup.patient_name;
    }


    if (
        followup.patient
    ) {

        if (
            typeof followup.patient ===
            "object"
        ) {

            return (
                followup.patient.name ||
                followup.patient.full_name ||
                "Patient"
            );
        }

        return followup.patient;
    }


    if (
        followup.patient_id
    ) {

        const patient =
            followupPatients.find(
                item =>
                    Number(item.id) ===
                    Number(
                        followup.patient_id
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


function getFollowupPatientId(
    followup
) {

    if (
        followup.patient_display_id
    ) {

        return followup.patient_display_id;
    }


    if (
        followup.patient_id
    ) {

        const patient =
            followupPatients.find(
                item =>
                    Number(item.id) ===
                    Number(
                        followup.patient_id
                    )
            );


        if (patient) {

            return (
                patient.patient_id ||
                `ID ${patient.id}`
            );
        }


        return `ID ${followup.patient_id}`;
    }


    return "-";
}


/* =========================================================
   STATUS
   ========================================================= */

function getStatusBadgeClass(
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


    if (value === "pending") {
        return "badge-warning";
    }


    return "badge-primary";
}


/* =========================================================
   DATE
   ========================================================= */

function getFollowupDateValue(
    followup
) {

    const value =
        followup.followup_date ||
        followup.date ||
        followup.scheduled_at ||
        followup.created_at;


    if (!value) {
        return Number.MAX_SAFE_INTEGER;
    }


    const timestamp =
        new Date(value).getTime();


    return Number.isNaN(timestamp)
        ? Number.MAX_SAFE_INTEGER
        : timestamp;
}


function isPastDateValue(value) {

    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return false;
    }


    const today =
        new Date();

    today.setHours(
        0,
        0,
        0,
        0
    );


    date.setHours(
        0,
        0,
        0,
        0
    );


    return date < today;
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
   FORM ERRORS
   ========================================================= */

function clearFollowupFormError() {

    const error =
        document.getElementById(
            "followupFormError"
        );


    if (!error) {
        return;
    }


    error.style.display =
        "none";

    error.textContent =
        "";
}


function showFollowupFormError(
    message
) {

    const error =
        document.getElementById(
            "followupFormError"
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

function renderFollowupsLoading() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="loading">

            <div class="spinner"></div>

            <span>
                Loading follow-ups...
            </span>

        </div>

    `;
}


function renderFollowupsError(message) {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    pageContent.innerHTML = `

        <div class="content-card">

            <div class="alert alert-error">

                Unable to load follow-ups.

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
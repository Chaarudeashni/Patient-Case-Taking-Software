let allPatients = [];
let filteredPatients = [];
let editingPatientId = null;

document.addEventListener("DOMContentLoaded", initializePatientsPage);


/* =========================================================
   INITIALIZE
   ========================================================= */

async function initializePatientsPage() {
    buildPatientsPage();
    setupPatientPageEvents();
    await loadPatients();
}


/* =========================================================
   BUILD PAGE
   ========================================================= */

function buildPatientsPage() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        console.error("pageContent was not found.");
        return;
    }

    pageContent.innerHTML = `
        <div class="page-header">

            <div>
                <h2>Patients</h2>
                <p>Manage patient information and records.</p>
            </div>
            <br>
            <button
                type="button"
                class="btn btn-primary"
                id="addPatientButton"
            >
                + Add Patient
                
            </button>
             <br><br>
        </div>


        <div class="card">

            <div class="card-header">

                <div>
                    <h3>Patient List</h3>
                    <span id="patientCount">0 patients</span>
                </div>

                <div class="search-box">

                    <input
                        type="text"
                        id="patientSearch"
                        placeholder="Search patients..."
                    >

                </div>

            </div>


            <div id="patientTableContainer">

                <div class="loading">

                    <div class="spinner"></div>

                    <span>
                        Loading patients...
                    </span>

                </div>

            </div>

        </div>


        <!-- PATIENT MODAL -->

        <div
            class="modal"
            id="patientModal"
            style="display:none;"
        >

            <div class="modal-content">

                <div class="modal-header">

                    <h2 id="patientModalTitle">
                        Add Patient
                    </h2>

                    <button
                        type="button"
                        class="modal-close"
                        data-close-patient-modal
                    >
                        ×
                    </button>

                </div>


                <form id="patientForm">

                    <div class="form-grid">


                        <!-- PATIENT ID -->

                        <div class="form-group">

                            <label for="patientId">
                                Patient ID
                            </label>

                            <input
                                type="text"
                                id="patientId"
                                placeholder="Example: P007"
                                required
                            >

                        </div>


                        <!-- NAME -->

                        <div class="form-group">

                            <label for="patientName">
                                Full Name
                            </label>

                            <input
                                type="text"
                                id="patientName"
                                required
                            >

                        </div>


                        <!-- DOB -->

                        <div class="form-group">

                            <label for="patientDob">
                                Date of Birth
                            </label>

                            <input
                                type="date"
                                id="patientDob"
                            >

                        </div>


                        <!-- GENDER -->

                        <div class="form-group">

                            <label for="patientGender">
                                Gender
                            </label>

                            <select id="patientGender">

                                <option value="">
                                    Select gender
                                </option>

                                <option value="Male">
                                    Male
                                </option>

                                <option value="Female">
                                    Female
                                </option>

                                <option value="Other">
                                    Other
                                </option>

                            </select>

                        </div>


                        <!-- PHONE -->

                        <div class="form-group">

                            <label for="patientPhone">
                                Phone
                            </label>

                            <input
                                type="tel"
                                id="patientPhone"
                            >

                        </div>


                        <!-- EMAIL -->

                        <div class="form-group">

                            <label for="patientEmail">
                                Email
                            </label>

                            <input
                                type="email"
                                id="patientEmail"
                            >

                        </div>


                        <!-- ADDRESS -->

                        <div class="form-group full-width">

                            <label for="patientAddress">
                                Address
                            </label>

                            <textarea
                                id="patientAddress"
                                rows="3"
                            ></textarea>

                        </div>

                    </div>


                    <div class="modal-actions">

                        <button
                            type="button"
                            class="btn"
                            data-close-patient-modal
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            class="btn btn-primary"
                        >
                            Save Patient
                        </button>

                    </div>

                </form>

            </div>

        </div>
    `;
}


/* =========================================================
   EVENTS
   ========================================================= */

function setupPatientPageEvents() {

    const addButton =
        document.getElementById(
            "addPatientButton"
        );

    if (addButton) {

        addButton.addEventListener(
            "click",
            openAddPatientModal
        );

    }


    const searchInput =
        document.getElementById(
            "patientSearch"
        );

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            function () {

                filterPatients(
                    this.value
                );

            }
        );

    }


    const form =
        document.getElementById(
            "patientForm"
        );

    if (form) {

        form.addEventListener(
            "submit",
            handlePatientFormSubmit
        );

    }


    document.addEventListener(
        "click",
        handlePatientPageClick
    );
}


/* =========================================================
   LOAD PATIENTS
   ========================================================= */

async function loadPatients() {

    const container =
        document.getElementById(
            "patientTableContainer"
        );


    if (container) {

        container.innerHTML = `
            <div class="loading">

                <div class="spinner"></div>

                <span>
                    Loading patients...
                </span>

            </div>
        `;

    }


    try {

        allPatients =
            await getPatients();


        if (!Array.isArray(allPatients)) {

            allPatients = [];

        }


        filteredPatients =
            [...allPatients];


        renderPatients();


    } catch (error) {

        console.error(
            "Patient loading error:",
            error
        );


        if (container) {

            container.innerHTML = `
                <div class="alert alert-danger">

                    Failed to load patients.

                    <br>

                    ${escapeHtml(
                        error.message ||
                        "Unknown error"
                    )}

                </div>
            `;

        }

    }
}


/* =========================================================
   SEARCH
   ========================================================= */

function filterPatients(searchText) {

    const search =
        String(searchText || "")
            .trim()
            .toLowerCase();


    if (!search) {

        filteredPatients =
            [...allPatients];

    } else {

        filteredPatients =
            allPatients.filter(
                patient => {

                    const name =
                        getPatientFullName(
                            patient
                        ).toLowerCase();


                    const patientId =
                        getPatientDisplayId(
                            patient
                        ).toLowerCase();


                    const phone =
                        String(
                            patient.phone || ""
                        ).toLowerCase();


                    const email =
                        String(
                            patient.email || ""
                        ).toLowerCase();


                    return (
                        name.includes(search) ||
                        patientId.includes(search) ||
                        phone.includes(search) ||
                        email.includes(search)
                    );
                }
            );

    }


    renderPatients();
}


/* =========================================================
   RENDER
   ========================================================= */

function renderPatients() {

    const container =
        document.getElementById(
            "patientTableContainer"
        );


    const countElement =
        document.getElementById(
            "patientCount"
        );


    if (!container) {

        console.error(
            "patientTableContainer was not found."
        );

        return;
    }


    if (countElement) {

        countElement.textContent =
            `${filteredPatients.length} patient${
                filteredPatients.length === 1
                    ? ""
                    : "s"
            }`;

    }


    if (filteredPatients.length === 0) {

        container.innerHTML = `

            <div class="empty-state">

                <h3>
                    No patients found
                </h3>

                <p>
                    Add a new patient or change your search.
                </p>

            </div>

        `;

        return;
    }


    let html = `

        <div class="table-responsive">

            <table class="data-table">

                <thead>

                    <tr>

                        <th>Patient ID</th>

                        <th>Name</th>

                        <th>Date of Birth</th>

                        <th>Gender</th>

                        <th>Phone</th>

                        <th>Email</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

    `;


    filteredPatients.forEach(
        patient => {

            const dbId =
                getPatientDbId(
                    patient
                );


            const displayId =
                getPatientDisplayId(
                    patient
                );


            const fullName =
                getPatientFullName(
                    patient
                );


            html += `

                <tr>

                    <td>
                        <strong>
                            ${escapeHtml(
                                displayId
                            )}
                        </strong>
                    </td>


                    <td>
                        ${escapeHtml(
                            fullName
                        )}
                    </td>


                    <td>
                        ${formatDate(
                            patient.date_of_birth
                        )}
                    </td>


                    <td>
                        ${displayValue(
                            patient.gender
                        )}
                    </td>


                    <td>
                        ${displayValue(
                            patient.phone
                        )}
                    </td>


                    <td>
                        ${displayValue(
                            patient.email
                        )}
                    </td>


                    <td>

                        <div class="table-actions">

                            <button
                                type="button"
                                class="btn btn-sm"
                                data-view-patient="${dbId}"
                            >
                                View
                            </button>


                            <button
                                type="button"
                                class="btn btn-sm btn-primary"
                                data-edit-patient="${dbId}"
                            >
                                Edit
                            </button>


                            <button
                                type="button"
                                class="btn btn-sm btn-danger"
                                data-delete-patient="${dbId}"
                            >
                                Delete
                            </button>

                        </div>

                    </td>

                </tr>

            `;

        }
    );


    html += `

                </tbody>

            </table>

        </div>

    `;


    container.innerHTML =
        html;
}


/* =========================================================
   HELPERS
   ========================================================= */

function getPatientDbId(patient) {

    return patient && patient.id
        ? patient.id
        : null;
}


function getPatientDisplayId(patient) {

    if (!patient) {
        return "";
    }


    return (
        patient.patient_id ||
        patient.patientId ||
        ""
    );
}


function getPatientFullName(patient) {

    if (!patient) {
        return "";
    }


    if (
        patient.first_name ||
        patient.last_name
    ) {

        return [
            patient.first_name || "",
            patient.last_name || ""
        ]
            .join(" ")
            .trim();

    }


    return (
        patient.name ||
        patient.full_name ||
        patient.fullName ||
        ""
    );
}


/* =========================================================
   BUTTON CLICKS
   ========================================================= */

function handlePatientPageClick(event) {

    const editButton =
        event.target.closest(
            "[data-edit-patient]"
        );


    if (editButton) {

        editPatient(
            Number(
                editButton.dataset.editPatient
            )
        );

        return;
    }


    const viewButton =
        event.target.closest(
            "[data-view-patient]"
        );


    if (viewButton) {

        viewPatient(
            Number(
                viewButton.dataset.viewPatient
            )
        );

        return;
    }


    const deleteButton =
        event.target.closest(
            "[data-delete-patient]"
        );


    if (deleteButton) {

        deletePatientById(
            Number(
                deleteButton.dataset.deletePatient
            )
        );

        return;
    }


    const closeButton =
        event.target.closest(
            "[data-close-patient-modal]"
        );


    if (closeButton) {

        closePatientModal();

    }
}


/* =========================================================
   ADD PATIENT
   ========================================================= */

function openAddPatientModal() {

    editingPatientId = null;


    const modal =
        document.getElementById(
            "patientModal"
        );


    const title =
        document.getElementById(
            "patientModalTitle"
        );


    const form =
        document.getElementById(
            "patientForm"
        );


    if (title) {

        title.textContent =
            "Add Patient";

    }


    if (form) {

        form.reset();

    }


    const patientId =
        document.getElementById(
            "patientId"
        );


    if (patientId) {

        patientId.value =
            generateNextPatientId();

    }


    if (modal) {

        modal.style.display =
            "flex";

    }
}


/* =========================================================
   EDIT PATIENT
   ========================================================= */

function editPatient(dbId) {

    const patient =
        allPatients.find(
            p =>
                Number(p.id) ===
                Number(dbId)
        );


    if (!patient) {

        showToast(
            "Patient not found.",
            "error"
        );

        console.error(
            "Patient not found:",
            dbId
        );

        return;
    }


    editingPatientId =
        patient.id;


    const modal =
        document.getElementById(
            "patientModal"
        );


    const title =
        document.getElementById(
            "patientModalTitle"
        );


    if (title) {

        title.textContent =
            "Edit Patient";

    }


    setInputValue(
        "patientId",
        getPatientDisplayId(
            patient
        )
    );


    setInputValue(
        "patientName",
        getPatientFullName(
            patient
        )
    );


    setInputValue(
        "patientDob",
        patient.date_of_birth
    );


    setInputValue(
        "patientGender",
        patient.gender
    );


    setInputValue(
        "patientPhone",
        patient.phone
    );


    setInputValue(
        "patientEmail",
        patient.email
    );


    setInputValue(
        "patientAddress",
        patient.address
    );


    if (modal) {

        modal.style.display =
            "flex";

    }
}


/* =========================================================
   SAVE PATIENT
   ========================================================= */

async function handlePatientFormSubmit(event) {

    event.preventDefault();


    const name =
        getInputValue(
            "patientName"
        ).trim();


    if (!name) {

        showToast(
            "Please enter the patient's name.",
            "error"
        );

        return;
    }


    const nameParts =
        name.split(/\s+/);


    const firstName =
        nameParts.shift() || "";


    const lastName =
        nameParts.join(" ");


    const data = {

        patient_id:
            getInputValue(
                "patientId"
            ).trim(),

        first_name:
            firstName,

        last_name:
            lastName,

        date_of_birth:
            getInputValue(
                "patientDob"
            ) || null,

        gender:
            getInputValue(
                "patientGender"
            ) || null,

        phone:
            getInputValue(
                "patientPhone"
            ).trim() || null,

        email:
            getInputValue(
                "patientEmail"
            ).trim() || null,

        address:
            getInputValue(
                "patientAddress"
            ).trim() || null

    };


    try {

        /* EDIT */

        if (
            editingPatientId !== null
        ) {

            const patientToUpdate =
                allPatients.find(
                    p =>
                        Number(p.id) ===
                        Number(
                            editingPatientId
                        )
                );


            if (!patientToUpdate) {

                throw new Error(
                    "Patient not found."
                );

            }


            const displayPatientId =
                getPatientDisplayId(
                    patientToUpdate
                );


            if (!displayPatientId) {

                throw new Error(
                    "Patient ID is missing."
                );

            }


            /*
             * IMPORTANT:
             * Backend expects P006,
             * not numeric database ID 5.
             */

            await updatePatient(
                displayPatientId,
                data
            );


            showToast(
                "Patient updated successfully.",
                "success"
            );

        }


        /* CREATE */

        else {

            await createPatient(
                data
            );


            showToast(
                "Patient created successfully.",
                "success"
            );

        }


        closePatientModal();

        await loadPatients();


    } catch (error) {

        console.error(
            "Patient save error:",
            error
        );


        showToast(
            error.message ||
            "Failed to save patient.",
            "error"
        );
    }
}


function viewPatient(dbId) {

    const patient =
        allPatients.find(
            p =>
                Number(p.id) ===
                Number(dbId)
        );

    if (!patient) {

        showToast(
            "Patient not found.",
            "error"
        );

        return;
    }

    const fullName =
        getPatientFullName(patient);

    const displayId =
        getPatientDisplayId(patient);


    const existingModal =
        document.getElementById(
            "viewPatientModal"
        );


    if (existingModal) {
        existingModal.remove();
    }


    const modal =
        document.createElement("div");

    modal.id =
        "viewPatientModal";

    modal.className =
        "modal";

    modal.style.display =
        "flex";


    modal.innerHTML = `

        <div class="modal-content">

            <div class="modal-header">

                <div>
                    <h2>Patient Details</h2>

                    <p style="margin:4px 0 0;color:#6b7280;">
                        ${escapeHtml(displayId)}
                    </p>
                </div>

                <button
                    type="button"
                    class="modal-close"
                    id="closeViewPatientModal"
                >
                    ×
                </button>

            </div>


            <div style="padding:24px;">

                <div class="patient-details-grid">


                    <div class="detail-item">

                        <span class="detail-label">
                            Patient ID
                        </span>

                        <strong>
                            ${escapeHtml(displayId)}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span class="detail-label">
                            Full Name
                        </span>

                        <strong>
                            ${escapeHtml(fullName || "-")}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span class="detail-label">
                            Date of Birth
                        </span>

                        <strong>
                            ${formatDate(patient.date_of_birth)}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span class="detail-label">
                            Gender
                        </span>

                        <strong>
                            ${displayValue(patient.gender)}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span class="detail-label">
                            Phone
                        </span>

                        <strong>
                            ${displayValue(patient.phone)}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span class="detail-label">
                            Email
                        </span>

                        <strong>
                            ${displayValue(patient.email)}
                        </strong>

                    </div>


                    <div class="detail-item detail-full">

                        <span class="detail-label">
                            Address
                        </span>

                        <strong>
                            ${displayValue(patient.address)}
                        </strong>

                    </div>


                </div>


                <div
                    style="
                        display:flex;
                        justify-content:flex-end;
                        gap:10px;
                        margin-top:24px;
                    "
                >

                    <button
                        type="button"
                        class="btn"
                        id="closeViewPatientButton"
                    >
                        Close
                    </button>

                    <button
                        type="button"
                        class="btn btn-primary"
                        id="viewPatientEditButton"
                    >
                        Edit Patient
                    </button>

                </div>

            </div>

        </div>
    `;


    document.body.appendChild(modal);


    /* Close using X */

    document
        .getElementById(
            "closeViewPatientModal"
        )
        .addEventListener(
            "click",
            () => modal.remove()
        );


    /* Close using Close button */

    document
        .getElementById(
            "closeViewPatientButton"
        )
        .addEventListener(
            "click",
            () => modal.remove()
        );


    /* Edit directly from View */

    document
        .getElementById(
            "viewPatientEditButton"
        )
        .addEventListener(
            "click",
            () => {

                modal.remove();

                editPatient(dbId);

            }
        );


    /* Close when clicking outside the box */

    modal.addEventListener(
        "click",
        function(event) {

            if (event.target === modal) {

                modal.remove();

            }

        }
    );
}

/* =========================================================
   DELETE
   ========================================================= */

async function deletePatientById(dbId) {

    const patient =
        allPatients.find(
            p =>
                Number(p.id) ===
                Number(dbId)
        );


    if (!patient) {

        showToast(
            "Patient not found.",
            "error"
        );

        return;
    }


    const displayPatientId =
        getPatientDisplayId(
            patient
        );


    const patientName =
        getPatientFullName(
            patient
        );


    const confirmed =
        window.confirm(
            `Are you sure you want to delete ${
                patientName ||
                displayPatientId
            }?`
        );


    if (!confirmed) {
        return;
    }


    try {

        /*
         * Backend expects display ID,
         * e.g. P006.
         */

        await deletePatient(
            displayPatientId
        );


        showToast(
            "Patient deleted successfully.",
            "success"
        );


        await loadPatients();


    } catch (error) {

        console.error(
            "Patient delete error:",
            error
        );


        showToast(
            error.message ||
            "Failed to delete patient.",
            "error"
        );
    }
}


/* =========================================================
   CLOSE MODAL
   ========================================================= */

function closePatientModal() {

    const modal =
        document.getElementById(
            "patientModal"
        );


    if (modal) {

        modal.style.display =
            "none";

    }


    editingPatientId = null;


    const form =
        document.getElementById(
            "patientForm"
        );


    if (form) {

        form.reset();

    }
}


/* =========================================================
   NEXT PATIENT ID
   ========================================================= */

function generateNextPatientId() {

    let highestNumber = 0;


    allPatients.forEach(
        patient => {

            const id =
                getPatientDisplayId(
                    patient
                );


            if (!id) {
                return;
            }


            const match =
                String(id).match(
                    /^P(\d+)$/i
                );


            if (match) {

                highestNumber =
                    Math.max(
                        highestNumber,
                        Number(
                            match[1]
                        )
                    );

            }

        }
    );


    return `P${String(
        highestNumber + 1
    ).padStart(3, "0")}`;
}


/* =========================================================
   INPUT HELPERS
   ========================================================= */

function getInputValue(id) {

    const element =
        document.getElementById(id);


    return element
        ? element.value
        : "";
}


function setInputValue(
    id,
    value
) {

    const element =
        document.getElementById(id);


    if (element) {

        element.value =
            value === null ||
            value === undefined
                ? ""
                : value;

    }
}


/* =========================================================
   GLOBAL FUNCTIONS
   ========================================================= */

window.loadPatients =
    loadPatients;

window.editPatient =
    editPatient;

window.viewPatient =
    viewPatient;

window.deletePatientById =
    deletePatientById;

window.openAddPatientModal =
    openAddPatientModal;

window.closePatientModal =
    closePatientModal;
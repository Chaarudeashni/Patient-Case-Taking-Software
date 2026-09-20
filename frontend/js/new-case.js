/* =========================================================
   PATIENT CASE TAKING SOFTWARE
   NEW CLINICAL CASE
   ========================================================= */

let casePatients = [];
let currentStep = 1;
let selectedPatient = null;

let caseFormData = {
    caseDate: "",
    chiefComplaint: "",
    complaintDuration: "",
    complaintSeverity: "",

    presentHistory: "",
    pastHistory: "",
    personalHistory: "",
    familyHistory: "",

    rosGeneral: "",
    rosRespiratory: "",
    rosCardiovascular: "",
    rosGastrointestinal: "",
    rosNeurological: "",
    rosGenitourinary: "",
    rosMusculoskeletal: "",
    rosSkin: "",

    ayushSystem: "",
    ayushTreatment: "",
    ayushHistory: "",
    ayushResponse: ""
};


/* =========================================================
   INITIALIZATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeNewCase
);


async function initializeNewCase() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        console.error("pageContent not found.");
        return;
    }

    caseFormData.caseDate = getTodayDate();

    renderNewCaseLoading();

    try {

        const patients = await getPatients();

        casePatients =
            Array.isArray(patients)
                ? patients
                : [];

        renderNewCasePage();

    } catch (error) {

        console.error(
            "New Case loading error:",
            error
        );

        renderNewCaseError(
            error.message ||
            "Unable to load patients."
        );
    }
}


/* =========================================================
   MAIN PAGE
   ========================================================= */

function renderNewCasePage() {

    const pageContent =
        document.getElementById("pageContent");

    if (!pageContent) {
        return;
    }

    pageContent.innerHTML = `

        <div class="case-stepper">

            <div class="case-step active" data-step="1">
                <div class="step-number">1</div>
                <div class="step-content">
                    <strong>Patient</strong>
                    <span>Patient information</span>
                </div>
            </div>

            <div class="step-line"></div>

            <div class="case-step" data-step="2">
                <div class="step-number">2</div>
                <div class="step-content">
                    <strong>Chief Complaint</strong>
                    <span>Main concern</span>
                </div>
            </div>

            <div class="step-line"></div>

            <div class="case-step" data-step="3">
                <div class="step-number">3</div>
                <div class="step-content">
                    <strong>History</strong>
                    <span>Clinical history</span>
                </div>
            </div>

            <div class="step-line"></div>

            <div class="case-step" data-step="4">
                <div class="step-number">4</div>
                <div class="step-content">
                    <strong>Review of Systems</strong>
                    <span>System review</span>
                </div>
            </div>

            <div class="step-line"></div>

            <div class="case-step" data-step="5">
                <div class="step-number">5</div>
                <div class="step-content">
                    <strong>AYUSH History</strong>
                    <span>AYUSH information</span>
                </div>
            </div>

            <div class="step-line"></div>

            <div class="case-step" data-step="6">
                <div class="step-number">6</div>
                <div class="step-content">
                    <strong>Review & Save</strong>
                    <span>Complete case</span>
                </div>
            </div>

        </div>

        <div id="caseFormContainer"></div>

        <div
            id="caseError"
            class="form-error"
            style="display:none;"
        ></div>
    `;

    renderStep(1);
}


/* =========================================================
   STEP CONTROLLER
   ========================================================= */

function renderStep(step) {

    saveCurrentStepData();

    currentStep = step;

    updateStepper();

    const container =
        document.getElementById(
            "caseFormContainer"
        );

    if (!container) {
        console.error(
            "caseFormContainer not found."
        );
        return;
    }

    if (step === 1) {
        renderPatientStep(container);

    } else if (step === 2) {
        renderComplaintStep(container);

    } else if (step === 3) {
        renderHistoryStep(container);

    } else if (step === 4) {
        renderRosStep(container);

    } else if (step === 5) {
        renderAyushStep(container);

    } else if (step === 6) {
        renderReviewStep(container);

    } else {
        renderPatientStep(container);
    }
}


/* =========================================================
   STEP 1 — PATIENT
   ========================================================= */

function renderPatientStep(container) {

    let patientOptions = "";

    casePatients.forEach(function(patient) {

        const isSelected =
            selectedPatient &&
            Number(selectedPatient.id) ===
            Number(patient.id);

        patientOptions += `
            <option
                value="${patient.id}"
                ${isSelected ? "selected" : ""}
            >
                ${escapeHtml(
                    getPatientDisplayId(patient)
                )}
                -
                ${escapeHtml(
                    getPatientFullName(patient)
                )}
            </option>
        `;
    });


    container.innerHTML = `

        <div class="content-card">

            <div class="card-header">

                <div>
                    <h3>Select Patient</h3>

                    <p>
                        Select an existing patient
                        for this clinical case.
                    </p>
                </div>

                <button
                    type="button"
                    class="secondary-button"
                    id="createPatientFromCase"
                >
                    + New Patient
                </button>

            </div>


            <div class="form-group">

                <label for="casePatientSelect">
                    Patient
                </label>

                <select
                    id="casePatientSelect"
                    required
                >

                    <option value="">
                        Select a patient
                    </option>

                    ${patientOptions}

                </select>

            </div>


            <div
                id="selectedPatientPreview"
                class="patient-preview"
            >
                ${renderSelectedPatientPreview()}
            </div>


            <div class="form-group">

                <label for="caseDate">
                    Case Date
                </label>

                <input
                    type="date"
                    id="caseDate"
                    value="${escapeHtml(
                        caseFormData.caseDate
                    )}"
                    required
                >

            </div>


            <div class="case-navigation">

                <div></div>

                <button
                    type="button"
                    class="primary-button"
                    id="nextToComplaint"
                >
                    Next
                </button>

            </div>

        </div>
    `;


    const patientSelect =
        document.getElementById(
            "casePatientSelect"
        );

    if (patientSelect) {

        patientSelect.addEventListener(
            "change",
            function() {

                const selectedId =
                    Number(this.value);

                selectedPatient =
                    casePatients.find(
                        function(patient) {
                            return Number(
                                patient.id
                            ) === selectedId;
                        }
                    ) || null;


                const preview =
                    document.getElementById(
                        "selectedPatientPreview"
                    );

                if (preview) {

                    preview.innerHTML =
                        renderSelectedPatientPreview();

                }
            }
        );
    }


    const newPatientButton =
        document.getElementById(
            "createPatientFromCase"
        );

    if (newPatientButton) {

        newPatientButton.addEventListener(
            "click",
            function() {

                window.location.href =
                    "patients.html";

            }
        );
    }


    const nextButton =
        document.getElementById(
            "nextToComplaint"
        );

    if (nextButton) {

        nextButton.addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                if (!selectedPatient) {

                    showCaseError(
                        "Please select a patient."
                    );

                    return;
                }

                clearCaseError();

                renderStep(2);

            }
        );
    }
}


/* =========================================================
   STEP 2 — CHIEF COMPLAINT
   ========================================================= */

function renderComplaintStep(container) {

    container.innerHTML = `

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Chief Complaint
                    </h3>

                    <p>
                        Record the patient's primary
                        complaint or reason for consultation.
                    </p>

                </div>

            </div>


            <div class="form-group">

                <label for="chiefComplaint">
                    Chief Complaint
                </label>

                <textarea
                    id="chiefComplaint"
                    rows="5"
                    placeholder="Describe the patient's main complaint..."
                >${escapeHtml(
                    caseFormData.chiefComplaint
                )}</textarea>

            </div>


            <div class="form-grid">

                <div class="form-group">

                    <label for="complaintDuration">
                        Duration
                    </label>

                    <input
                        type="text"
                        id="complaintDuration"
                        value="${escapeHtml(
                            caseFormData.complaintDuration
                        )}"
                        placeholder="Example: 3 days"
                    >

                </div>


                <div class="form-group">

                    <label for="complaintSeverity">
                        Severity
                    </label>

                    <select id="complaintSeverity">

                        <option value="">
                            Select severity
                        </option>

                        <option
                            value="Mild"
                            ${caseFormData.complaintSeverity === "Mild"
                                ? "selected"
                                : ""}
                        >
                            Mild
                        </option>

                        <option
                            value="Moderate"
                            ${caseFormData.complaintSeverity === "Moderate"
                                ? "selected"
                                : ""}
                        >
                            Moderate
                        </option>

                        <option
                            value="Severe"
                            ${caseFormData.complaintSeverity === "Severe"
                                ? "selected"
                                : ""}
                        >
                            Severe
                        </option>

                    </select>

                </div>

            </div>


            ${caseNavigationButtons(
                "Back",
                "backToPatient",
                "Next",
                "nextToHistory"
            )}

        </div>
    `;


    document
        .getElementById("backToPatient")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                renderStep(1);

            }
        );


    document
        .getElementById("nextToHistory")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                if (
                    !caseFormData.chiefComplaint ||
                    !caseFormData.chiefComplaint.trim()
                ) {

                    showCaseError(
                        "Please enter the chief complaint."
                    );

                    return;
                }

                clearCaseError();

                renderStep(3);

            }
        );
}


/* =========================================================
   STEP 3 — HISTORY
   ========================================================= */

function renderHistoryStep(container) {

    container.innerHTML = `

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Clinical History
                    </h3>

                    <p>
                        Record relevant patient history.
                    </p>

                </div>

            </div>


            <div class="form-group">

                <label for="presentHistory">
                    Present History
                </label>

                <textarea
                    id="presentHistory"
                    rows="5"
                    placeholder="Describe the history of the present complaint..."
                >${escapeHtml(
                    caseFormData.presentHistory
                )}</textarea>

            </div>


            <div class="form-group">

                <label for="pastHistory">
                    Past Medical History
                </label>

                <textarea
                    id="pastHistory"
                    rows="4"
                    placeholder="Previous illnesses, treatments or procedures..."
                >${escapeHtml(
                    caseFormData.pastHistory
                )}</textarea>

            </div>


            <div class="form-group">

                <label for="personalHistory">
                    Personal History
                </label>

                <textarea
                    id="personalHistory"
                    rows="4"
                    placeholder="Diet, sleep, habits, occupation and other relevant information..."
                >${escapeHtml(
                    caseFormData.personalHistory
                )}</textarea>

            </div>


            <div class="form-group">

                <label for="familyHistory">
                    Family History
                </label>

                <textarea
                    id="familyHistory"
                    rows="4"
                    placeholder="Relevant family medical history..."
                >${escapeHtml(
                    caseFormData.familyHistory
                )}</textarea>

            </div>


            ${caseNavigationButtons(
                "Back",
                "backToComplaint",
                "Next",
                "nextToRos"
            )}

        </div>
    `;


    document
        .getElementById("backToComplaint")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                renderStep(2);

            }
        );


    document
        .getElementById("nextToRos")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                clearCaseError();

                renderStep(4);

            }
        );
}


/* =========================================================
   STEP 4 — REVIEW OF SYSTEMS
   ========================================================= */

function renderRosStep(container) {

    container.innerHTML = `

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Review of Systems
                    </h3>

                    <p>
                        Record relevant symptoms by system.
                    </p>

                </div>

            </div>


            <div class="form-grid">

                ${rosField(
                    "rosGeneral",
                    "General",
                    "Fever, fatigue, weight changes..."
                )}

                ${rosField(
                    "rosRespiratory",
                    "Respiratory",
                    "Cough, breathlessness..."
                )}

                ${rosField(
                    "rosCardiovascular",
                    "Cardiovascular",
                    "Chest pain, palpitations..."
                )}

                ${rosField(
                    "rosGastrointestinal",
                    "Gastrointestinal",
                    "Nausea, vomiting, abdominal symptoms..."
                )}

                ${rosField(
                    "rosNeurological",
                    "Neurological",
                    "Headache, dizziness, weakness..."
                )}

                ${rosField(
                    "rosGenitourinary",
                    "Genitourinary",
                    "Urinary or reproductive symptoms..."
                )}

                ${rosField(
                    "rosMusculoskeletal",
                    "Musculoskeletal",
                    "Pain, stiffness, mobility..."
                )}

                ${rosField(
                    "rosSkin",
                    "Skin",
                    "Rashes, itching, skin changes..."
                )}

            </div>


            ${caseNavigationButtons(
                "Back",
                "backToHistory",
                "Next",
                "nextToAyush"
            )}

        </div>
    `;


    document
        .getElementById("backToHistory")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                renderStep(3);

            }
        );


    document
        .getElementById("nextToAyush")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                clearCaseError();

                renderStep(5);

            }
        );
}


function rosField(
    id,
    label,
    placeholder
) {

    return `

        <div class="form-group">

            <label for="${id}">
                ${label}
            </label>

            <textarea
                id="${id}"
                rows="3"
                placeholder="${placeholder}"
            >${escapeHtml(
                caseFormData[id] || ""
            )}</textarea>

        </div>
    `;
}


/* =========================================================
   STEP 5 — AYUSH
   ========================================================= */

function renderAyushStep(container) {

    container.innerHTML = `

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        AYUSH History
                    </h3>

                    <p>
                        Record relevant AYUSH treatment
                        and history information.
                    </p>

                </div>

            </div>


            <div class="form-grid">

                <div class="form-group">

                    <label for="ayushSystem">
                        System of Medicine
                    </label>

                    <select id="ayushSystem">

                        <option value="">
                            Select system
                        </option>

                        <option
                            value="Ayurveda"
                            ${caseFormData.ayushSystem === "Ayurveda"
                                ? "selected"
                                : ""}
                        >
                            Ayurveda
                        </option>

                        <option
                            value="Yoga"
                            ${caseFormData.ayushSystem === "Yoga"
                                ? "selected"
                                : ""}
                        >
                            Yoga
                        </option>

                        <option
                            value="Naturopathy"
                            ${caseFormData.ayushSystem === "Naturopathy"
                                ? "selected"
                                : ""}
                        >
                            Naturopathy
                        </option>

                        <option
                            value="Unani"
                            ${caseFormData.ayushSystem === "Unani"
                                ? "selected"
                                : ""}
                        >
                            Unani
                        </option>

                        <option
                            value="Siddha"
                            ${caseFormData.ayushSystem === "Siddha"
                                ? "selected"
                                : ""}
                        >
                            Siddha
                        </option>

                        <option
                            value="Homeopathy"
                            ${caseFormData.ayushSystem === "Homeopathy"
                                ? "selected"
                                : ""}
                        >
                            Homeopathy
                        </option>

                        <option
                            value="Other"
                            ${caseFormData.ayushSystem === "Other"
                                ? "selected"
                                : ""}
                        >
                            Other
                        </option>

                    </select>

                </div>


                <div class="form-group">

                    <label for="ayushTreatment">
                        Current Treatment
                    </label>

                    <input
                        type="text"
                        id="ayushTreatment"
                        value="${escapeHtml(
                            caseFormData.ayushTreatment
                        )}"
                        placeholder="Current AYUSH treatment"
                    >

                </div>

            </div>


            <div class="form-group">

                <label for="ayushHistory">
                    Treatment / History Details
                </label>

                <textarea
                    id="ayushHistory"
                    rows="5"
                    placeholder="Previous or current AYUSH treatments, medicines and response..."
                >${escapeHtml(
                    caseFormData.ayushHistory
                )}</textarea>

            </div>


            <div class="form-group">

                <label for="ayushResponse">
                    Treatment Response
                </label>

                <textarea
                    id="ayushResponse"
                    rows="3"
                    placeholder="Describe response to previous treatment..."
                >${escapeHtml(
                    caseFormData.ayushResponse
                )}</textarea>

            </div>


            ${caseNavigationButtons(
                "Back",
                "backToRos",
                "Next",
                "nextToReview"
            )}

        </div>
    `;


    document
        .getElementById("backToRos")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                renderStep(4);

            }
        );


    document
        .getElementById("nextToReview")
        .addEventListener(
            "click",
            function() {

                saveCurrentStepData();

                clearCaseError();

                renderStep(6);

            }
        );
}


/* =========================================================
   STEP 6 — REVIEW
   ========================================================= */

function renderReviewStep(container) {

    saveCurrentStepData();

    const patient = selectedPatient;


    container.innerHTML = `

        <div class="content-card">

            <div class="card-header">

                <div>

                    <h3>
                        Review Clinical Case
                    </h3>

                    <p>
                        Review the information before
                        saving the case.
                    </p>

                </div>

            </div>


            <div class="review-section">

                <h4>Patient</h4>

                <div class="detail-grid">

                    <div class="detail-item">

                        <span>Patient ID</span>

                        <strong>
                            ${escapeHtml(
                                getPatientDisplayId(patient)
                            )}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span>Name</span>

                        <strong>
                            ${escapeHtml(
                                getPatientFullName(patient)
                            )}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span>Gender</span>

                        <strong>
                            ${escapeHtml(
                                patient &&
                                patient.gender
                                    ? patient.gender
                                    : "-"
                            )}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span>Case Date</span>

                        <strong>
                            ${formatDate(
                                caseFormData.caseDate
                            )}
                        </strong>

                    </div>

                </div>

            </div>


            <div class="review-section">

                <h4>Chief Complaint</h4>

                <p class="review-text">
                    ${escapeHtml(
                        caseFormData.chiefComplaint || "-"
                    )}
                </p>

                <div class="detail-grid">

                    <div class="detail-item">

                        <span>Duration</span>

                        <strong>
                            ${escapeHtml(
                                caseFormData.complaintDuration || "-"
                            )}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span>Severity</span>

                        <strong>
                            ${escapeHtml(
                                caseFormData.complaintSeverity || "-"
                            )}
                        </strong>

                    </div>

                </div>

            </div>


            <div class="review-section">

                <h4>Clinical History</h4>

                <div class="review-list">

                    ${reviewTextBlock(
                        "Present History",
                        caseFormData.presentHistory
                    )}

                    ${reviewTextBlock(
                        "Past History",
                        caseFormData.pastHistory
                    )}

                    ${reviewTextBlock(
                        "Personal History",
                        caseFormData.personalHistory
                    )}

                    ${reviewTextBlock(
                        "Family History",
                        caseFormData.familyHistory
                    )}

                </div>

            </div>


            <div class="review-section">

                <h4>Review of Systems</h4>

                ${renderRosReview()}

            </div>


            <div class="review-section">

                <h4>AYUSH History</h4>

                <div class="detail-grid">

                    <div class="detail-item">

                        <span>System</span>

                        <strong>
                            ${escapeHtml(
                                caseFormData.ayushSystem || "-"
                            )}
                        </strong>

                    </div>


                    <div class="detail-item">

                        <span>Current Treatment</span>

                        <strong>
                            ${escapeHtml(
                                caseFormData.ayushTreatment || "-"
                            )}
                        </strong>

                    </div>

                </div>


                <p class="review-text">

                    <strong>
                        History:
                    </strong>

                    ${escapeHtml(
                        caseFormData.ayushHistory || "-"
                    )}

                </p>


                <p class="review-text">

                    <strong>
                        Response:
                    </strong>

                    ${escapeHtml(
                        caseFormData.ayushResponse || "-"
                    )}

                </p>

            </div>


            <div class="case-navigation">

                <button
                    type="button"
                    class="secondary-button"
                    id="backToAyush"
                >
                    Back
                </button>


                <button
                    type="button"
                    class="primary-button"
                    id="saveCompleteCase"
                >
                    Save Clinical Case
                </button>

            </div>

        </div>
    `;


    document
        .getElementById("backToAyush")
        .addEventListener(
            "click",
            function() {

                renderStep(5);

            }
        );


    document
        .getElementById("saveCompleteCase")
        .addEventListener(
            "click",
            saveCompleteCase
        );
}


/* =========================================================
   SAVE COMPLETE CASE
   ========================================================= */

async function saveCompleteCase() {

    saveCurrentStepData();


    const button =
        document.getElementById(
            "saveCompleteCase"
        );


    /* -----------------------------------------------------
       VALIDATION
       ----------------------------------------------------- */

    if (!selectedPatient) {

        showCaseError(
            "Please select a patient."
        );

        return;
    }


    if (
        !caseFormData.chiefComplaint ||
        !caseFormData.chiefComplaint.trim()
    ) {

        showCaseError(
            "Chief complaint is required."
        );

        renderStep(2);

        return;
    }


    /* -----------------------------------------------------
       CURRENT USER
       ----------------------------------------------------- */

    const currentUser =
        getStoredUser();


    /* -----------------------------------------------------
       DISABLE SAVE BUTTON
       ----------------------------------------------------- */

    if (button) {

        button.disabled = true;

        button.textContent =
            "Saving Case...";
    }


    clearCaseError();


    try {

        /*
         * IMPORTANT:
         *
         * The backend CompleteCase schema expects
         * FLAT STRING fields.
         *
         * Do NOT send:
         *
         * complaint: {
         *     complaint: "..."
         * }
         *
         * or:
         *
         * present_history: {
         *     history: "..."
         * }
         *
         * The correct backend field names are:
         *
         * chief_complaint
         * history_present_illness
         * past_medical_history
         * personal_notes
         * family_history
         */


        const caseData = {

            /* -------------------------------------------------
               BASIC CASE INFORMATION
               ------------------------------------------------- */

            patient_id:
                Number(
                    selectedPatient.id
                ),

            clinician_id:
                Number(
                    currentUser?.id || 1
                ),

            case_date:
                caseFormData.caseDate ||
                getTodayDate(),

            status:
                "active",


            /* -------------------------------------------------
               CHIEF COMPLAINT
               ------------------------------------------------- */

            chief_complaint:
                caseFormData.chiefComplaint ||
                "",

            duration:
                caseFormData.complaintDuration ||
                "",

            duration_unit:
                "",

            additional_complaints:
                "",

            severity:
                caseFormData.complaintSeverity ||
                "",

            complaint_notes:
                "",


            /* -------------------------------------------------
               PRESENT HISTORY
               ------------------------------------------------- */

            history_present_illness:
                caseFormData.presentHistory ||
                "",

            onset:
                "",

            course:
                "",

            associated_symptoms:
                "",

            aggravating_factors:
                "",

            relieving_factors:
                "",

            previous_treatment:
                "",

            history_notes:
                "",


            /* -------------------------------------------------
               PAST HISTORY
               ------------------------------------------------- */

            past_medical_history:
                caseFormData.pastHistory ||
                "",

            past_surgical_history:
                "",

            allergies:
                "",

            medications:
                "",

            hospitalization_details:
                "",

            past_history_notes:
                "",


            /* -------------------------------------------------
               PERSONAL HISTORY
               ------------------------------------------------- */

            diet:
                "",

            appetite:
                "",

            sleep:
                "",

            bowel:
                "",

            bladder:
                "",

            exercise:
                "",

            smoking:
                "",

            alcohol:
                "",

            personal_notes:
                caseFormData.personalHistory ||
                "",


            /* -------------------------------------------------
               FAMILY HISTORY
               ------------------------------------------------- */

            family_history:
                caseFormData.familyHistory ||
                "",


            /* -------------------------------------------------
               EXAMINATION
               ------------------------------------------------- */

            temperature:
                "",

            pulse:
                "",

            respiratory_rate:
                "",

            blood_pressure:
                "",

            spo2:
                "",

            weight:
                "",

            height:
                "",

            general_examination:
                "",

            system_examination:
                "",


            /* -------------------------------------------------
               ASSESSMENT
               ------------------------------------------------- */

            provisional_diagnosis:
                "",

            differential_diagnosis:
                "",

            clinical_assessment:
                "",

            treatment_plan:
                ""
        };


        console.log(
            "CORRECTED clinical case payload:",
            caseData
        );


        /* -----------------------------------------------------
           CREATE MAIN CASE
           ----------------------------------------------------- */

        const createdCase =
            await createCompleteCase(
                caseData
            );


        console.log(
            "Created case:",
            createdCase
        );


        const createdCaseId =
            createdCase?.id;


        /* -----------------------------------------------------
           SAVE ROS
           ----------------------------------------------------- */

        if (createdCaseId) {

            const rosData =
                buildRosData();


            const hasRosData =
                Object.values(
                    rosData
                ).some(
                    value =>
                        String(
                            value || ""
                        ).trim() !== ""
                );


            if (hasRosData) {

                try {

                    await createReviewOfSystems(
                        createdCaseId,
                        rosData
                    );


                    console.log(
                        "Review of Systems saved successfully."
                    );

                } catch (rosError) {

                    console.warn(
                        "ROS save warning:",
                        rosError
                    );

                    console.warn(
                        "ROS payload was:",
                        rosData
                    );
                }
            }


            /* -------------------------------------------------
               SAVE AYUSH
               ------------------------------------------------- */

            const ayushData =
                buildAyushData();


            const hasAyushData =
                Object.values(
                    ayushData
                ).some(
                    value =>
                        String(
                            value || ""
                        ).trim() !== ""
                );


            if (hasAyushData) {

                try {

                    await createAyushHistory(
                        createdCaseId,
                        ayushData
                    );


                    console.log(
                        "AYUSH history saved successfully."
                    );

                } catch (ayushError) {

                    console.warn(
                        "AYUSH save warning:",
                        ayushError
                    );

                    console.warn(
                        "AYUSH payload was:",
                        ayushData
                    );
                }
            }
        }


        /* -----------------------------------------------------
           SUCCESS
           ----------------------------------------------------- */

        showCaseSuccess(
            createdCase
        );


    } catch (error) {

        console.error(
            "Complete case save error:",
            error
        );


        showCaseError(
            error.message ||
            "Unable to save clinical case."
        );


        if (button) {

            button.disabled = false;

            button.textContent =
                "Save Clinical Case";
        }
    }
}


/* =========================================================
   SUCCESS
   ========================================================= */

function showCaseSuccess(createdCase) {

    const container =
        document.getElementById(
            "caseFormContainer"
        );


    if (!container) {
        return;
    }


    const caseId =
        createdCase &&
        (
            createdCase.case_id ||
            createdCase.id
        )
            ? (
                createdCase.case_id ||
                createdCase.id
            )
            : "-";


    container.innerHTML = `

        <div class="content-card">

            <div class="success-state">

                <div class="success-icon">
                    ✓
                </div>


                <h2>
                    Clinical Case Saved
                </h2>


                <p>
                    The patient clinical case has been
                    successfully saved.
                </p>


                <div class="success-details">

                    <div>

                        <span>
                            Patient
                        </span>

                        <strong>
                            ${escapeHtml(
                                getPatientFullName(
                                    selectedPatient
                                )
                            )}
                        </strong>

                    </div>


                    <div>

                        <span>
                            Patient ID
                        </span>

                        <strong>
                            ${escapeHtml(
                                getPatientDisplayId(
                                    selectedPatient
                                )
                            )}
                        </strong>

                    </div>


                    <div>

                        <span>
                            Case ID
                        </span>

                        <strong>
                            ${escapeHtml(
                                caseId
                            )}
                        </strong>

                    </div>


                    <div>

                        <span>
                            Case Date
                        </span>

                        <strong>
                            ${formatDate(
                                caseFormData.caseDate
                            )}
                        </strong>

                    </div>

                </div>


                <div class="success-actions">

                    <button
                        type="button"
                        class="secondary-button"
                        id="viewClinicalRecords"
                    >
                        View Clinical Records
                    </button>


                    <button
                        type="button"
                        class="primary-button"
                        id="createAnotherCase"
                    >
                        Create Another Case
                    </button>

                </div>

            </div>

        </div>
    `;


    updateStepperComplete();


    const viewButton =
        document.getElementById(
            "viewClinicalRecords"
        );

    if (viewButton) {

        viewButton.addEventListener(
            "click",
            function() {

                window.location.href =
                    "clinical-records.html";

            }
        );
    }


    const anotherButton =
        document.getElementById(
            "createAnotherCase"
        );

    if (anotherButton) {

        anotherButton.addEventListener(
            "click",
            function() {

                window.location.reload();

            }
        );
    }
}


/* =========================================================
   ROS DATA
   ========================================================= */

function buildRosData() {

    return {

        general:
            caseFormData.rosGeneral || "",

        respiratory:
            caseFormData.rosRespiratory || "",

        cardiovascular:
            caseFormData.rosCardiovascular || "",

        gastrointestinal:
            caseFormData.rosGastrointestinal || "",

        neurological:
            caseFormData.rosNeurological || "",

        genitourinary:
            caseFormData.rosGenitourinary || "",

        musculoskeletal:
            caseFormData.rosMusculoskeletal || "",

        skin:
            caseFormData.rosSkin || ""

    };
}


/* =========================================================
   AYUSH DATA
   ========================================================= */

function buildAyushData() {

    return {

        system:
            caseFormData.ayushSystem || "",

        treatment:
            caseFormData.ayushTreatment || "",

        history:
            caseFormData.ayushHistory || "",

        response:
            caseFormData.ayushResponse || ""

    };
}


/* =========================================================
   ROS REVIEW
   ========================================================= */

function renderRosReview() {

    const systems = [

        ["General", "rosGeneral"],
        ["Respiratory", "rosRespiratory"],
        ["Cardiovascular", "rosCardiovascular"],
        ["Gastrointestinal", "rosGastrointestinal"],
        ["Neurological", "rosNeurological"],
        ["Genitourinary", "rosGenitourinary"],
        ["Musculoskeletal", "rosMusculoskeletal"],
        ["Skin", "rosSkin"]

    ];


    return `

        <div class="review-list">

            ${systems.map(
                function(item) {

                    const label = item[0];
                    const id = item[1];

                    return `

                        <div>

                            <strong>
                                ${label}
                            </strong>

                            <p>
                                ${escapeHtml(
                                    caseFormData[id] ||
                                    "-"
                                )}
                            </p>

                        </div>

                    `;

                }
            ).join("")}

        </div>
    `;
}


/* =========================================================
   PATIENT PREVIEW
   ========================================================= */

function renderSelectedPatientPreview() {

    if (!selectedPatient) {

        return `

            <div class="empty-state compact">

                <p>
                    Select a patient to view
                    patient information.
                </p>

            </div>

        `;
    }


    return `

        <div class="patient-preview-card">

            <div class="patient-detail-avatar">

                ${getInitial(
                    getPatientFullName(
                        selectedPatient
                    )
                )}

            </div>


            <div>

                <strong>

                    ${escapeHtml(
                        getPatientFullName(
                            selectedPatient
                        )
                    )}

                </strong>


                <span>

                    ${escapeHtml(
                        getPatientDisplayId(
                            selectedPatient
                        )
                    )}

                </span>


                <small>

                    ${escapeHtml(
                        selectedPatient.gender ||
                        "-"
                    )}

                    ·

                    ${formatDate(
                        selectedPatient.date_of_birth
                    )}

                </small>

            </div>

        </div>
    `;
}


/* =========================================================
   PATIENT HELPERS
   ========================================================= */

function getPatientFullName(patient) {

    if (!patient) {
        return "-";
    }


    const firstName =
        patient.first_name ||
        "";

    const lastName =
        patient.last_name ||
        "";


    const fullName =
        `${firstName} ${lastName}`.trim();


    if (fullName) {
        return fullName;
    }


    return (
        patient.name ||
        patient.full_name ||
        "Patient"
    );
}


function getPatientDisplayId(patient) {

    if (!patient) {
        return "-";
    }


    return (
        patient.patient_id ||
        `P${patient.id}`
    );
}


/* =========================================================
   STEPPER
   ========================================================= */

function updateStepper() {

    const steps =
        document.querySelectorAll(
            ".case-step"
        );


    steps.forEach(
        function(step) {

            const stepNumber =
                Number(
                    step.dataset.step
                );


            step.classList.remove(
                "active",
                "completed"
            );


            if (
                stepNumber ===
                currentStep
            ) {

                step.classList.add(
                    "active"
                );

            } else if (
                stepNumber <
                currentStep
            ) {

                step.classList.add(
                    "completed"
                );
            }
        }
    );
}


function updateStepperComplete() {

    const steps =
        document.querySelectorAll(
            ".case-step"
        );


    steps.forEach(
        function(step) {

            step.classList.remove(
                "active"
            );

            step.classList.add(
                "completed"
            );

        }
    );
}


/* =========================================================
   NAVIGATION BUTTONS
   ========================================================= */

function caseNavigationButtons(
    backText,
    backId,
    nextText,
    nextId
) {

    return `

        <div class="case-navigation">

            <button
                type="button"
                class="secondary-button"
                id="${backId}"
            >
                ${backText}
            </button>


            <button
                type="button"
                class="primary-button"
                id="${nextId}"
            >
                ${nextText}
            </button>

        </div>
    `;
}


/* =========================================================
   SAVE CURRENT FORM DATA
   ========================================================= */

function saveCurrentStepData() {

    const caseDate =
        document.getElementById("caseDate");

    if (caseDate) {
        caseFormData.caseDate =
            caseDate.value;
    }


    const chiefComplaint =
        document.getElementById(
            "chiefComplaint"
        );

    if (chiefComplaint) {
        caseFormData.chiefComplaint =
            chiefComplaint.value.trim();
    }


    const complaintDuration =
        document.getElementById(
            "complaintDuration"
        );

    if (complaintDuration) {
        caseFormData.complaintDuration =
            complaintDuration.value.trim();
    }


    const complaintSeverity =
        document.getElementById(
            "complaintSeverity"
        );

    if (complaintSeverity) {
        caseFormData.complaintSeverity =
            complaintSeverity.value;
    }


    const historyFields = [
        "presentHistory",
        "pastHistory",
        "personalHistory",
        "familyHistory"
    ];


    historyFields.forEach(
        function(id) {

            const element =
                document.getElementById(id);

            if (element) {

                caseFormData[id] =
                    element.value.trim();

            }
        }
    );


    const rosFields = [
        "rosGeneral",
        "rosRespiratory",
        "rosCardiovascular",
        "rosGastrointestinal",
        "rosNeurological",
        "rosGenitourinary",
        "rosMusculoskeletal",
        "rosSkin"
    ];


    rosFields.forEach(
        function(id) {

            const element =
                document.getElementById(id);

            if (element) {

                caseFormData[id] =
                    element.value.trim();

            }
        }
    );


    const ayushFields = [
        "ayushSystem",
        "ayushTreatment",
        "ayushHistory",
        "ayushResponse"
    ];


    ayushFields.forEach(
        function(id) {

            const element =
                document.getElementById(id);

            if (element) {

                caseFormData[id] =
                    element.value.trim();

            }
        }
    );
}


/* =========================================================
   REVIEW TEXT
   ========================================================= */

function reviewTextBlock(
    label,
    value
) {

    return `

        <div>

            <strong>
                ${label}
            </strong>

            <p>
                ${escapeHtml(
                    value || "-"
                )}
            </p>

        </div>
    `;
}


/* =========================================================
   DATE
   ========================================================= */

function getTodayDate() {

    const now = new Date();

    const year =
        now.getFullYear();

    const month =
        String(
            now.getMonth() + 1
        ).padStart(
            2,
            "0"
        );

    const day =
        String(
            now.getDate()
        ).padStart(
            2,
            "0"
        );

    return `${year}-${month}-${day}`;
}


/* =========================================================
   INITIAL
   ========================================================= */

function getInitial(name) {

    return String(
        name || "P"
    )
        .trim()
        .charAt(0)
        .toUpperCase();
}


/* =========================================================
   ERROR HANDLING
   ========================================================= */

function clearCaseError() {

    const error =
        document.getElementById(
            "caseError"
        );


    if (!error) {
        return;
    }


    error.style.display =
        "none";

    error.textContent =
        "";
}


function showCaseError(message) {

    const error =
        document.getElementById(
            "caseError"
        );


    if (!error) {
        return;
    }


    error.textContent =
        message;


    error.style.display =
        "block";


    error.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


/* =========================================================
   LOADING
   ========================================================= */

function renderNewCaseLoading() {

    const pageContent =
        document.getElementById(
            "pageContent"
        );


    if (!pageContent) {
        return;
    }


    pageContent.innerHTML = `

        <div class="loading">

            <div class="spinner"></div>

            <span>
                Loading patients...
            </span>

        </div>
    `;
}


/* =========================================================
   LOAD ERROR
   ========================================================= */

function renderNewCaseError(message) {

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

                Unable to load the new case page.

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
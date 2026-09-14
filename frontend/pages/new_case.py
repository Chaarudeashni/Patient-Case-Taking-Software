import streamlit as st
from datetime import date
from utils.api import get_patients, create_complete_case
st.title("New Case")
st.write("Create a complete medical case for a patient.")

st.divider()

if "case_step" not in st.session_state:
    st.session_state["case_step"] = 1


# Store all case information in session state
if "case_data" not in st.session_state:
    st.session_state["case_data"] = {}


case_data = st.session_state["case_data"]

steps = [
    "Chief Complaints",
    "History",
    "Past History",
    "Personal History",
    "Examination",
    "Assessment",
    "Review",
]

current_step = st.session_state["case_step"]

def save_case_value(field_name, value):
    """Save a field value into the current case."""
    st.session_state["case_data"][field_name] = value

st.write(
    f"**Step {current_step} of {len(steps)}:** "
    f"{steps[current_step - 1]}"
)

st.progress(current_step / len(steps))


cols = st.columns(len(steps))

for i, step in enumerate(steps, start=1):

    with cols[i - 1]:

        if i == current_step:

            st.button(
                f"✓ {i}",
                key=f"current_step_{i}",
                use_container_width=True,
                disabled=True,
            )

        else:

            if st.button(
                str(i),
                key=f"goto_step_{i}",
                use_container_width=True,
            ):

                st.session_state["case_step"] = i
                st.rerun()


st.divider()

# Patient selection (database-backed)
try:
    _patients = get_patients()
except RuntimeError as _e:
    st.error(str(_e)); _patients = []
if _patients:
    _labels = {f"{p["patient_id"]} — {p["first_name"]} {p["last_name"]}" : p for p in _patients}
    _selected_label = st.selectbox("Patient *", list(_labels.keys()), key="case_patient")
    case_data["patient_db_id"] = _labels[_selected_label]["id"]
    case_data["patient_display"] = _selected_label
else:
    st.warning("Register a patient before creating a case.")

if current_step == 1:

    st.subheader("1. Chief Complaints")

    st.write(
        "Record the patient's main complaints and symptoms."
    )

    st.divider()

    st.write("### Main Complaint")

    chief_complaint = st.text_input(
        "Chief Complaint",
        value=case_data.get("chief_complaint", ""),
        placeholder="Example: Fever, headache, cough...",
        key="chief_complaint_input",
    )

    save_case_value("chief_complaint", chief_complaint)

    col1, col2 = st.columns(2)

    with col1:

        duration = st.number_input(
            "Duration",
            min_value=0,
            step=1,
            value=case_data.get("duration", 0),
            key="duration_input",
        )

        save_case_value("duration", duration)

    with col2:

        duration_unit = st.selectbox(
            "Duration Unit",
            [
                "Days",
                "Weeks",
                "Months",
                "Years",
            ],
            index=[
                "Days",
                "Weeks",
                "Months",
                "Years",
            ].index(
                case_data.get("duration_unit", "Days")
            ),
            key="duration_unit_input",
        )

        save_case_value("duration_unit", duration_unit)

    additional_complaints = st.text_area(
        "Additional Complaints",
        value=case_data.get("additional_complaints", ""),
        placeholder="Enter any other complaints or symptoms...",
        height=120,
        key="additional_complaints_input",
    )

    save_case_value(
        "additional_complaints",
        additional_complaints
    )

    severity = st.selectbox(
        "Severity",
        [
            "Select Severity",
            "Mild",
            "Moderate",
            "Severe",
        ],
        index=[
            "Select Severity",
            "Mild",
            "Moderate",
            "Severe",
        ].index(
            case_data.get(
                "severity",
                "Select Severity"
            )
        ),
        key="severity_input",
    )

    save_case_value("severity", severity)

    complaint_notes = st.text_area(
        "Additional Notes",
        value=case_data.get("complaint_notes", ""),
        placeholder="Enter any additional information...",
        height=100,
        key="complaint_notes_input",
    )

    save_case_value(
        "complaint_notes",
        complaint_notes
    )


# ============================================================
# STEP 2 — HISTORY
# ============================================================

elif current_step == 2:

    st.subheader("2. History")

    st.write(
        "Record the history related to the patient's present illness."
    )

    st.divider()

    st.write("### History of Present Illness")

    history_present_illness = st.text_area(
        "History of Present Illness",
        value=case_data.get(
            "history_present_illness",
            ""
        ),
        placeholder=(
            "Describe when the symptoms started, "
            "how they progressed, and relevant details..."
        ),
        height=160,
        key="history_present_illness_input",
    )

    save_case_value(
        "history_present_illness",
        history_present_illness
    )

    st.write("### Symptom Details")

    col1, col2 = st.columns(2)

    onset_options = [
        "Select Onset",
        "Sudden",
        "Gradual",
    ]

    course_options = [
        "Select Course",
        "Improving",
        "Worsening",
        "Stable",
        "Intermittent",
        "Continuous",
    ]

    with col1:

        onset = st.selectbox(
            "Onset",
            onset_options,
            index=onset_options.index(
                case_data.get(
                    "onset",
                    "Select Onset"
                )
            ),
            key="onset_input",
        )

        save_case_value("onset", onset)

    with col2:

        course = st.selectbox(
            "Course",
            course_options,
            index=course_options.index(
                case_data.get(
                    "course",
                    "Select Course"
                )
            ),
            key="course_input",
        )

        save_case_value("course", course)

    associated_symptoms = st.text_area(
        "Associated Symptoms",
        value=case_data.get(
            "associated_symptoms",
            ""
        ),
        placeholder=(
            "Enter other symptoms associated with "
            "the main complaint..."
        ),
        height=120,
        key="associated_symptoms_input",
    )

    save_case_value(
        "associated_symptoms",
        associated_symptoms
    )

    aggravating_factors = st.text_area(
        "Aggravating Factors",
        value=case_data.get(
            "aggravating_factors",
            ""
        ),
        placeholder="Enter factors that make symptoms worse...",
        height=100,
        key="aggravating_factors_input",
    )

    save_case_value(
        "aggravating_factors",
        aggravating_factors
    )

    relieving_factors = st.text_area(
        "Relieving Factors",
        value=case_data.get(
            "relieving_factors",
            ""
        ),
        placeholder="Enter factors that provide relief...",
        height=100,
        key="relieving_factors_input",
    )

    save_case_value(
        "relieving_factors",
        relieving_factors
    )

    previous_treatment = st.text_area(
        "Previous Treatment",
        value=case_data.get(
            "previous_treatment",
            ""
        ),
        placeholder=(
            "Enter any treatment or medication already "
            "taken for the current problem..."
        ),
        height=120,
        key="previous_treatment_input",
    )

    save_case_value(
        "previous_treatment",
        previous_treatment
    )

    history_notes = st.text_area(
        "Additional History Notes",
        value=case_data.get(
            "history_notes",
            ""
        ),
        placeholder="Enter any additional relevant history...",
        height=100,
        key="history_notes_input",
    )

    save_case_value(
        "history_notes",
        history_notes
    )

elif current_step == 3:

    st.subheader("3. Past History")

    st.write(
        "Record the patient's previous medical, surgical, "
        "allergy and medication history."
    )

    st.divider()

    st.write("### Past Medical History")

    past_medical_history = st.text_area(
        "Previous Medical Conditions",
        value=case_data.get(
            "past_medical_history",
            ""
        ),
        placeholder=(
            "Example: Diabetes, hypertension, asthma, "
            "heart disease..."
        ),
        height=130,
        key="past_medical_history_input",
    )

    save_case_value(
        "past_medical_history",
        past_medical_history
    )

    st.write("### Past Surgical History")

    past_surgical_history = st.text_area(
        "Previous Surgeries / Procedures",
        value=case_data.get(
            "past_surgical_history",
            ""
        ),
        placeholder=(
            "Enter previous surgeries, procedures "
            "or hospitalizations..."
        ),
        height=120,
        key="past_surgical_history_input",
    )

    save_case_value(
        "past_surgical_history",
        past_surgical_history
    )

    st.write("### Allergies")

    allergy_options = [
        "No Known Allergies",
        "Yes",
    ]

    allergy_status = st.radio(
        "Does the patient have any known allergies?",
        allergy_options,
        index=allergy_options.index(
            case_data.get(
                "allergy_status",
                "No Known Allergies"
            )
        ),
        horizontal=True,
        key="allergy_status_input",
    )

    save_case_value(
        "allergy_status",
        allergy_status
    )

    if allergy_status == "Yes":

        allergies = st.text_area(
            "Known Allergies",
            value=case_data.get(
                "allergies",
                ""
            ),
            placeholder=(
                "Enter drug, food or environmental allergies..."
            ),
            height=100,
            key="allergies_input",
        )

    else:

        allergies = "No Known Allergies"

    save_case_value("allergies", allergies)

    st.write("### Medication History")

    medication_options = [
        "No",
        "Yes",
    ]

    medication_status = st.radio(
        "Is the patient currently taking any medication?",
        medication_options,
        index=medication_options.index(
            case_data.get(
                "medication_status",
                "No"
            )
        ),
        horizontal=True,
        key="medication_status_input",
    )

    save_case_value(
        "medication_status",
        medication_status
    )

    if medication_status == "Yes":

        medications = st.text_area(
            "Current Medications",
            value=case_data.get(
                "medications",
                ""
            ),
            placeholder=(
                "Enter medication name, dosage and frequency..."
            ),
            height=120,
            key="medications_input",
        )

    else:

        medications = "No Current Medications"

    save_case_value(
        "medications",
        medications
    )

    st.write("### Family History")

    family_history = st.text_area(
        "Family Medical History",
        value=case_data.get(
            "family_history",
            ""
        ),
        placeholder=(
            "Enter relevant family history such as "
            "diabetes, hypertension, cancer or hereditary conditions..."
        ),
        height=120,
        key="family_history_input",
    )

    save_case_value(
        "family_history",
        family_history
    )

    st.write("### Previous Hospitalization")

    hospitalization_options = [
        "No",
        "Yes",
    ]

    hospitalization_status = st.radio(
        "Has the patient been hospitalized previously?",
        hospitalization_options,
        index=hospitalization_options.index(
            case_data.get(
                "hospitalization_status",
                "No"
            )
        ),
        horizontal=True,
        key="hospitalization_status_input",
    )

    save_case_value(
        "hospitalization_status",
        hospitalization_status
    )

    if hospitalization_status == "Yes":

        hospitalization_details = st.text_area(
            "Hospitalization Details",
            value=case_data.get(
                "hospitalization_details",
                ""
            ),
            placeholder=(
                "Enter reason for hospitalization, "
                "approximate date and relevant details..."
            ),
            height=120,
            key="hospitalization_details_input",
        )

    else:

        hospitalization_details = (
            "No Previous Hospitalization"
        )

    save_case_value(
        "hospitalization_details",
        hospitalization_details
    )

    past_history_notes = st.text_area(
        "Additional Past History Notes",
        value=case_data.get(
            "past_history_notes",
            ""
        ),
        placeholder="Enter any other relevant past history...",
        height=100,
        key="past_history_notes_input",
    )

    save_case_value(
        "past_history_notes",
        past_history_notes
    )

elif current_step == 4:

    st.subheader("4. Personal History")

    st.write(
        "Record the patient's lifestyle and personal history."
    )

    st.divider()

    st.write("### Lifestyle Information")

    col1, col2 = st.columns(2)

    with col1:

        diet = st.text_input(
            "Diet",
            value=case_data.get(
                "diet",
                ""
            ),
            placeholder="Example: Vegetarian / Mixed",
            key="diet_input",
        )

        save_case_value("diet", diet)

        appetite_options = [
            "Normal",
            "Increased",
            "Decreased",
        ]

        appetite = st.selectbox(
            "Appetite",
            appetite_options,
            index=appetite_options.index(
                case_data.get(
                    "appetite",
                    "Normal"
                )
            ),
            key="appetite_input",
        )

        save_case_value(
            "appetite",
            appetite
        )

        sleep_options = [
            "Normal",
            "Disturbed",
        ]

        sleep = st.selectbox(
            "Sleep",
            sleep_options,
            index=sleep_options.index(
                case_data.get(
                    "sleep",
                    "Normal"
                )
            ),
            key="sleep_input",
        )

        save_case_value(
            "sleep",
            sleep
        )

    with col2:

        bowel_options = [
            "Normal",
            "Abnormal",
        ]

        bowel = st.selectbox(
            "Bowel Habits",
            bowel_options,
            index=bowel_options.index(
                case_data.get(
                    "bowel",
                    "Normal"
                )
            ),
            key="bowel_input",
        )

        save_case_value(
            "bowel",
            bowel
        )

        bladder_options = [
            "Normal",
            "Abnormal",
        ]

        bladder = st.selectbox(
            "Bladder Habits",
            bladder_options,
            index=bladder_options.index(
                case_data.get(
                    "bladder",
                    "Normal"
                )
            ),
            key="bladder_input",
        )

        save_case_value(
            "bladder",
            bladder
        )

        exercise = st.text_input(
            "Exercise",
            value=case_data.get(
                "exercise",
                ""
            ),
            placeholder="Example: Walking 30 minutes daily",
            key="exercise_input",
        )

        save_case_value(
            "exercise",
            exercise
        )

    st.write("### Substance / Lifestyle History")

    smoking_options = [
        "Never",
        "Former",
        "Current",
    ]

    smoking = st.selectbox(
        "Smoking",
        smoking_options,
        index=smoking_options.index(
            case_data.get(
                "smoking",
                "Never"
            )
        ),
        key="smoking_input",
    )

    save_case_value(
        "smoking",
        smoking
    )

    alcohol_options = [
        "Never",
        "Former",
        "Current",
    ]

    alcohol = st.selectbox(
        "Alcohol Use",
        alcohol_options,
        index=alcohol_options.index(
            case_data.get(
                "alcohol",
                "Never"
            )
        ),
        key="alcohol_input",
    )

    save_case_value(
        "alcohol",
        alcohol
    )

    personal_notes = st.text_area(
        "Additional Personal History",
        value=case_data.get(
            "personal_notes",
            ""
        ),
        placeholder="Enter any additional personal history...",
        height=120,
        key="personal_notes_input",
    )

    save_case_value(
        "personal_notes",
        personal_notes
    )

elif current_step == 5:

    st.subheader("5. Examination")

    st.write(
        "Record the patient's vital signs and examination findings."
    )

    st.divider()

    st.write("### Vital Signs")

    col1, col2, col3 = st.columns(3)

    with col1:

        temperature = st.number_input(
            "Temperature (°F)",
            min_value=0.0,
            value=case_data.get(
                "temperature",
                0.0
            ),
            step=0.1,
            key="temperature_input",
        )

        save_case_value(
            "temperature",
            temperature
        )

    with col2:

        pulse = st.number_input(
            "Pulse (bpm)",
            min_value=0,
            value=case_data.get(
                "pulse",
                0
            ),
            step=1,
            key="pulse_input",
        )

        save_case_value(
            "pulse",
            pulse
        )

    with col3:

        respiratory_rate = st.number_input(
            "Respiratory Rate (/min)",
            min_value=0,
            value=case_data.get(
                "respiratory_rate",
                0
            ),
            step=1,
            key="respiratory_rate_input",
        )

        save_case_value(
            "respiratory_rate",
            respiratory_rate
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        blood_pressure = st.text_input(
            "Blood Pressure",
            value=case_data.get(
                "blood_pressure",
                ""
            ),
            placeholder="Example: 120/80",
            key="blood_pressure_input",
        )

        save_case_value(
            "blood_pressure",
            blood_pressure
        )

    with col2:

        spo2 = st.number_input(
            "SpO₂ (%)",
            min_value=0,
            max_value=100,
            value=case_data.get(
                "spo2",
                0
            ),
            step=1,
            key="spo2_input",
        )

        save_case_value(
            "spo2",
            spo2
        )

    with col3:

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            value=case_data.get(
                "weight",
                0.0
            ),
            step=0.1,
            key="weight_input",
        )

        save_case_value(
            "weight",
            weight
        )

    height = st.number_input(
        "Height (cm)",
        min_value=0.0,
        value=case_data.get(
            "height",
            0.0
        ),
        step=0.1,
        key="height_input",
    )

    save_case_value(
        "height",
        height
    )

    st.write("### General Examination")

    general_examination = st.text_area(
        "General Examination",
        value=case_data.get(
            "general_examination",
            ""
        ),
        placeholder=(
            "Enter general appearance, pallor, "
            "cyanosis, edema and other findings..."
        ),
        height=140,
        key="general_examination_input",
    )

    save_case_value(
        "general_examination",
        general_examination
    )

    st.write("### Systemic Examination")

    system_examination = st.text_area(
        "Systemic Examination",
        value=case_data.get(
            "system_examination",
            ""
        ),
        placeholder=(
            "Enter cardiovascular, respiratory, abdominal, "
            "neurological or other systemic findings..."
        ),
        height=150,
        key="system_examination_input",
    )

    save_case_value(
        "system_examination",
        system_examination
    )

elif current_step == 6:

    st.subheader("6. Assessment")

    st.write(
        "Record the clinical assessment, diagnosis and treatment plan."
    )

    st.divider()

    st.write("### Diagnosis")

    provisional_diagnosis = st.text_area(
        "Provisional Diagnosis",
        value=case_data.get(
            "provisional_diagnosis",
            ""
        ),
        placeholder="Enter the provisional diagnosis...",
        height=120,
        key="provisional_diagnosis_input",
    )

    save_case_value(
        "provisional_diagnosis",
        provisional_diagnosis
    )

    differential_diagnosis = st.text_area(
        "Differential Diagnosis",
        value=case_data.get(
            "differential_diagnosis",
            ""
        ),
        placeholder="Enter possible differential diagnoses...",
        height=120,
        key="differential_diagnosis_input",
    )

    save_case_value(
        "differential_diagnosis",
        differential_diagnosis
    )

    clinical_assessment = st.text_area(
        "Clinical Assessment",
        value=case_data.get(
            "clinical_assessment",
            ""
        ),
        placeholder="Enter the clinical assessment...",
        height=140,
        key="clinical_assessment_input",
    )

    save_case_value(
        "clinical_assessment",
        clinical_assessment
    )

    st.write("### Treatment / Management Plan")

    treatment_plan = st.text_area(
        "Treatment / Plan",
        value=case_data.get(
            "treatment_plan",
            ""
        ),
        placeholder=(
            "Enter medicines, investigations, advice, "
            "referrals or follow-up plan..."
        ),
        height=150,
        key="treatment_plan_input",
    )

    save_case_value(
        "treatment_plan",
        treatment_plan
    )

elif current_step == 7:

    st.subheader("7. Review")

    st.write(
        "Review the information entered in all sections "
        "before saving the case."
    )

    st.divider()
    with st.expander(
        "1. Chief Complaints",
        expanded=True
    ):

        st.write(
            "**Main Complaint:**",
            case_data.get(
                "chief_complaint",
                "Not entered"
            )
        )

        duration = case_data.get(
            "duration",
            0
        )

        duration_unit = case_data.get(
            "duration_unit",
            "Days"
        )

        st.write(
            f"**Duration:** {duration} {duration_unit}"
        )

        st.write(
            "**Additional Complaints:**",
            case_data.get(
                "additional_complaints",
                "Not entered"
            )
        )

        st.write(
            "**Severity:**",
            case_data.get(
                "severity",
                "Not selected"
            )
        )

        st.write(
            "**Additional Notes:**",
            case_data.get(
                "complaint_notes",
                "Not entered"
            )
        )

    with st.expander("2. History"):

        st.write(
            "**History of Present Illness:**",
            case_data.get(
                "history_present_illness",
                "Not entered"
            )
        )

        st.write(
            "**Onset:**",
            case_data.get(
                "onset",
                "Not selected"
            )
        )

        st.write(
            "**Course:**",
            case_data.get(
                "course",
                "Not selected"
            )
        )

        st.write(
            "**Associated Symptoms:**",
            case_data.get(
                "associated_symptoms",
                "Not entered"
            )
        )

        st.write(
            "**Aggravating Factors:**",
            case_data.get(
                "aggravating_factors",
                "Not entered"
            )
        )

        st.write(
            "**Relieving Factors:**",
            case_data.get(
                "relieving_factors",
                "Not entered"
            )
        )

        st.write(
            "**Previous Treatment:**",
            case_data.get(
                "previous_treatment",
                "Not entered"
            )
        )

    with st.expander("3. Past History"):

        st.write(
            "**Medical History:**",
            case_data.get(
                "past_medical_history",
                "Not entered"
            )
        )

        st.write(
            "**Surgical History:**",
            case_data.get(
                "past_surgical_history",
                "Not entered"
            )
        )

        st.write(
            "**Allergies:**",
            case_data.get(
                "allergies",
                "Not entered"
            )
        )

        st.write(
            "**Current Medications:**",
            case_data.get(
                "medications",
                "Not entered"
            )
        )

        st.write(
            "**Family History:**",
            case_data.get(
                "family_history",
                "Not entered"
            )
        )

        st.write(
            "**Hospitalization:**",
            case_data.get(
                "hospitalization_details",
                "Not entered"
            )
        )

    with st.expander("4. Personal History"):

        st.write(
            "**Diet:**",
            case_data.get(
                "diet",
                "Not entered"
            )
        )

        st.write(
            "**Appetite:**",
            case_data.get(
                "appetite",
                "Not selected"
            )
        )

        st.write(
            "**Sleep:**",
            case_data.get(
                "sleep",
                "Not selected"
            )
        )

        st.write(
            "**Bowel Habits:**",
            case_data.get(
                "bowel",
                "Not selected"
            )
        )

        st.write(
            "**Bladder Habits:**",
            case_data.get(
                "bladder",
                "Not selected"
            )
        )

        st.write(
            "**Exercise:**",
            case_data.get(
                "exercise",
                "Not entered"
            )
        )

        st.write(
            "**Smoking:**",
            case_data.get(
                "smoking",
                "Not selected"
            )
        )

        st.write(
            "**Alcohol Use:**",
            case_data.get(
                "alcohol",
                "Not selected"
            )
        )

        st.write(
            "**Additional Notes:**",
            case_data.get(
                "personal_notes",
                "Not entered"
            )
        )

    with st.expander("5. Examination"):

        st.write(
            "**Temperature:**",
            f"{case_data.get('temperature', 0)} °F"
        )

        st.write(
            "**Pulse:**",
            f"{case_data.get('pulse', 0)} bpm"
        )

        st.write(
            "**Respiratory Rate:**",
            f"{case_data.get('respiratory_rate', 0)} /min"
        )

        st.write(
            "**Blood Pressure:**",
            case_data.get(
                "blood_pressure",
                "Not entered"
            )
        )

        st.write(
            "**SpO₂:**",
            f"{case_data.get('spo2', 0)} %"
        )

        st.write(
            "**Weight:**",
            f"{case_data.get('weight', 0)} kg"
        )

        st.write(
            "**Height:**",
            f"{case_data.get('height', 0)} cm"
        )

        st.write(
            "**General Examination:**",
            case_data.get(
                "general_examination",
                "Not entered"
            )
        )

        st.write(
            "**Systemic Examination:**",
            case_data.get(
                "system_examination",
                "Not entered"
            )
        )

    with st.expander("6. Assessment"):

        st.write(
            "**Provisional Diagnosis:**",
            case_data.get(
                "provisional_diagnosis",
                "Not entered"
            )
        )

        st.write(
            "**Differential Diagnosis:**",
            case_data.get(
                "differential_diagnosis",
                "Not entered"
            )
        )

        st.write(
            "**Clinical Assessment:**",
            case_data.get(
                "clinical_assessment",
                "Not entered"
            )
        )

        st.write(
            "**Treatment / Plan:**",
            case_data.get(
                "treatment_plan",
                "Not entered"
            )
        )

    st.divider()

    st.warning(
        "Please verify all information carefully before saving."
    )

    if st.button(
        "Save Case",
        use_container_width=True
    ):

        if not case_data.get("patient_db_id"):
            st.error("Please select a patient before saving the case.")
        else:
            payload = dict(case_data)
            payload["patient_id"] = case_data["patient_db_id"]
            payload.pop("patient_db_id", None)
            payload.pop("patient_display", None)
            payload["case_date"] = date.today().isoformat()
            for _field in ["duration", "temperature", "pulse", "respiratory_rate", "spo2", "weight", "height"]:
                if _field in payload and payload[_field] is not None:
                    payload[_field] = str(payload[_field])
            try:
                saved = create_complete_case(payload)
                st.session_state["case_saved"] = True
                st.session_state["saved_case"] = saved
                st.success(f"Case {saved['case_id']} saved successfully to the database.")
                st.session_state["case_step"] = 1
                st.session_state["case_data"] = {}
            except RuntimeError as e:
                st.error(str(e))


st.divider()

col1, col2 = st.columns(2)


with col1:

    if current_step > 1:

        if st.button(
            "← Previous",
            use_container_width=True
        ):

            st.session_state["case_step"] -= 1
            st.rerun()

with col2:

    if current_step < len(steps):

        if st.button(
            "Next →",
            use_container_width=True
        ):

            st.session_state["case_step"] += 1
            st.rerun()
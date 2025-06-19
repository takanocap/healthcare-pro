
-- PATIENTS
-- =========================================
CREATE TABLE patients (
    patient_id UNIQUEIDENTIFIER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(20)
);

-- =========================================
-- CONTACT INFO
-- =========================================
CREATE TABLE contact_info (
    patient_id UNIQUEIDENTIFIER  PRIMARY KEY REFERENCES patients(patient_id),
    phone VARCHAR(100),
    email VARCHAR(100),
    street VARCHAR(100),
    city VARCHAR(100),
    [state] VARCHAR(100),
    zip VARCHAR(20)
);


-- =========================================
-- CHRONIC CONDITIONS
-- =========================================
CREATE TABLE chronic_conditions (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    condition VARCHAR(1000)
);


-- =========================================
-- PAST ILLNESSES
-- =========================================
CREATE TABLE past_illnesses (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    illness VARCHAR(100),
    age_at_diagnosis INTEGER,
	date_of_reporting DATE
);

-- =========================================
-- SURGERIES
-- =========================================
CREATE TABLE surgeries (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    surgery_name VARCHAR(1000),
    surgery_date DATE,
    -- Add more fields if needed
);

-- =========================================
-- HOSPITALIZATIONS
-- =========================================
CREATE TABLE hospitalizations (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    reason VARCHAR(1000),
    date_admitted DATE,
    date_discharged DATE
);

-- =========================================
-- MEDICATIONS
-- =========================================
CREATE TABLE medications (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    name VARCHAR(100),
    dose VARCHAR(100),
    frequency VARCHAR(100),
    start_date DATE,
	end_date Date null,
	reason varchar(1000) null
);

-- =========================================
-- ALLERGIES
-- =========================================
CREATE TABLE allergies (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    substance VARCHAR(100),
    reaction VARCHAR(100),
    severity VARCHAR(100)
);

-- =========================================
-- FAMILY HISTORY
-- =========================================
CREATE TABLE family_history (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    relation VARCHAR(100),
    condition VARCHAR(100),
    age_at_diagnosis INTEGER
);

-- =========================================
-- SOCIAL HISTORY
-- =========================================
CREATE TABLE social_history (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    smoking_status VARCHAR(100),
    alcohol_use VARCHAR(100),
    occupation VARCHAR(100),
    exercise_habits VARCHAR(100)
);


-- =========================================
-- IMMUNIZATIONS
-- =========================================
CREATE TABLE immunizations (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    vaccine VARCHAR(100),
    date DATE
);

-- =========================================
-- REVIEW OF SYSTEMS
-- =========================================
CREATE TABLE review_of_systems (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    general TEXT,
    cardiovascular TEXT,
    respiratory TEXT,
    neurological TEXT,
	date DATE
);


-- =========================================
-- CLINICAL NOTES
-- =========================================
CREATE TABLE notes (
	id UNIQUEIDENTIFIER PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    date DATE,
    author VARCHAR(100),
    content TEXT
);

CREATE TABLE patient_reviews (
    review_id UNIQUEIDENTIFIER  PRIMARY KEY,
    patient_id UNIQUEIDENTIFIER  REFERENCES patients(patient_id),
    interaction_datetime Datetime DEFAULT CURRENT_TIMESTAMP,
    prompt_index INTEGER,
    prompt TEXT,
    assistance TEXT,
    analysis_report TEXT,
    summary_report TEXT,
    severity VARCHAR(20)  -- e.g., "low", "medium", "high"
);
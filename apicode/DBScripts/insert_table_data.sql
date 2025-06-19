-- =========================================
-- PATIENTS
-- =========================================
INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, gender) VALUES
('11111111-1111-1111-1111-111111111111', 'John', 'Smith', '1975-03-12', 'Male'),
('22222222-2222-2222-2222-222222222222', 'Jane', 'Doe', '1982-06-25', 'Female'),
('33333333-3333-3333-3333-333333333333', 'Alice', 'Brown', '1990-11-02', 'Female'),
('44444444-4444-4444-4444-444444444444', 'Bob', 'Taylor', '1968-08-17', 'Male'),
('55555555-5555-5555-5555-555555555555', 'Mike', 'Wilson', '1970-04-29', 'Male'),
('66666666-6666-6666-6666-666666666666', 'Sara', 'Davis', '1985-01-15', 'Female'),
('77777777-7777-7777-7777-777777777777', 'Tom', 'Evans', '1992-10-09', 'Male'),
('88888888-8888-8888-8888-888888888888', 'Laura', 'White', '1959-12-01', 'Female'),
('99999999-9999-9999-9999-999999999999', 'Chris', 'King', '1978-07-22', 'Male'),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Emma', 'Scott', '1988-09-05', 'Female');

-- =========================================
-- CONTACT INFO
-- =========================================
INSERT INTO contact_info (patient_id, phone, email, street, city, state, zip) VALUES
('11111111-1111-1111-1111-111111111111', '555-1234', 'john@example.com', '123 Elm St', 'Springfield', 'IL', '62701'),
('22222222-2222-2222-2222-222222222222', '555-2345', 'jane@example.com', '456 Oak St', 'Springfield', 'IL', '62702'),
('33333333-3333-3333-3333-333333333333', '555-3456', 'alice@example.com', '789 Pine St', 'Springfield', 'IL', '62703'),
('44444444-4444-4444-4444-444444444444', '555-4567', 'bob@example.com', '101 Maple St', 'Springfield', 'IL', '62704'),
('55555555-5555-5555-5555-555555555555', '555-5678', 'mike@example.com', '202 Birch St', 'Springfield', 'IL', '62705'),
('66666666-6666-6666-6666-666666666666', '555-6789', 'sara@example.com', '303 Cedar St', 'Springfield', 'IL', '62706'),
('77777777-7777-7777-7777-777777777777', '555-7890', 'tom@example.com', '404 Walnut St', 'Springfield', 'IL', '62707'),
('88888888-8888-8888-8888-888888888888', '555-8901', 'laura@example.com', '505 Chestnut St', 'Springfield', 'IL', '62708'),
('99999999-9999-9999-9999-999999999999', '555-9012', 'chris@example.com', '606 Poplar St', 'Springfield', 'IL', '62709'),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '555-0123', 'emma@example.com', '707 Spruce St', 'Springfield', 'IL', '62710');

-- =========================================
-- CHRONIC CONDITIONS
-- =========================================
INSERT INTO chronic_conditions (id, patient_id, condition) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Diabetes'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Heart disease'),
(NEWID(),'33333333-3333-3333-3333-333333333333', 'Hypertension'),
(NEWID(),'44444444-4444-4444-4444-444444444444', 'COPD'),
(NEWID(),'55555555-5555-5555-5555-555555555555', 'Arthritis'),
(NEWID(),'66666666-6666-6666-6666-666666666666', 'Asthma'),
(NEWID(),'77777777-7777-7777-7777-777777777777', 'Chronic kidney disease'),
(NEWID(),'88888888-8888-8888-8888-888888888888', 'Depression'),
(NEWID(),'99999999-9999-9999-9999-999999999999', 'Bipolar disorder'),
(NEWID(),'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Diabetes');

-- =========================================
-- PAST ILLNESSES
-- =========================================
INSERT INTO past_illnesses (id, patient_id, illness, age_at_diagnosis, date_of_reporting) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Flu', 30, '20190506'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Bronchitis', 35, '20190506'),
(NEWID(),'33333333-3333-3333-3333-333333333333', 'Chickenpox', 12, '20190506'),
(NEWID(),'44444444-4444-4444-4444-444444444444', 'Anemia', 40, '20190506'),
(NEWID(),'55555555-5555-5555-5555-555555555555', 'Migraines', 25, '20190506'),
(NEWID(),'66666666-6666-6666-6666-666666666666', 'Allergies', 18, '20190506'),
(NEWID(),'77777777-7777-7777-7777-777777777777', 'Flu', 20, '20190506'),
(NEWID(),'88888888-8888-8888-8888-888888888888', 'UTI', 28, '20190506'),
(NEWID(),'99999999-9999-9999-9999-999999999999', 'Asthma', 10, '20190506'),
(NEWID(),'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'GERD', 33, '20190506');

-- =========================================
-- SURGERIES
-- =========================================
INSERT INTO surgeries (id, patient_id, surgery_name, surgery_date) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Appendectomy', '2005-06-01'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Heart Bypass', '2018-09-10'),
(NEWID(),'33333333-3333-3333-3333-333333333333', 'Tonsillectomy', '1998-07-15');

-- =========================================
-- HOSPITALIZATIONS
-- =========================================
INSERT INTO hospitalizations (id, patient_id, reason, date_admitted, date_discharged) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Diabetes Complications', '2020-03-01', '2020-03-10'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Heart Attack', '2019-05-15', '2019-05-25');

-- =========================================
-- MEDICATIONS
-- =========================================
INSERT INTO medications (id, patient_id, name, dose, frequency, start_date) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Metformin', '500mg', 'Twice a day', '2015-01-01'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Atorvastatin', '20mg', 'Once daily', '2017-03-10');

-- =========================================
-- ALLERGIES
-- =========================================
INSERT INTO allergies (id, patient_id, substance, reaction, severity) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Peanuts', 'Anaphylaxis', 'Severe'),
(NEWID(),'33333333-3333-3333-3333-333333333333', 'Penicillin', 'Rash', 'Moderate'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Penicillin', 'Rash', 'Moderate');

-- =========================================
-- FAMILY HISTORY
-- =========================================
INSERT INTO family_history (id, patient_id, relation, condition, age_at_diagnosis) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Father', 'Diabetes', 55),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Mother', 'Heart disease', 60);

-- =========================================
-- SOCIAL HISTORY
-- =========================================
INSERT INTO social_history (id, patient_id, smoking_status, alcohol_use, occupation, exercise_habits) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Never', 'Occasional', 'Engineer', 'Regular'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Former', 'Frequent', 'Teacher', 'None');

-- =========================================
-- IMMUNIZATIONS
-- =========================================
INSERT INTO immunizations (id, patient_id, vaccine, date) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'Influenza', '2023-10-01'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'COVID-19 Booster', '2024-01-15');

-- =========================================
-- REVIEW OF SYSTEMS
-- =========================================
INSERT INTO review_of_systems (id, patient_id, general, cardiovascular, respiratory, neurological, date) VALUES
(NEWID(),'11111111-1111-1111-1111-111111111111', 'No fatigue', 'No chest pain', 'Mild wheezing', 'Normal', '2023-10-01'),
(NEWID(),'22222222-2222-2222-2222-222222222222', 'Weight loss', 'Palpitations', 'Shortness of breath', 'Dizziness', '2024-01-15');

-- =========================================
-- CLINICAL NOTES
-- =========================================
INSERT INTO notes (id, patient_id, date, author, content) VALUES
(NEWID(), '11111111-1111-1111-1111-111111111111', '2024-06-01', 'Dr. Adams', 'Patient doing well on Metformin. Blood sugar stable.'),
(NEWID(), '22222222-2222-2222-2222-222222222222', '2024-06-01', 'Dr. Brown', 'Heart condition stable. Monitor cholesterol.');

-- =========================================
-- PATIENT REVIEWS
-- =========================================
INSERT INTO patient_reviews (
    review_id, patient_id, interaction_datetime, prompt_index, prompt, assistance, analysis_report, summary_report, severity
) VALUES
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', CURRENT_TIMESTAMP, 1, 'How is the diabetes management?', 'Suggested dietary change', 'A1C stable', 'Continue current plan', 'low'),
('cccccccc-cccc-cccc-cccc-cccccccccccc', '22222222-2222-2222-2222-222222222222', CURRENT_TIMESTAMP, 2, 'Assess heart disease risk', 'Medication adjusted', 'Cholesterol high', 'Monitor monthly', 'medium');

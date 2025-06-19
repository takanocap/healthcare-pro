from datetime import datetime
import models
import schemas
from sqlalchemy.orm import Session
from models import Patient, ContactInfo, FamilyHistory, SocialHistory, ChronicConditions as ChronicCond, PastIllnesses, Surgeries
from models import Hospitalizations, Medications, Allergies, Immunizations,  ReviewOfSystems, Notes
from schemas import PatientCreate
import uuid

def create_patient(db: Session, patient: PatientCreate):
    new_patient = Patient(
        patient_id=uuid.uuid4(),
        first_name=patient.first_name,
        last_name=patient.last_name,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender
    )
    db.add(new_patient)
    db.flush()  # ensure patient_id is available

    if patient.contact_info:
        contact = ContactInfo(
            patient_id=new_patient.patient_id,
            phone=patient.contact_info.phone,
            email=patient.contact_info.email,
            street=patient.contact_info.street,
            city=patient.contact_info.city,
            state=patient.contact_info.state,
            zip=patient.contact_info.zip
        )
        db.add(contact)

    for item in patient.family_history:
        fh = FamilyHistory(
            patient_id=new_patient.patient_id,
            relation=item.relation,
            condition=item.condition,
            age_at_diagnosis=item.age_at_diagnosis
        )
        db.add(fh)
    
    for item in patient.social_history:
        sh = SocialHistory(
            patient_id=new_patient.patient_id,
            smoking_status=item.smoking_status,
            alcohol_use=item.alcohol_use,
            occupation=item.occupation,
            exercise_habits=item.exercise_habits
        )
        db.add(sh)
        
    for item in patient.chronic_conditions:
        ch = ChronicCond(
            patient_id=new_patient.patient_id,
            condition=item.condition
        )
        db.add(ch)
        
    for item in patient.past_illnesses:
        pl = PastIllnesses(
            patient_id=new_patient.patient_id,
            illness=item.illness,
            age_at_diagnosis=item.age_at_diagnosis,
            date_of_reporting = item.date_of_reporting
        )
        db.add(pl)
        
    for item in patient.surgeries:
        sur = Surgeries(
            patient_id=new_patient.patient_id,
            surgery_name=item.surgery_name,
            surgery_date=item.surgery_date
        )
        db.add(sur)
        
    for item in patient.hospitalizations:
        hos = Hospitalizations(
            patient_id=new_patient.patient_id,
            reason=item.reason,
            date_admitted=item.date_admitted,
            date_discharged=item.date_discharged
        )
        db.add(hos)
        
    for item in patient.medications:
        med = Medications(
            patient_id=new_patient.patient_id,
            name=item.name,
            dose=item.dose,
            frequency=item.frequency,
            start_date=item.start_date,
            end_date=item.end_date,
            reason=item.reason
        )
        db.add(med)
        
    for item in patient.allergies:
        allg = Allergies(
            patient_id=new_patient.patient_id,
            substance=item.substance,
            reaction=item.reaction,
            severity=item.severity
        )
        db.add(allg)

    for item in patient.immunizations:
        imm = Immunizations(
            patient_id=new_patient.patient_id,
            vaccine=item.vaccine,
            date=item.date
        )
        db.add(imm)
     
     
    for item in patient.review_of_systems:
        ros = ReviewOfSystems(
            patient_id=new_patient.patient_id,
            general=item.general,
            cardiovascular=item.cardiovascular,
            respiratory=item.respiratory,
            neurological=item.neurological,
            date=item.date
        )
        db.add(ros)
    
    
    for item in patient.notes:
        note = Notes(
            patient_id=new_patient.patient_id,
            date=item.date,
            author=item.author,
            content=item.content
        )
        db.add(note)

    db.commit()
    db.refresh(new_patient)
    return new_patient

def get_all_patients(db: Session):
    return db.query(Patient).all()

def get_patient_by_id(db: Session, patient_id: str):
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()

def create_patient_review(db: Session, review: schemas.PatientReviewCreate):
    new_review = models.PatientReview(
        review_id=uuid.uuid4(),
        interaction_datetime=datetime.utcnow(),
        **review.dict()
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_patient_reviews(db: Session):
    return db.query(models.PatientReview).all()

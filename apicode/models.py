from datetime import datetime
from sqlalchemy import Column, String, Date, ForeignKey, Integer
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    gender = Column(String(20))
    contact_info = relationship("ContactInfo", back_populates="patient", uselist=False, cascade="all, delete-orphan")
    family_history = relationship("FamilyHistory", back_populates="patient", cascade="all, delete-orphan")
    social_history = relationship("SocialHistory", back_populates="patient", cascade="all, delete-orphan")
    chronic_conditions = relationship("ChronicConditions", back_populates="patient", cascade="all, delete-orphan")
    past_illnesses = relationship("PastIllnesses", back_populates="patient", cascade="all, delete-orphan")
    surgeries = relationship("Surgeries", back_populates="patient", cascade="all, delete-orphan")
    hospitalizations = relationship("Hospitalizations", back_populates="patient", cascade="all, delete-orphan") 
    medications = relationship("Medications", back_populates="patient", cascade="all, delete-orphan")
    allergies = relationship("Allergies", back_populates="patient", cascade="all, delete-orphan")   
    immunizations = relationship("Immunizations", back_populates="patient", cascade="all, delete-orphan")
    review_of_systems = relationship("ReviewOfSystems", back_populates="patient", cascade="all, delete-orphan")
    notes = relationship("Notes", back_populates="patient", cascade="all, delete-orphan")


class ContactInfo(Base):
    __tablename__ = "contact_info"
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"), primary_key=True)
    phone = Column(String(100))
    email = Column(String(100))
    street = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    zip = Column(String(20))
    patient = relationship("Patient", back_populates="contact_info")

class FamilyHistory(Base):
    __tablename__ = "family_history"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    relation = Column(String(100))
    condition = Column(String(100))
    age_at_diagnosis = Column(Integer)
    patient = relationship("Patient", back_populates="family_history")
    
class SocialHistory(Base):
    __tablename__ = "social_history"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    smoking_status = Column(String(100))
    alcohol_use = Column(String(100))
    occupation = Column(String(100))
    exercise_habits = Column(String(100))
    patient = relationship("Patient", back_populates="social_history")

class ChronicConditions(Base):
    __tablename__ = "chronic_conditions"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    condition = Column(String(1000))
    patient = relationship("Patient", back_populates="chronic_conditions")

class PastIllnesses(Base):
    __tablename__ = "past_illnesses"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    illness = Column(String(100))
    age_at_diagnosis = Column(Integer)
    date_of_reporting = Column(Date)
    patient = relationship("Patient", back_populates="past_illnesses")
    
class Surgeries(Base):
    __tablename__ = "surgeries"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    surgery_name = Column(String(100))
    surgery_date = Column(Date)
    patient = relationship("Patient", back_populates="surgeries")
    
class Hospitalizations(Base):
    __tablename__ = "hospitalizations"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    reason = Column(String(100))
    date_admitted = Column(Date)
    date_discharged = Column(Date)
    patient = relationship("Patient", back_populates="hospitalizations")
    
class Medications(Base):
    __tablename__ = "medications"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    name = Column(String(100))
    dose = Column(String(100))
    frequency = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    reason = Column(String(100), nullable=True)
    patient = relationship("Patient", back_populates="medications")
    
class Allergies(Base):
    __tablename__ = "allergies"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    substance = Column(String(100))
    reaction = Column(String(100))
    severity = Column(String(20))
    patient = relationship("Patient", back_populates="allergies")
    
class Immunizations(Base):
    __tablename__ = "immunizations"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    vaccine = Column(String(100))
    date = Column(Date)
    patient = relationship("Patient", back_populates="immunizations")

   
class ReviewOfSystems(Base):
    __tablename__ = "review_of_systems"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    general = Column(String(1000))
    cardiovascular = Column(String(1000))
    respiratory = Column(String(1000))
    neurological = Column(String(1000))
    date = Column(Date)
    patient = relationship("Patient", back_populates="review_of_systems")


class Notes(Base):
    __tablename__ = "notes"
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    date = Column(Date)
    author = Column(String(100))
    content = Column(String(1000))
    patient = relationship("Patient", back_populates="notes")
    
####    
class PatientReview(Base):
    __tablename__ = "patient_reviews"

    review_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    patient_id = Column(UNIQUEIDENTIFIER, ForeignKey("patients.patient_id"))
    interaction_datetime = Column(Date, default=datetime.utcnow)
    prompt_index = Column(Integer)
    prompt = Column(String)
    assistance = Column(String)
    analysis_report = Column(String)
    summary_report = Column(String)
    severity = Column(String(20))

    patient = relationship("Patient", backref="patient_reviews")
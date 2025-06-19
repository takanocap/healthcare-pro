from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import date

class ContactInfoSchema(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    class Config:
        orm_mode = True

class FamilyHistorySchema(BaseModel):
    relation: str
    condition: str
    age_at_diagnosis: int
    class Config:
        orm_mode = True

class SocialHistorySchema(BaseModel):
    smoking_status: Optional[str]
    alcohol_use: Optional[str]
    occupation: Optional[str]
    exercise_habits: Optional[str]
    class Config:
        orm_mode = True        

class ChronicConditionsSchema(BaseModel):
    condition: str
    class Config:
        orm_mode = True
        
class PastIllnessesSchema(BaseModel):
    illness: str
    age_at_diagnosis: int
    date_of_reporting: date
    class Config:
        orm_mode = True
        
class SurgeriesSchema(BaseModel):
    surgery_name: str
    surgery_date: date
    class Config:
        orm_mode = True
        
class HospitalizationsSchema(BaseModel):
    reason: str
    date_admitted: date
    date_discharged: date
    class Config:
        orm_mode = True
        
class MedicationsSchema(BaseModel):
    name: str
    dose: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    reason: Optional[str] = None
    class Config:
        orm_mode = True
        
class AllergiesSchema(BaseModel):
    substance: str
    reaction: str
    severity: str
    class Config:
        orm_mode = True

class ImmunizationsSchema(BaseModel):
    vaccine: str
    date: date
    class Config:
        orm_mode = True

class ReviewOfSystemsSchema(BaseModel):
    general: str
    cardiovascular: str
    respiratory: str
    neurological: str
    date: date

    class Config:
        orm_mode = True

class NotesSchema(BaseModel):
    date: date
    author: str
    content: str
    class Config:
        orm_mode = True

### add here

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    contact_info: Optional[ContactInfoSchema]
    family_history: Optional[List[FamilyHistorySchema]] = []
    social_history: Optional[List[SocialHistorySchema]] = []
    chronic_conditions: Optional[List[ChronicConditionsSchema]] = []
    past_illnesses: Optional[List[PastIllnessesSchema]] = []
    surgeries: Optional[List[SurgeriesSchema]] = []
    hospitalizations: Optional[List[HospitalizationsSchema]] = []
    medications: Optional[List[MedicationsSchema]] = []
    allergies: Optional[List[AllergiesSchema]] = []
    immunizations: Optional[List[ImmunizationsSchema]] = []
    review_of_systems : Optional[List[ReviewOfSystemsSchema]] = []
    notes: Optional[List[NotesSchema]] = []

class PatientResponse(BaseModel):
    patient_id: UUID
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    contact_info: Optional[ContactInfoSchema]
    family_history: List[FamilyHistorySchema] = []
    social_history: List[SocialHistorySchema] = []
    chronic_conditions: Optional[List[ChronicConditionsSchema]] = []
    past_illnesses: Optional[List[PastIllnessesSchema]] = []
    surgeries: Optional[List[SurgeriesSchema]] = []
    hospitalizations: Optional[List[HospitalizationsSchema]] = []
    medications: Optional[List[MedicationsSchema]] = []
    allergies: Optional[List[AllergiesSchema]] = []
    immunizations: Optional[List[ImmunizationsSchema]] = []
    review_of_systems : Optional[List[ReviewOfSystemsSchema]] = []
    notes: Optional[List[NotesSchema]] = []
    class Config:
        orm_mode = True



#####
class PatientReviewCreate(BaseModel):
    patient_id: UUID
    prompt_index: int
    prompt: str
    assistance: str
    analysis_report: str
    summary_report: str
    severity: str
    
class PatientReviewResponse(PatientReviewCreate):
    review_id: UUID
    interaction_datetime: datetime

    class Config:
        orm_mode = True
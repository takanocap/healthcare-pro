from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models, schemas, crud
from uuid import UUID
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class LoginRequest(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str

class LoginResponse(BaseModel):
    patient_id: str
    
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=LoginResponse)
def login_patient(request: LoginRequest, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(
        models.Patient.first_name == request.first_name,
        models.Patient.last_name == request.last_name,
        models.Patient.date_of_birth == request.date_of_birth
    ).first()

    if not patient:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"patient_id": str(patient.patient_id)}

@app.post("/patients/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.get("/patients/", response_model=List[schemas.PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    return crud.get_all_patients(db)

@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient_by_id(patient_id: UUID, db: Session = Depends(get_db)):
    patient = crud.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/reviews/", response_model=schemas.PatientReviewResponse)
def create_review(review: schemas.PatientReviewCreate, db: Session = Depends(get_db)):
    return crud.create_patient_review(db, review)

# GET /reviews/{id}
@app.get("/reviews/{id}", response_model=schemas.PatientReviewResponse)
def get_review_by_id(id: str, db: Session = Depends(get_db)):
    review = db.query(models.PatientReview).filter(models.PatientReview.review_id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@app.get("/reviews/", response_model=List[schemas.PatientReviewResponse])
def list_reviews(db: Session = Depends(get_db)):
    return crud.get_patient_reviews(db)

@app.get("/patients/{patient_id}/reviews/{id}", response_model=schemas.PatientReviewResponse)
def get_review_by_id(patient_id: str, id: str, db: Session = Depends(get_db)):
    review = (
        db.query(models.PatientReview)
        .filter(models.PatientReview.review_id == id, models.PatientReview.patient_id == patient_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@app.get("/patients/{patient_id}/reviews", response_model=list[schemas.PatientReviewResponse])
def get_reviews_for_patient(patient_id: str, db: Session = Depends(get_db)):
    # Optional: validate patient exists
    patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    reviews = db.query(models.PatientReview).filter(models.PatientReview.patient_id == patient_id).all()
    return reviews
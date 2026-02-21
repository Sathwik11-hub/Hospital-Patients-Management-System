from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import backend.database_models as models
from backend.database import SessionLocal, engine
from backend.models import PatientCreate, PatientResponse

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- GET ALL ----------------
@app.get("/patients", response_model=list[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).order_by(models.Patient.id).all()

# ---------------- GET ONE ----------------
@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient_by_id(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ---------------- CREATE ----------------
@app.post("/patients", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    data = patient.model_dump()

    # ensure phone stored as int safely
    data["phone"] = int(data["phone"])

    new_patient = models.Patient(**data)

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

# ---------------- UPDATE ----------------
@app.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)):

    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    data = patient.model_dump()
    data["phone"] = int(data["phone"])

    for key, value in data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)

    return db_patient

# ---------------- DELETE ----------------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):

    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()

    return {"message": "Patient deleted successfully"}

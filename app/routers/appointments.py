from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..main import get_current_user

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/", response_model=list[schemas.AppointmentOut])
def read_appointments(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    appointments = db.query(models.Appointment).filter(models.Appointment.user_id == current_user.id).all()
    return appointments

@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    # Additional checks for mentor availability can be added here
    try:
        db_appointment = crud.create_appointment(db, appointment, current_user.id)
        # Optionally integrate video link generation here
        return db_appointment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Implement PUT and DELETE similarly

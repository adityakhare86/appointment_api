from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, is_mentor=user.is_mentor)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_appointment(db: Session, appointment: schemas.AppointmentCreate, user_id: int):
    # Check for overlapping appointments
    overlapping = db.query(models.Appointment).filter(
        models.Appointment.mentor_id == appointment.mentor_id,
        models.Appointment.start_time < appointment.end_time,
        models.Appointment.end_time > appointment.start_time
    ).first()
    if overlapping:
        raise Exception("Time slot is already booked.")
    
    db_appointment = models.Appointment(
        user_id=user_id,
        mentor_id=appointment.mentor_id,
        start_time=appointment.start_time,
        end_time=appointment.end_time
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# Add more CRUD functions as needed...

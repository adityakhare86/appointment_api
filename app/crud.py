from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime
import uuid

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

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta):
    from jose import jwt
    import os
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session, email: str):
    return get_user_by_email(db, email)

def create_appointment(db: Session, appointment: schemas.AppointmentCreate, user_id: int):
    overlapping = db.query(models.Appointment).filter(
        models.Appointment.mentor_id == appointment.mentor_id,
        models.Appointment.start_time < appointment.end_time,
        models.Appointment.end_time > appointment.start_time
    ).first()
    if overlapping:
        raise Exception("Time slot is already booked.")
    video_link = generate_video_link()
    db_appointment = models.Appointment(
        user_id=user_id,
        mentor_id=appointment.mentor_id,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        video_link=video_link
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session, user_id: int):
    return db.query(models.Appointment).filter(models.Appointment.user_id == user_id).all()

def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentCreate, user_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id, models.Appointment.user_id == user_id).first()
    if not db_appointment:
        raise Exception("Appointment not found.")
    overlapping = db.query(models.Appointment).filter(
        models.Appointment.mentor_id == appointment.mentor_id,
        models.Appointment.start_time < appointment.end_time,
        models.Appointment.end_time > appointment.start_time,
        models.Appointment.id != appointment_id
    ).first()
    if overlapping:
        raise Exception("Time slot is already booked.")
    db_appointment.mentor_id = appointment.mentor_id
    db_appointment.start_time = appointment.start_time
    db_appointment.end_time = appointment.end_time
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int, user_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id, models.Appointment.user_id == user_id).first()
    if not db_appointment:
        raise Exception("Appointment not found.")
    db.delete(db_appointment)
    db.commit()
    return

def set_availability(db: Session, availability: schemas.AvailabilityCreate, mentor_id: int):
    db_availability = models.MentorAvailability(
        mentor_id=mentor_id,
        start_time=availability.start_time,
        end_time=availability.end_time
    )
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

def get_availability(db: Session, mentor_id: int):
    return db.query(models.MentorAvailability).filter(models.MentorAvailability.mentor_id == mentor_id).all()

def generate_video_link():
    room_name = str(uuid.uuid4())
    return f"https://meet.jit.si/{room_name}"

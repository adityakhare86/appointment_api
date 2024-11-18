from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..main import get_current_user

router = APIRouter(
    prefix="/mentors",
    tags=["mentors"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/availability", response_model=schemas.AvailabilityOut)
def set_availability(availability: schemas.AvailabilityCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_mentor:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_availability = models.MentorAvailability(
        mentor_id=current_user.id,
        start_time=availability.start_time,
        end_time=availability.end_time
    )
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

@router.get("/availability", response_model=list[schemas.AvailabilityOut])
def get_availability(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_mentor:
        raise HTTPException(status_code=403, detail="Not authorized")
    availability = db.query(models.MentorAvailability).filter(models.MentorAvailability.mentor_id == current_user.id).all()
    return availability

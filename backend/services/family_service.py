from backend.database import SessionLocal
from datetime import datetime,UTC
from fastapi import HTTPException

from backend.models.family import Family
from backend.utils.family_code_generator import generate_family_code

def add_family(username):
    db = SessionLocal()
    try:
        db_family = Family(
            family_name="family_" + username,
            family_code=generate_family_code(),
            created_at=datetime.now(UTC),
        )
        db.add(db_family)
        db.commit()
        db.refresh(db_family)
        return db_family
    finally:
        db.close()

def get_family(family_code):
    db = SessionLocal()
    try:
        db_family = db.query(Family).filter_by(family_code=family_code).first()
        if not db_family:
            raise HTTPException(status_code=404, detail="Family not found")
        return db_family
    finally:
        db.close()
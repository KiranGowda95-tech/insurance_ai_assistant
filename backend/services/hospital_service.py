from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Hospital

def get_hospital_by_id(hospital_id:str):

    db=SessionLocal()

    try:
        statement=select(Hospital).where(
            Hospital.hospital_id==hospital_id
        )

        result=db.execute(statement)

        hospital=result.scalar_one_or_none()

        if not hospital:
            return None

        return {
            "hospital_id": hospital.hospital_id,
            "hospital_name": hospital.hospital_name,
            "city": hospital.city,
            "network_status": hospital.network_status,
            "specialty": hospital.specialty,
        }

    finally:
        db.close()
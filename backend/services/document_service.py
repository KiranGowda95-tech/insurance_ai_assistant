from sqlalchemy import select

from database.connection import SessionLocal
from database.models import ClaimDocument

def get_claim_documents(claim_id:str):

    db=SessionLocal()

    try:
        statement=select(ClaimDocument).where(
            ClaimDocument.claim_id == claim_id
        )

        result=db.execute(statement)

        documents=result.scalars().all

        return [
            {
                "claim_id":document.claim_id,
                "document_type":document.document_type,
                "upload_status":document.upload_status,
                "verification_status":document.verification_status,
                "file_type":document.file_type
            }

            for document in documents
        ]
    finally:
        db.close()

def get_missing_documents(claim_id:str):

    db=SessionLocal()

    try:
        statement=select(ClaimDocument).where(
            ClaimDocument.claim_id==claim_id,
            ClaimDocument.upload_status=="Missing"
        )

        result=db.execute(statement)

        documents=result.scalars().all()

        return [
            {
                "document_type":document.document_type,
                "upload_status":document.upload_status,
                "verification_status":document.verification_status
            }
            for document in documents
        ]

    finally:
        db.close()
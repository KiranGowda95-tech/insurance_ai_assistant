from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Claim

def get_claim_by_id(claim_id:str):

    db=SessionLocal()

    try:
        statement=select(Claim).where(
            Claim.claim_id==claim_id
        )

        result=db.execute(statement)

        claim=result.scalar_one_or_none()

        if not claim:
            return None

        return {
            "claim_id": claim.claim_id,
            "customer_id": claim.customer_id,
            "policy_id": claim.policy_id,
            "policy_type": claim.policy_type,
            "claim_date": str(claim.claim_date),
            "claim_amount": claim.claim_amount,
            "claim_status": claim.claim_status,
            "approved_amount": claim.approved_amount,
            "diagnosis_or_loss_type": claim.diagnosis_or_loss_type,
            "hospital_id": claim.hospital_id,
            "fraud_risk_score": claim.fraud_risk_score,
            "manual_review_flag": claim.manual_review_flag,
            "rejection_or_adjustment_reason":
                claim.rejection_or_adjustment_reason,
        }

    finally:
        db.close()
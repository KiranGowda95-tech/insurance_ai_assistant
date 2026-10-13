from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Claim, Policy, ClaimDocument, Hospital


def analyze_claim(claim_id: str):
    """Retrieve structured claim, policy, document, and hospital data."""

    claim_id = claim_id.strip()
    db = SessionLocal()

    try:
        # 1. Retrieve the claim.
        claim_statement = select(Claim).where(
            Claim.claim_id == claim_id
        )
        claim = db.execute(claim_statement).scalar_one_or_none()

        if claim is None:
            return None

        # 2. Retrieve the associated policy.
        policy_statement = select(Policy).where(
            Policy.policy_id == claim.policy_id
        )
        policy = db.execute(policy_statement).scalar_one_or_none()

        # 3. Retrieve all documents associated with this claim.
        document_statement = select(ClaimDocument).where(
            ClaimDocument.claim_id == claim_id
        )
        documents = db.execute(document_statement).scalars().all()

        missing_documents = [
            doc.document_type
            for doc in documents
            if (doc.upload_status or "").strip().lower() == "missing"
        ]

        pending_documents = [
            doc.document_type
            for doc in documents
            if (doc.verification_status or "").strip().lower() == "pending"
        ]

        verified_documents = [
            doc.document_type
            for doc in documents
            if (doc.verification_status or "").strip().lower() == "verified"
        ]

        # 4. Retrieve the hospital when an ID is recorded.
        hospital = None

        if claim.hospital_id:
            hospital_statement = select(Hospital).where(
                Hospital.hospital_id == claim.hospital_id
            )
            hospital = db.execute(
                hospital_statement
            ).scalar_one_or_none()

        # 5. Return structured evidence, even if the hospital is absent.
        return {
            "found": True,
            "claim": {
                "claim_id": claim.claim_id,
                "customer_id": claim.customer_id,
                "policy_id": claim.policy_id,
                "claim_status": claim.claim_status,
                "claim_amount": claim.claim_amount,
                "approved_amount": claim.approved_amount,
                "diagnosis_or_loss_type": claim.diagnosis_or_loss_type,
                "fraud_risk_score": claim.fraud_risk_score,
                "manual_review_flag": claim.manual_review_flag,
                "rejection_or_adjustment_reason":
                    claim.rejection_or_adjustment_reason,
                "hospital_id": claim.hospital_id,
            },
            "policy": (
                {
                    "policy_id": policy.policy_id,
                    "product_name": policy.product_name,
                    "policy_type": policy.policy_type,
                    "policy_status": policy.policy_status,
                    "sum_insured": policy.sum_insured,
                    "annual_premium": policy.annual_premium,
                    "co_pay_pct": policy.co_pay_pct,
                    "deductible": policy.deductible,
                    "waiting_period_days": policy.waiting_period_days,
                }
                if policy is not None
                else None
            ),
            "documents": {
                "total": len(documents),
                "missing": missing_documents,
                "pending_verification": pending_documents,
                "verified": verified_documents,
            },
            "hospital": (
                {
                    "hospital_id": hospital.hospital_id,
                    "hospital_name": hospital.hospital_name,
                    "city": hospital.city,
                    "network_status": hospital.network_status,
                    "specialty": hospital.specialty,
                }
                if hospital is not None
                else None
            ),
        }

    finally:
        db.close()

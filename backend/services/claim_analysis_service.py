from sqlalchemy import select

from database.connection import SessionLocal
from database.models import (
    Claim,
    Policy,
    ClaimDocument,
    Hospital,
)

def analyze_claim(claim_id:str):

    db=SessionLocal()

    try:
        #We get claim details  
        claim_statement=select(Claim).where(
            Claim.claim_id==claim_id
        )

        claim_result=db.execute(claim_statement)

        claim=claim_result.scalar_one_or_none()

        if not claim:
            return None

        #gets policy
        policy_statement=select(Policy).where(
            Policy.policy_id==claim.policy_id
        )

        policy_result=db.execute(policy_statement)

        policy=policy_result.scalar_one_or_none()

        #Gets Document
        document_statement=select(ClaimDocument).where(
            ClaimDocument.claim_id==claim_id
        )

        document_result=db.execute(document_statement)

        documents=document_result.scalars().all()


        #Get Hospital
        hospital=None

        if claim.hospital_id:

            hospital_statement=select(Hospital).where(
                Hospital.hospital_id==claim.hospital_id
            )

            hospital_result=db.execute(
                hospital_statement
            )

            hospital=hospital_result.scalar_one_or_none()

            #Analying the document
            missing_documents=[
                document.document_type
                for document in documents
                if document.upload_status=="Missing"
            ]

            pending_documents=[
                document.document_type
                for document in documents
                if document.verification_status=="Pending"
            ]

            verified_documents=[
                document.document_type
                for document in documents
                if document.verification_status=="Verified"
            ]

            #response
            return {
                "claim":{
                     "claim_id": claim.claim_id,
                "customer_id": claim.customer_id,
                "policy_id": claim.policy_id,
                "claim_status": claim.claim_status,
                "claim_amount": claim.claim_amount,
                "approved_amount": claim.approved_amount,
                "diagnosis_or_loss_type":
                    claim.diagnosis_or_loss_type,
                "fraud_risk_score":
                    claim.fraud_risk_score,
                "manual_review_flag":
                    claim.manual_review_flag,
                "rejection_or_adjustment_reason":
                    claim.rejection_or_adjustment_reason,
                },
                "policy":(
                    {
                         "policy_id": policy.policy_id,
                    "product_name": policy.product_name,
                    "policy_type": policy.policy_type,
                    "policy_status": policy.policy_status,
                    "sum_insured": policy.sum_insured,
                    "annual_premium": policy.annual_premium,
                    "co_pay_pct": policy.co_pay_pct,
                    "deductible": policy.deductible,
                    "waiting_period_days":
                        policy.waiting_period_days,
                    }
                    if policy
                    else None
                ),
                "documents":{
                    "total": len(documents),
                    "missing": missing_documents,
                    "pending_verification": pending_documents,
                    "verified": verified_documents,
                },
                "hospital":(
                    {
                        "hospital_id": hospital.hospital_id,
                    "hospital_name": hospital.hospital_name,
                    "city": hospital.city,
                    "network_status":
                        hospital.network_status,
                    "specialty": hospital.specialty,
                    }
                )
            }

    finally:
        db.close()
from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Policy

def get_policy_by_id(policy_id:str):

    db=SessionLocal()

    try:
        statement=select(Policy).where(
            Policy.policy_id==policy_id
        )

        result=db.execute(statement)

        policy=result.scalar_one_or_none()

        if not policy:
            return None

        return {
             "policy_id": policy.policy_id,
            "customer_id": policy.customer_id,
            "policy_type": policy.policy_type,
            "product_name": policy.product_name,
            "policy_start_date": str(policy.policy_start_date),
            "policy_end_date": str(policy.policy_end_date),
            "sum_insured": policy.sum_insured,
            "annual_premium": policy.annual_premium,
            "policy_status": policy.policy_status,
            "co_pay_pct": policy.co_pay_pct,
            "deductible": policy.deductible,
            "waiting_period_days": policy.waiting_period_days,
        }

    finally:
        db.close()
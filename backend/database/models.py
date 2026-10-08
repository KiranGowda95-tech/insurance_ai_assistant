from sqlalchemy import Column,String,Integer,Float,Date,Boolean
from .connection import Base

    # CUSTOMERS

class Customer(Base):
    __tablename__="customers"
    customer_id=Column(String,primary_key=True)
    customer_name=Column(String)
    age=Column(Integer)
    gender=Column(String)
    city=Column(String)
    state=Column(String)
    customer_since=Column(Date)
    kyc_status=Column(String)
    risk_segment=Column(String)


    # POLICIES

class Policy(Base):
    __tablename__="policies"
    policy_id=Column(String,primary_key=True)
    customer_id=Column(String)
    policy_type=Column(String)
    product_name=Column(String)
    policy_start_date=Column(Date)
    policy_end_date=Column(Date)
    sum_insured=Column(Float)
    annual_premium=Column(Float)
    policy_status=Column(String)
    co_pay_pct=Column(Float)
    deductible=Column(Float)
    waiting_period_days=Column(Integer)

class Claim(Base):
    __tablename__="claims"
    claim_id=Column(String,primary_key=True)
    customer_id=Column(String)
    policy_id=Column(String)
    policy_type=Column(String)
    claim_date=Column(Date)
    claim_amount=Column(Float)
    claim_status=Column(String)
    approved_amount=Column(Float)
    diagnosis_or_loss_type=Column(String)
    hospital_id=Column(String)
    fraud_risk_score=Column(Float)
    manual_review_flag=Column(Boolean)
    rejection_or_adjustment_reason=Column(String)

class ClaimDocument(Base):
    __tablename__="claim_documents"
    id=Column(Integer,primary_key=True)
    claim_id=Column(String)
    document_type=Column(String)
    upload_status=Column(String)
    document_status=Column(String)
    verification_status=Column(String)
    file_type=Column(String)

class Hospital(Base):
    __tablename__="hospitals"
    hospital_id=Column(String,primary_key=True)
    hospital_name=Column(String)
    city=Column(String)
    network_status=Column(String)
    specialty=Column(String)

class CustomerInteraction(Base):
    __tablename__="customer_interactions"
    interaction_id=Column(String,primary_key=True)
    customer_id=Column(String)
    claim_id=Column(String)
    interaction_date=Column(Date)
    channel=Column(String)
    intent=Column(String)
    sentiment=Column(String)
    resolution_status=Column(String)

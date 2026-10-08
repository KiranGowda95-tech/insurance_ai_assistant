from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database.connection import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from database.models import Claim

from services.claim_service import get_claim_by_id
from services.document_service import get_claim_documents,get_missing_documents

from services.policy_service import get_policy_by_id
from services.hospital_service import get_hospital_by_id

from services.claim_analysis_service import analyze_claim



app=FastAPI(
    title="Insurance AI Assistance API",
    description="Backend APi for the Enterprise Claims & Policy Intelligence Assistant",
    version="1.0.0",
)

#  cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




@app.get("/")
def root():
    return{
        "message":"Insurance AI Assistance API is running"
    }

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {
        "status":"Kiran is online"
    }

# CHAT

class ChatRequest(BaseModel):
    question:str

@app.post("/chat")
def chat(request:ChatRequest):
    return {
        "answer":f"You asked: {request.question}",
        "route":"TEST",
        "confidence":1.0,
        "source":[]
    }
    
@app.get("/claims")
def get_claims(db:Session=Depends(get_db)):
    claims=db.query(Claim).all()

    return claims

@app.get("/claims/{claim_id}")
def get_claim(claim_id:str):
    claim=get_claim_by_id(claim_id)

    if not claim:
        return {
            "success":False,
            "message":f"Claim {claim_id} not found"
        }

    return {
        "success":True,
        "claim":claim
    }


@app.get("/claims/{claim_id}/documents")
def claim_documents(claim_id:str):

    documents=get_claim_documents(claim_id)

    if not documents:
        return {
            "success":False,
            "message":f"No documents found for claim {claim_id}"
        }
    return {
        "success":True,
        "claim_id":claim_id,
        "documents":documents
    }


@app.get("/claims/{claim_id}/missing-documents")
def missing_documents(claim_id:str):

    documents=get_missing_documents(claim_id)

    return {
        "success":True,
        "claim_id":claim_id,
        "missing_documents":documents,
        "count":len(documents)
    }


@app.get("/policies/{policy_id}")
def get_policy(policy_id):

    policy=get_policy_by_id(policy_id)

    if not policy:
        return {
            "success":False,
            "message":f"Policy {policy_id} not found"
        }

    return {
        "success":True,
        "policy":policy
    }


@app.get("/hospitals/{hospital_id}")
def get_hospital(hospital_id:str):

    hospital=get_hospital_by_id(hospital_id)

    if not hospital:
        return {
            "success":False,
            "message":f"Hospital {hospital_id} not found"
        }

    return {
        "success":True,
        "hospital":hospital
    }

@app.get("/claims/{claim_id}/analysis")
def claim_analysis(claim_id:str):

    analysis=analyze_claim(claim_id)

    if not analysis:
        return {
            "success":True,
            "message":f"Claim {claim_id} not found"
        }

    return {
        "success":True,
        "claim_id":claim_id,
        "analysis":analysis
    }

    
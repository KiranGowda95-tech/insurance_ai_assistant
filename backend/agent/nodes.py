import re

from agent.state import AgentState

from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results
from rag.context_builder import build_context
from services.llm_service import generate_answer

from services.claim_service import get_claim_by_id
from services.document_service import get_missing_documents
from services.hospital_service import get_hospital_by_id


def classify_intent(state:AgentState)->dict:
    """
    choose the processing path based on the user's question.
    """
    query=state["query"].strip()
    normalized=query.lower()


    #Extract an identifier from question
    match=re.search(r"\bCLM[-_]?[A-Za-z0-9]+\b",query,re.I)
    claim_id=match.group(0) if match else ""

    #questions specifically about missing claim documents.
    if any(
        term in normalized
        for term in (
            "missing document",
            "missing documents",
            "documents are missing",
            "required documents",
            "pending documents",
    )
    ):
        intent="missing_documents"

    elif "hospital" in normalized or "hospitals" in normalized:
        intent="hospital"

    elif claim_id or any(
        term in normalized
        for term in [
            "claim status",
            "claim details",
            "claim number",
            "claim amount",
            "claim id"
        ]
    ):
        intent ="claim"

    elif any(
        term in normalized
        for term in [
            "policy",
            "coverage",
            "covered",
            "waiting period",
            "maternity",
            "exclusion",
            "deductible",
            "premium",
            "benifit",
            "benifits"
        ]
    ):
        intent ="policy"

    else:
        intent="unknown"

    return {
        "intent":intent,
        "claim_id":claim_id,
    }


def policy_node(state:AgentState)->dict:
    """Run the existing hybrid retrieval, reranking and LLM pipeline."""

    query=state["query"]

    candidates=hybrid_search(query=query,top_k=5)
    ranked=rerank_results(
        query=query,
        results=candidates,
        top_k=3
    )

    context=build_context(ranked)
    answer=generate_answer(query=query,context=context)

    sources=[
        {
            "policy_name":item.get("policy_name"),
            "document":item.get("source"),
            "rerank_score":item.get("rerank_score"),
        }
        for item in ranked
    ]

    return {
        "answer":answer,
        "sources":sources,
        "result":{"retrieved_policy_count":len(ranked)},
    }

def claim_node(state:AgentState)->dict:
    """Retrieve claim information from the SQL database."""

    claim_id=state.get("claim_id","")

    if not claim_id:
        return {
            "answer":"Please include the claim ID, for example CLM123.",
            "result":{},
        }

    claim=get_claim_by_id(claim_id)

    if not claim:
        return  {
            "answer":f"No claim was found for ID {claim_id}.Please verify the ID.",
            "result":{}
        }

    answer=(
        f"Claim ID: {claim['claim_id']}\n"
        f"Status: {claim['claim_status']}\n"
        f"Claim amount: {claim['claim_amount']}\n"
        f"Approved amount: {claim['approved_amount']}\n"
        f"Policy ID: {claim['policy_id']}\n"
        f"Diagnosis or loss type: {claim['diagnosis_or_loss_type']}"
    )

    return {"answer":answer,"result":claim,"sources":[]}


def missing_documents_node(state:AgentState)->dict:
    """Retrieve missing claim documents from SQL."""

    claim_id=state.get("claim_id","")

    if not claim_id:
        return {
            "answer":"Please include the claim ID so I can check its missing documents.",
            "result":[]
        }

    missing=get_missing_documents(claim_id)

    if not missing:
        return {
            "answer":(
                f"No documents marked as missing were found for claim {claim_id}."
            ),
            "result":[]
        }

    document_names=",".join(
        item["document_type"] for item in missing
    )

    return {
        "answer":(
            f"Claim {claim_id} has {len(missing)} document(s) marked as missing: "
            f"{document_names}."
        ),
        "result":missing,
        "sources":[]
    }

def hospital_node(state:AgentState)->dict:
    """Retrieve and format hospital information linked to a claim."""
    claim_id=state.get("claim_id","").strip()

    if not claim_id:
        return {
            "answer":(
                "Please include a claim ID so I can look up associated hospital."
            ),
            "result":{},
            "sources":[]
        }
    #Retrieve the claim
    claim =get_claim_by_id(claim_id)

    if not claim:
        return {
            "answer":f"No claim was found for ID {claim_id}.Please verify the ID.",
            "result":{},
            "sources":[],
        }

    #Extract the linked hospital ID
    hospital_id=claim.get("hospital_id")

    if not hospital_id:
        return {
            "answer":f"No hospital ID is recorder for claim {claim_id}.",
            "result":{"claim_id":claim_id,"hospital_id":None},
            "sources":[]
        }

    
    #Retrieve the hospital record
    hospital=get_hospital_by_id(str(hospital_id))

    if not hospital:
        return {
            "answer":(
                f"Claim {claim_id} references hospital {hospital_id}, "
                "but no matching hospital record was found."
            ),
            "result":{
                "claim_id":claim_id,
                "hospital_id":hospital_id
            },
            "sources":[]
        }

    #Format the returned data safely
    if isinstance(hospital,dict):
        details="\n".join(
            f"{key.replace('_',' ').title()}:{value}"
            for key,value in hospital.items()
            if value is not None
        )

    else:
        details=str(hospital)

    if not details.strip():
        details="The hospital record exists, but contains no displayable details."
    return {
        "answer":(
            f"Hospital linked to claim {claim_id}"
            f"(Hospital ID: {hospital_id})\n{details}"
        ),
        "result":{
            "claim_id":claim_id,
            "hospital_id":hospital_id,
            "hospital":hospital,
        },
        "sources":[]
    }







def unknown_node(state:AgentState)->dict:
    """Respond when the question does not match a supported operation."""

    return {
        "answer":(
            "I can help with insurance policy questions, claim details,"
            "missing claim documents and hospital associated with claims."
            "What would you like to know?"
        ),
        "sources":[],
        "result":{},
    }
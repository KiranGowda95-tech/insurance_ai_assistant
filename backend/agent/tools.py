import json

from langchain_core.tools import tool

from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results
from rag.context_builder import build_context

from services.claim_service import get_claim_by_id
from services.document_service import get_missing_documents
from services.hospital_service import get_hospital_by_id


@tool
def search_policy(query:str)->str:
    """Search insurance policy documents for coverage,benifits,waiting periods, conditions, and policy terms."""

    candidates=hybrid_search(query=query,top_k=10)

    ranked=rerank_results(
        query=query,
        results=candidates,
        top_k=3
    )

    context=build_context(ranked)

    sources=[
        {
            "policy_name":item.get("policy_name"),
            "document":item.get("source"),
            "rerank_score":item.get("rerank_score")
        }
        for item in ranked
    ]

    return json.dumps(
        {
            "context":context,
            "sources":sources
        },
        ensure_ascii=False,
        default=str
    )


@tool
def get_claim_details(claim_id:str)->str:
    """Retrieve claim status,amounts,policy ID, and loss details using an exact claim ID such as CLM300001."""
    
    claim_id=claim_id.strip()
    claim=get_claim_by_id(claim_id)

    if claim is None:
        return json.dumps(
            {
                "found":False,
                "message":f"Claim {claim_id} was not found."
            }
        )

    return json.dumps({
        "found":True,
        "claim":claim
    },ensure_ascii=False,default=str)


@tool
def get_missing_claim_documents(claim_id:str)->str:
    """Find documents marked Missing for an exact claim ID."""

    claim_id=claim_id.strip()
    claim =get_claim_by_id(claim_id)

    if not claim:
        return json.dumps(
            {
                "found":False,
                "message":f"Claim {claim_id} was not found.",

            }
        )

    documents=get_missing_documents(claim_id)

    return json.dumps(
        {
            "found":True,
            "claim_id":claim_id,
            "missing_documents":documents,
            "count":len(documents)
        },
        ensure_ascii=False,
        default=str,
    )


@tool
def get_claim_hospital(claim_id:str)->str:
    """Retrieve the hospital linked to an exact claim ID.
    Repost when the claim or linked hospital cannot be found."""

    claim_id=claim_id.strip()
    claim=get_claim_by_id(claim_id)

    if not claim:
        return json.dumps(
            {
                "found":False,
                "message":f"Claim {claim_id} was not found."
            }
        )

    hospital_id=claim.get("hospital_id")

    if not hospital_id:
        return json.dumps(
            {
                "found":True,
                "hospital_found":False,
                "claim_id":claim_id,
                "message":"No hospital ID is recorded for this claim."
            }
        )

    hospital=get_hospital_by_id(str(hospital_id))

    if not hospital:
        return json.dumps(
            {
                "found":True,
                "hospital_found":False,
                "claim_id":claim_id,
                "hospital_id":hospital_id,
                "message":"The linked hospital record was not found."
            }
        )

    return json.dumps(
        {
            "found":True,
            "hospital_found":True,
            "claim_id":claim_id,
            "hospital_id":hospital_id,
            "hospital":hospital,
        },
        ensure_ascii=False,
        default=str,
    )

INSURANCE_TOOLS=[
    search_policy,
    get_claim_details,
    get_missing_claim_documents,
    get_claim_hospital
]
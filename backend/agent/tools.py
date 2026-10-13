import json

from langchain_core.tools import tool

from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results
from rag.context_builder import build_context

from services.claim_service import get_claim_by_id
from services.document_service import get_missing_documents
from services.hospital_service import get_hospital_by_id
from services.claim_analysis_service import analyze_claim



@tool
def search_policy(query: str) -> str:
    """Search insurance policy documents for coverage, benefits, waiting
    periods, exclusions, and policy terms. Restrict retrieval to a named
    policy when the question identifies one."""

    import re

    policy_names = [
        "Health Secure Plus",
        "Family Care Gold",
        "Critical Care Elite",
        "Motor Protect Comprehensive",
        "Global Travel Secure",
        "Senior Health Shield",
        "Maternity Protect",
        "Two Wheeler Secure",
        "Car Shield Plus",
    ]

    def normalize(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")

    normalized_query = normalize(query)

    requested_policy = next(
        (
            name
            for name in policy_names
            if normalize(name) in normalized_query
        ),
        None,
    )

    policy_filter = (
        requested_policy.replace(" ", "_")
        if requested_policy
        else None
    )

    candidates = hybrid_search(
        query=query,
        top_k=10,
        policy_name=policy_filter,
    )

    # Enforce the policy boundary before reranking as an additional safeguard.
    if policy_filter:
        candidates = [
            item for item in candidates
            if normalize(
                item.get("policy_name")
                or item.get("source", "").removesuffix(".txt")
            ) == normalize(policy_filter)
        ]

    if not candidates:
        return json.dumps(
            {
                "context": "",
                "sources": [],
                "requested_policy": requested_policy,
                "message": (
                    f"No matching policy evidence was retrieved for "
                    f"{requested_policy}."
                    if requested_policy
                    else "No matching policy evidence was retrieved."
                ),
            },
            ensure_ascii=False,
        )

    ranked = rerank_results(
        query=query,
        results=candidates,
        top_k=3,
    )

    # Keep only the requested policy in the final evidence as well.
    if policy_filter:
        ranked = [
            item for item in ranked
            if normalize(
                item.get("policy_name")
                or item.get("source", "").removesuffix(".txt")
            ) == normalize(policy_filter)
        ]

    context = build_context(ranked)

    sources = [
        {
            "policy_name": item.get("policy_name"),
            "document": item.get("source"),
            "rerank_score": item.get("rerank_score"),
        }
        for item in ranked
    ]

    return json.dumps(
        {
            "context": context,
            "sources": sources,
            "requested_policy": requested_policy,
            "message": (
                "No matching policy evidence was found after reranking."
                if not ranked
                else None
            ),
        },
        ensure_ascii=False,
        default=str,
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

@tool
def analyze_claim_with_policy(claim_id: str) -> str:
    """Analyze an exact insurance claim using SQL records and policy RAG.
    Combine claim, policy, document, hospital, and relevant policy evidence.
    Do not infer that missing documents caused a claim to be pending."""

    claim_id = claim_id.strip()
    analysis = analyze_claim(claim_id)

    if analysis is None:
        return json.dumps(
            {
                "found": False,
                "claim_id": claim_id,
                "message": f"Claim {claim_id} was not found.",
            },
            ensure_ascii=False,
        )

    # Build a focused RAG query using facts from the retrieved SQL record.
    claim = analysis["claim"]
    policy = analysis.get("policy")

    if policy is None:
        policy_evidence = {
            "query": None,
            "context": "",
            "sources": [],
            "message": "No linked policy record was found. Policy-specific retrieval was skipped.",
        }
    else:

        policy_name = (
            policy.get("product_name")
            if policy
            else ""
        )
        diagnosis = claim.get("diagnosis_or_loss_type") or ""

        policy_query = (
            f"{policy_name}. Relevant coverage, exclusions, "
            f"claim requirements, and conditions for {diagnosis}."
        )

    # Retrieve and rerank policy-document evidence.
        candidates = hybrid_search(query=policy_query, top_k=10,policy_name=policy_name,)

        ranked = rerank_results(
            query=policy_query,
            results=candidates,
            top_k=3,
        )
        policy_context = build_context(ranked)

        policy_sources = [
            {
                "policy_name": item.get("policy_name"),
                "document": item.get("source"),
                "rerank_score": item.get("rerank_score"),
            }
            for item in ranked
        ]

        policy_evidence = {
            "query": policy_query,
            "context": policy_context,
            "sources": policy_sources,
        }

    return json.dumps(
        {
            "found": True,
            "analysis": analysis,
            "policy_evidence": policy_evidence,
            "interpretation_rules": [
                "Treat SQL records as the source of claim-specific facts.",
                "Treat retrieved policy text as policy evidence.",
                "Do not assume missing documents caused a pending claim.",
                "Do not invent a coverage decision or claim outcome.",
                "State when retrieved evidence is insufficient.",
            ],
        },
        ensure_ascii=False,
        default=str,
    )



INSURANCE_TOOLS=[
    search_policy,
    get_claim_details,
    get_missing_claim_documents,
    get_claim_hospital,
    analyze_claim_with_policy
]
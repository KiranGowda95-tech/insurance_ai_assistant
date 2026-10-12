from typing import Any,Literal
from typing_extensions import TypedDict

class AgentState(TypedDict,total=False):
    query:str
    intent:Literal[
        "policy",
        "claim",
        "missing_documents",
        "hospital",
        "unknown"
    ]
    claim_id:str
    answer:str
    sources:list[dict[str,Any]]
    result:dict[str,Any]
    error:str
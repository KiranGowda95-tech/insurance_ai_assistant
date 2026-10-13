

from langgraph.graph import StateGraph,START,END

from agent.state import AgentState
from agent.nodes import (
    classify_intent,
    policy_node,
    claim_node,
    missing_documents_node,
    hospital_node,
    unknown_node
)

# def route_by_intent(state:AgentState)->str:
#     """Choose the next node using the detected intent."""

#     intent=state.get("intent","unknown")

#     if intent=="policy":
#         return "policy"

#     if intent=="claim":
#         return "claim"

#     if intent=="missing_documents":
#         return "missing_documents"
    
#     if intent=="hospital":
#         return "hospital"

#     return "unknown"

def route_by_intent(state:AgentState)->str:
    intent=state.get("intent","unknown")

    routes={
        "policy":"policy",
        "claim":"claim",
        "missing_documents":"missing_documents",
        "hospital":"hospital"
    }

    return routes.get(intent,"unknown")


builder=StateGraph(AgentState)

builder.add_node("classify",classify_intent)
builder.add_node("policy",policy_node)
builder.add_node("claim",claim_node)
builder.add_node("missing_documents",missing_documents_node)
builder.add_node("hospital",hospital_node)
builder.add_node("unknown",unknown_node)

builder.add_edge(START,"classify")

builder.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "policy":"policy",
        "claim":"claim",
        "missing_documents":"missing_documents",
        "hospital":"hospital",
        "unknown":"unknown",
    }
)

builder.add_edge("policy",END)
builder.add_edge("claim",END)
builder.add_edge("missing_documents",END)
builder.add_edge("hospital",END)
builder.add_edge("unknown",END)

insurance_graph=builder.compile()

# def run_agent(query:str)->dict:
#     """Run the insurance assistant graph for one question."""

#     result=insurance_graph.invoke({"query":query})

#     return {
#         "query":result.get("query",query),
#         "query":result.get("intent","unknown"),
#         "query":result.get("answer",''),
#         "query":result.get("sources",[]),
#         "query":result.get("result",{}),
#     }


def run_agent(query: str) -> dict:
    """Run the insurance assistant graph and normalize its response."""

    result = insurance_graph.invoke({"query": query})

    return {
        "query": result.get("query", query),
        "intent": result.get("intent", "unknown"),
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "result": result.get("result", {}),
    }




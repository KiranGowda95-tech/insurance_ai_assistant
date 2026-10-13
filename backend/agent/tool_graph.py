import os
import re
from pathlib import Path
from typing import Annotated, Literal

from dotenv import load_dotenv
from typing_extensions import TypedDict

from langchain_core.messages import AIMessage,AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END,MessagesState
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition

from agent.tools import INSURANCE_TOOLS


#Load .env from the project root.
PROJECT_ROOT=Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT /".env")

SYSTEM_PROMPT="""
Tou are an insurance claim and policy intelligence assistant.

Use the available tools to answer policy,claim,missing-document, and hospital questions.

Rules:
1. Use policy search for policy terms and coverage questions.
2. Use claim tools for claim-specific questions.
3. Never invent claim records,document statuses, or hospital details.
4. Base factual answers on tool results.
5. id a record is not found, say so clearly.
6. Do not claim that a claim is approved or rejected unless the retrieved claim record explicitly supports that status.
7. Policy documents are synthetic training documents, not real insurance contracts.
8. Be concise and preserve important conditions and limitations.
9. Only answer questions related to insurance policies,
   claims, missing documents, hospitals, and insurance
   processes. Politely decline unrelated questions.
"""

INSURANCE_KEYWORDS = {
    "insurance", "insurer", "policy", "policies", "claim", "claims",
    "coverage", "covered", "premium", "deductible", "exclusion",
    "maternity", "waiting period", "benefit", "benefits",
    "reimbursement", "cashless", "hospital", "network hospital",
    "missing document", "missing documents", "claim form",
    "settlement", "pre-existing", "preexisting", "add-on",
    "copay", "co-pay", "sum insured", "renewal", "nominee",
    "under review", "approved claim", "rejected claim",
    "health plan", "health insurance", "motor insurance",
    "travel insurance", "critical illness", "document",
    "documents",
    "missing document",
    "missing documents",
    "claim form",
    "claim id",
    "claim status",
    "claim number",
    "claim details",
    "hospital details",
    "policy details",
    "waiting period",
    "insurance claim",
}

# These patterns identify clearly unrelated requests.
OFF_TOPIC_PATTERNS = (
    "capital of france",
    "capital of germany",
    "capital of india",
    "weather today",
    "write python code",
    "debug my code",
    "football score",
    "recipe for",
    "write a poem",
    "translate this",
    "latest movie",
)

CLARIFICATION_PATTERNS = (
    "hello",
    "hi",
    "hey",
    "help me",
    "what can you do",
    "can you help",
)

class InsuranceAgentState(TypedDict,total=False):
    messages:Annotated[list[AnyMessage],add_messages]
    query:str
    scope_status:Literal[
        "in_scope","out_of_scope","clarification"
    ]


def get_latest_user_query(state:InsuranceAgentState)->str:
    """Extract the latest user message from the conversation."""
    for message in reversed(state.get("messages",[])):

        if isinstance(message,dict):
            message_type=message.get("type") or message.get("role")
            content=message.get("content","")

        else:
            message_type=getattr(message,"type","")
            content=getattr(message,"content","")

        if message_type not in ("human","user"):
            continue

        if isinstance(content,str):
            return content.strip()

        if isinstance(content,list):
            text_parts=[
                item.get("text","")
                for item in content
                if isinstance(item,dict)
                and item.get("type")=="text"
            ]

            return " ".join(text_parts).strip()
        return ""
    return ""


def validate_scope(state:InsuranceAgentState)->dict:
    """Classsify the request before invoking the LLm or tools."""
    query=get_latest_user_query(state)
    normalized_query=query.lower().strip()

    if not normalized_query:
        return {
            "query":query,
            "scope_status":"clarification",
        }

    if any(pattern in normalized_query for pattern in OFF_TOPIC_PATTERNS):
        return {
            "query":query,
            "scope_status":"out_of_scope",
        }

    GREETINGS={
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if normalized_query in GREETINGS or any(
        phrase in normalized_query
        for phrase in ("help me","what can you do")
    ):
        return {
            "query":query,
            "scope_status":"clarification"
        }

    has_claim_id=bool(
        re.search(r"\bCLM[-_]?[A-Za-z0-9]+\b",
            normalized_query,)
        
    )

    if has_claim_id or any(
        keyword in normalized_query
        for keyword in INSURANCE_KEYWORDS
    ):
        return {
            "query":query,
            "scope_status":"in_scope",
        }

    #Unknown requests are clarified insted of automatically
    #being classified as unrelated.
    return {
        "query":query,
        "scope_status":"out_of_scope",
    }

def route_after_validation(state:InsuranceAgentState)->str:
    """Choose the next node using the validation result."""
    if state.get("scope_status")=="in_scope":
        return "assistant"
    return "scope_response"

def scope_response_node(state:InsuranceAgentState)->dict:
    """Respond without calling the LLM or insurance tools."""
    if state.get("scope_status")=="out_of_scope":
        answer=(
            "I'm sorry, but I can only assist with questions related "
            "to insurance policies, claims, missing documents, "
            "hospitals, and insurance processes."
        )
    else:
        answer=(
            "I can help with insurance policies, claim status, "
            "missing documents, hospital details, and coverage. "
            "What would you like to know?"
        )

    return {
        "messages":[AIMessage(content=answer)]
    }


#Initializing the model abd bind the existing tools.
llm=ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools=llm.bind_tools(INSURANCE_TOOLS)

def assistant_node(state:InsuranceAgentState)->dict:
    """Generate an answer or request a tool call."""
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT,
        },
        *state["messages"]
    ]

    response=llm_with_tools.invoke(messages)

    return {
        "messages":[response]
    }


#Build the graph
builder=StateGraph(InsuranceAgentState)

builder.add_node("validate_scope",validate_scope)
builder.add_node("assistant",assistant_node)
builder.add_node("tools",ToolNode(INSURANCE_TOOLS))
builder.add_node("scope_response",scope_response_node)

builder.add_edge(START,"validate_scope")


builder.add_conditional_edges(
    "validate_scope",
    route_after_validation,
    {
        "assistant":"assistant",
        "scope_response":"scope_response",
    }
)
builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools":"tools",
        END:END,
    }
)

builder.add_edge("tools","assistant")
builder.add_edge("scope_response",END)

tool_calling_graph=builder.compile()

def run_tool_agent(query:str)->dict:
    """Run a user query through validation and the tool-calling graph."""

    result=tool_calling_graph.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":query
                }
            ]
        },
        config={"recursion_limit":8}
    )

    messages=result["messages"]
    final_message=messages[-1]

    answer=final_message.content

    if isinstance(answer,list):
        answer="\n".join(
            block.get("text","")
            for block in answer
            if isinstance(block,dict) and block.get("type")=="text"
        )

    tools_used=[
        message.name
        for message in messages
        if getattr(message,"type","")=="tool"
    ]

    return {
        "query":query,
        "answer":answer,
        "tools_used":tools_used,
        "scope_status":result.get("scope_status","unknown")
    }


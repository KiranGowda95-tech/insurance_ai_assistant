import logging
import re
from pathlib import Path
from typing import Annotated, Literal

from dotenv import load_dotenv
from typing_extensions import TypedDict

from langchain_core.messages import AIMessage, AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from agent.tools import INSURANCE_TOOLS


logger = logging.getLogger(__name__)


# Load .env from the project root.
# Adjust this path if this file is located at a different depth.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


SYSTEM_PROMPT = """
You are an insurance claim and policy intelligence assistant.

Use the available tools to answer policy, claim, missing-document,
and hospital questions.

Rules:
1. Use policy search for policy terms and coverage questions.
2. Use claim tools for claim-specific questions.
3. Never invent claim records, document statuses, or hospital details.
4. Base factual answers on tool results.
5. If a record is not found, say so clearly.
6. Do not claim that a claim is approved or rejected unless the
   retrieved claim record explicitly supports that status.
7. Policy documents are synthetic training documents, not real
   insurance contracts.
8. Be concise and preserve important conditions and limitations.
9. Only answer questions related to insurance policies, claims,
   missing documents, hospitals, and insurance processes.
   Politely decline unrelated questions.
10. Retrieve claim facts from the claim tools. Do not invent records
    or values.
11. Retrieve missing-document information from the appropriate tool.
12. For policy information, use the policy search tool.
13. For combined claim analysis, use all relevant tools and combine
    their results.
14. Clearly separate verified facts from possible explanations.
15. Never state that a missing document caused a claim to be pending
    unless retrieved records explicitly establish that relationship.
16. A manual review flag means the claim is marked for manual review.
    Do not invent the reason.
17. Do not invent policy clauses, coverage decisions, or outcomes.
18. If the evidence cannot establish why a claim is pending, say so.
19. Do not assume a currency symbol or code unless the source data
    establishes it.
20. Answer in readable Markdown with clear headings and bullet points.
"""


INSURANCE_KEYWORDS = {
    "insurance",
    "insurer",
    "policy",
    "policies",
    "claim",
    "claims",
    "coverage",
    "covered",
    "premium",
    "deductible",
    "exclusion",
    "maternity",
    "waiting period",
    "benefit",
    "benefits",
    "reimbursement",
    "cashless",
    "hospital",
    "network hospital",
    "missing document",
    "missing documents",
    "claim form",
    "settlement",
    "pre-existing",
    "preexisting",
    "add-on",
    "copay",
    "co-pay",
    "sum insured",
    "renewal",
    "nominee",
    "under review",
    "approved claim",
    "rejected claim",
    "health plan",
    "health insurance",
    "motor insurance",
    "travel insurance",
    "critical illness",
    "document",
    "documents",
    "claim id",
    "claim status",
    "claim number",
    "claim details",
    "hospital details",
    "policy details",
    "insurance claim",
}


# Clearly unrelated requests.
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


GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
}


class InsuranceAgentState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    query: str
    scope_status: Literal[
        "in_scope",
        "out_of_scope",
        "clarification",
    ]


def get_latest_user_query(state: InsuranceAgentState) -> str:
    """Extract the latest user message from the conversation."""

    for message in reversed(state.get("messages", [])):
        if isinstance(message, dict):
            message_type = message.get("type") or message.get("role")
            content = message.get("content", "")
        else:
            message_type = getattr(message, "type", "")
            content = getattr(message, "content", "")

        if message_type not in ("human", "user"):
            continue

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            text_parts = [
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
                and item.get("type") == "text"
            ]
            return " ".join(text_parts).strip()

        return ""

    return ""


def has_relevant_previous_context(state: InsuranceAgentState) -> bool:
    """Return True when a vague follow-up refers to an insurance conversation."""

    messages = state.get("messages", [])

    # The graph receives conversation history followed by the current question.
    # Exclude the last message because it is the current user question.
    previous_messages = messages[:-1] if messages else []

    previous_parts = []

    for message in previous_messages:
        if isinstance(message, dict):
            role = message.get("role") or message.get("type", "")
            content = message.get("content", "")
        else:
            role = getattr(message, "type", "")
            content = getattr(message, "content", "")

        role = str(role).lower()

        if role not in ("human", "user", "ai", "assistant"):
            continue

        if isinstance(content, str):
            previous_parts.append(content.lower())
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    previous_parts.append(item["text"].lower())

    previous_context = " ".join(previous_parts)

    has_insurance_context = (
        bool(re.search(r"\bCLM[-_]?[A-Za-z0-9]+\b", previous_context, re.I))
        or any(
            keyword in previous_context
            for keyword in INSURANCE_KEYWORDS
        )
    )

    return has_insurance_context


def previous_context_query(state: InsuranceAgentState) -> str:
    """Return the latest user question in lowercase."""
    return get_latest_user_query(state).lower().strip()


def validate_scope(state: InsuranceAgentState) -> dict:
    """Validate scope while supporting contextual insurance follow-ups."""

    query = get_latest_user_query(state)
    normalized_query = query.lower().strip()

    if not normalized_query:
        return {
            "query": query,
            "scope_status": "clarification",
        }

    # Explicitly unrelated requests remain blocked.
    if any(
        pattern in normalized_query
        for pattern in OFF_TOPIC_PATTERNS
    ):
        return {
            "query": query,
            "scope_status": "out_of_scope",
        }

    if normalized_query in GREETINGS or normalized_query in (
        "help me",
        "what can you do",
    ):
        return {
            "query": query,
            "scope_status": "clarification",
        }

    # Normalize the phrases too, so capitalization cannot break matching.
    follow_up_phrases = (
        "this issue",
        "that issue",
        "resolve this",
        "resolve it",
        "fix this",
        "fix it",
        "how can i",
        "how do i",
        "what should i do",
        "why is it",
        "what about it",
        "tell me more",
        "explain further",
    )

    is_follow_up = (
        has_relevant_previous_context(state)
        and any(
            phrase in normalized_query
            for phrase in follow_up_phrases
        )
    )

    has_claim_id = bool(
        re.search(
            r"\bCLM[-_]?[A-Za-z0-9]+\b",
            normalized_query,
            re.IGNORECASE,
        )
    )

    if (
        is_follow_up
        or has_claim_id
        or any(
            keyword in normalized_query
            for keyword in INSURANCE_KEYWORDS
        )
    ):
        return {
            "query": query,
            "scope_status": "in_scope",
        }

    return {
        "query": query,
        "scope_status": "clarification",
    }


def route_after_validation(state: InsuranceAgentState) -> str:
    """Choose the next node based on scope validation."""

    if state.get("scope_status") == "in_scope":
        return "assistant"

    return "scope_response"


def scope_response_node(state: InsuranceAgentState) -> dict:
    """Respond without invoking the LLM or insurance tools."""

    if state.get("scope_status") == "out_of_scope":
        answer = (
            "I'm sorry, but I can only assist with questions related "
            "to insurance policies, claims, missing documents, "
            "hospitals, and insurance processes."
        )
    else:
        answer = (
            "I can help with insurance policies, claim status, "
            "missing documents, hospital details, and coverage. "
            "What would you like to know?"
        )

    return {
        "messages": [AIMessage(content=answer)]
    }


# Initialize the model and bind the existing insurance tools.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools = llm.bind_tools(INSURANCE_TOOLS)


def assistant_node(state: InsuranceAgentState) -> dict:
    """Generate an answer or request a tool call."""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        *state.get("messages", []),
    ]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# Build the LangGraph workflow.
builder = StateGraph(InsuranceAgentState)

builder.add_node("validate_scope", validate_scope)
builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(INSURANCE_TOOLS))
builder.add_node("scope_response", scope_response_node)

builder.add_edge(START, "validate_scope")

builder.add_conditional_edges(
    "validate_scope",
    route_after_validation,
    {
        "assistant": "assistant",
        "scope_response": "scope_response",
    },
)

builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "assistant")
builder.add_edge("scope_response", END)

tool_calling_graph = builder.compile()


def run_tool_agent(
    query: str,
    history: list[dict] | None = None,
) -> dict:
    """Run the insurance agent with optional conversation history."""

    messages = []

    # Keep only the last 10 history messages.
    for item in (history or [])[-10:]:
        role = item.get("role")
        content = item.get("content", "")

        if (
            role in ("user", "assistant")
            and isinstance(content, str)
        ):
            messages.append({
                "role": role,
                "content": content,
            })

    messages.append({
        "role": "user",
        "content": query,
    })

    result = tool_calling_graph.invoke(
        {"messages": messages},
        config={"recursion_limit": 8},
    )

    answer = ""
    tools_used = []

    for message in result.get("messages", []):
        if getattr(message, "type", "") == "ai":
            if (
                isinstance(message.content, str)
                and message.content.strip()
            ):
                answer = message.content

        if getattr(message, "type", "") == "tool":
            tool_name = getattr(message, "name", None)

            if tool_name and tool_name not in tools_used:
                tools_used.append(tool_name)

    return {
        "query": query,
        "answer": answer,
        "tools_used": tools_used,
        "scope_status": result.get("scope_status", "unknown"),
    }
import os

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END,MessagesState
from langgraph.prebuilt import ToolNode,tools_condition

from agent.tools import INSURANCE_TOOLS

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
llm=ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools=llm.bind_tools(INSURANCE_TOOLS)

def assistant_node(state:MessagesState):
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

builder=StateGraph(MessagesState)

builder.add_node("assistant",assistant_node)
builder.add_node("tools",ToolNode(INSURANCE_TOOLS))

builder.add_edge(START,"assistant")

builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools":"tools",
        END:END,
    }
)

builder.add_edge("tools","assistant")

tool_calling_graph=builder.compile()

def run_tool_agent(query:str)->dict:
    """Run the LLM-driven tool-calling workflow."""

    result=tool_calling_graph.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":query
                }
            ]
        }
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

    tool_names=[
        message.name
        for message in messages
        if getattr(message,"type",None)=="tool"
    ]

    return {
        "query":query,
        "answer":answer,
        "tools_used":tool_names

    }


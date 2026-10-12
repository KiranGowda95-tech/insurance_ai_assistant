from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results
from rag.context_builder import build_context
from services.llm_service import generate_answer

from agent.graph import run_agent

# def process_chat(query:str)->dict:
#     """"
#     Runs the complete RAG pipeline for a user query.
#     """

#     #Retrieve candidates using hybrid search
#     hybrid_results=hybrid_search(
#         query=query,
#         top_k=5
#     )

#     #Rerank retrieved candidates
#     reranked_results=rerank_results(
#         query=query,
#         results=hybrid_results,
#         top_k=3
#     )

#     #Build grounded context
#     context=build_context(reranked_results)

#     #Generate final answer using the LLm
#     answer=generate_answer(
#         query=query,
#         context=context
#     )

#     #Extract source information
#     sources=[]

#     for result in reranked_results:
#         source={
#             "policy_name":result.get("policy_name"),
#             "document":result.get("source"),
#             "rerank_score":result.get("rerank_score")
                
#         }

#         sources.append(source)


#     return {
#         "query":query,
#         "answer":answer,
#         "sources":sources
#     }


# def process_chat(query:str)->dict:
#     """Delegate chat requests to the LangGraph insurance assistant."""

#     return run_agent(query.strip())


from agent.tool_graph import run_tool_agent

def process_chat(query:str)->dict:
    """Process a chat request through the LLM tool-calling agent."""

    query=query.strip()

    if not query:
        return {
            "query":query,
            "answer":"Please enter a question.",
            "tools_used":[]
        }

    result=run_tool_agent(query)

    return {
        "query":result.get("query",query),
        "answer":result.get("answer",""),
        "tools_used":result.get("tools_used",[])
    }
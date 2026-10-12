import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results
from rag.context_builder import build_context
from services.llm_service import generate_answer

query="What is the maternity waiting period?"

#Hybrid retrieval

hybrid_results=hybrid_search(
    query=query,
    top_k=5
)

#Cross-encoder reranking
reranked_results=rerank_results(
    query=query,
    results=hybrid_results,
    top_k=3
)

#Build grounded context
context=build_context(
    reranked_results
)

#Generate answer
answer=generate_answer(
    query=query,
    context=context
)

print("="*70)
print("RAG ANSWER")
print("="*70)

print(answer)

print('='*70)

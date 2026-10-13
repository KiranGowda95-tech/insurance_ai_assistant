import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results
from rag.context_builder import build_context

query="What is the maternity waiting period?"

#Hybrid retrieval
hybrid_results=hybrid_search(
    query=query,
    top_k=5
)

print("\n"+"="*70)
print("HYBRID RESULT COUNT")
print("="*70)

print(len(hybrid_results))

#reranking
reranked_results=rerank_results(
    query=query,
    results=hybrid_results,
    top_k=3
)

print("\n"+"="*70)
print("\nRERANKED RESULT COUNT:")
print("="*70)

print(len(reranked_results))

# Inspect every result
print("\n"+"="*70)
print("RERANKED RESULTS DEBUG")
print("="*70)

for index,result in enumerate(
    reranked_results,
    start=1
):
    print(f"\nRESULT {index}")
    print("Keys:",result.keys())
    print("Policy:",result.get("policy_name"))
    print("Source:",result.get("source"))
    print("Text length",len(result.get("text","")))


#buid  context
context=build_context(
    reranked_results
)


#Inspect context
print("\n" + "=" * 70)
print("RAG CONTEXT")
print("=" * 70)

print(context)

print("\n" + "=" * 70)
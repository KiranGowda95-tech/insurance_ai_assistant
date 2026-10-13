from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank_results

query="What is teh maternity waiting period?"

# To get candidates from hybrid search
hybrid_results=hybrid_search(
    query=query,
    top_k=5
)

#Rerank those candidates
reranked_results=rerank_results(
    query=query,
    results=hybrid_results,
    top_k=3
)


print("="*70)
print("RERANKED SEARCH")
print("="*70)

for index, result in enumerate(
    reranked_results,
    start=1
):

    print()

    print(f"RESULT {index}")

    print(f"Policy: {result["policy_name"]}")

    print(f"Source: {result["source"]}")

    print(
        f"Rerank Score: "
        f"{result['rerank_score']:.4f}"
    )

    print(
        f"RRF Score: "
        f"{result['rrf_score']:.6f}"
    )

    print("\nTEXT:")

    print(result["text"])

    print("=" * 70)
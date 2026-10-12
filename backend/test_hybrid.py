from rag.hybrid_retriever import hybrid_search

query="What is the maternity waiting period?"

results=hybrid_search(
    query=query,
    top_k=5
)

print("=" * 70)
print("HYBRID SEARCH")
print("=" * 70)

print(f"Query: {query}")

print("=" * 70)

for index, result in enumerate(results,start=1):

    print()
    print(f"RESULT {index}")

    print(f"Policy: {result["policy_name"]}")
    print(f"source: {result["source"]}")
    print(f"RRF Score: {result["rrf_score"]:.6f}")

    print("\nTEXT:")
    print(result["text"])

    print("=" * 70)

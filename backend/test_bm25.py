from rag.bm25_retriever import search_bm25

query="What is the maternity waiting period?"

results=search_bm25(
    query,
    top_k=3
)

print("="*70)
print("BM25 SEARCH")
print("="*70)

print(f"Query: {query}")

print("="*70)

for index,result in enumerate(results,start=1):

    print()
    print(f"RESULT {index}")

    print(f"Policy: {result['policy_name']}")
    print(f"Source: {result['source']}")
    print(f"BM25 Score: {result["bm25_score"]:.4f}")

    print("\nTEXT")
    print(result["text"])

    print("-"*70)
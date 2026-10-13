from rag.retriever import search_policy

query="What is the maternity waiting period for a family care Gold?"

results=search_policy(query,top_k=3)

print("="*70)
print("QUERY")
print("query")
print("="*70)

for index,result in enumerate(results,start=1):
    print()
    print(f"RESULT {index}")
    print(f"Policy: {result["policy_name"]}")
    print(f"Source: {result["source"]}")
    print(f"Distance: {result['distance']:.4f}")

    print("\nTEXT:")
    print(result['text'])

    print("="*70)

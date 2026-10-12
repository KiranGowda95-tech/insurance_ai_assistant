from rag.loader import load_policy_documents

documents=load_policy_documents()

print("="*70)
print(f"POLICY DOCUMENTS LOADED: {len(documents)}")
print("="*70)

for document in documents:

    print()
    print(f"Source: {document["source"]}")
    print(f"Policy: {document["policy_name"]}")
    print(f"Characters: {len(document["text"])}")

    print("\nPreview:")
    print(document["text"][:300])

    print("-"*70)
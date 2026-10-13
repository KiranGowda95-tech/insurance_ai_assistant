from rag.loader import load_policy_documents
from rag.chunker import chunk_policy_documents

documents=load_policy_documents()
chunks=chunk_policy_documents(documents)

print("="*70)
print(f"POLICY DOCUMENTS: {len(documents)}")
print(f"TOTAL CHUNKS: {len(chunks)}")
print("="*70)

for chunk in chunks[:10]:
    print()
    print(f"Chunk ID: {chunk["chunk_id"]}")
    print(f"Source: {chunk['source']}")
    print(f"Policy: {chunk['policy_name']}")
    print(f"characters: {len(chunk['text'])}")
    print("\nText:")
    print(chunk['text'])
    print("="*70)

import chromadb
from sentence_transformers import SentenceTransformer

from rag.loader import load_policy_documents
from rag.chunker import chunk_policy_documents


#Embedding model
embedding_model=SentenceTransformer("all-MiniLM-L6-v2")

#ChromaDB persistent storage
chroma_client=chromadb.PersistentClient(
    path="./chroma_db"
)

#Create or get the collections
collection=chroma_client.get_or_create_collection(
    name="insurance_policies"
)

def build_vector_store():
    documents=load_policy_documents()
    chunks=chunk_policy_documents(documents)

    ids=[]
    texts=[]
    metadatas=[]

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        texts.append(chunk["text"])

        metadatas.append({
            "source":chunk["source"],
            "policy_name":chunk["policy_name"]
        })

    embeddings=embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


    print("="*70)
    print("VECTOR STORE CREATED")
    print("="*70)
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Stored vectors: {collection.count()}")
from rank_bm25 import BM25Okapi

from rag.loader import load_policy_documents
from rag.chunker import chunk_policy_documents

#to load and chunk policy documents
documents=load_policy_documents()
chunks=chunk_policy_documents(documents)

#to tokenize each chunk
tokenized_chunks=[
    chunk["text"].lower().split()

    for chunk in chunks
]

# To build BM25 index
bm25=BM25Okapi(tokenized_chunks)

def search_bm25(query:str,top_k:int=3,policy_name:str=None):

    query_tokens=query.lower().split()

    scores=bm25.get_scores(query_tokens)

    ranked_indices=sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    results=[]

    for index in ranked_indices:
        chunk=chunks[index]

        # here metadata filtering will happen
        if policy_name and chunk["policy_name"] !=policy_name:
            continue

        results.append({
            "text":chunk['text'],
            "source":chunk["source"],
            "policy_name":chunk["policy_name"],
            "bm25_score":float(scores[index])

        })

        if len(results) >=top_k:
            break
    return results


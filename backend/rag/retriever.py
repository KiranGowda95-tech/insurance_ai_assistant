from rag.vector_store import collection,embedding_model

def search_policy(query:str,top_k:int=3,policy_name:str=None):
    query_embedding=embedding_model.encode([query])

    query_kwargs={
        "query_embeddings":query_embedding.tolist(),
        "n_results":top_k
    }

    #Optional metadata filtering
    if policy_name:
        query_kwargs["where"]={
            "policy_name":policy_name
        }

    results=collection.query(**query_kwargs)

    matches=[]

    documents=results["documents"][0]
    metadatas=results["metadatas"][0]
    distances=results["distances"][0]

    for i in range(len(documents)):
        matches.append({
            "text":documents[i],
            "source":metadatas[i]['source'],
            "policy_name":metadatas[i]['policy_name'],
            "distance":distances[i]

        })

    return matches
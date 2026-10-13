from sentence_transformers import CrossEncoder

reranker_model=CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)

def rerank_results(
        query:str,
        results:list,
        top_k:int=3
):
    """
    Rerank retrieved documents using a cross-encoder.

    Args:
        query:User's search query.
        results:Results returned by the hybrid retrieve.
        top_k:Number of results to return.
    Returns:
        Reranked results with relevance scores.
    """

    if not results:
        return []

    #Create query-document pairs
    pairs=[
        [query,result["text"]]
        for result in results
    ]

    #Calculate relevance scores
    scores=reranker_model.predict(pairs)

    reranked_results=[]

    for result,score in zip(results,scores):

        reranked_results.append({
            **result,
            "rerank_score":float(score)
        })

    #sort by reranker score
    reranked_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_results[:top_k]
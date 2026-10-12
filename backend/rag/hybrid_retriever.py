from rag.retriever import search_policy
from rag.bm25_retriever import search_bm25

RRF_K = 60


def hybrid_search(
    query: str,
    top_k: int = 5,
    policy_name: str = None
):
    # -----------------------------
    # 1. Semantic search
    # -----------------------------
    semantic_results = search_policy(
        query=query,
        top_k=top_k,
        policy_name=policy_name
    )

    # -----------------------------
    # 2. BM25 keyword search
    # -----------------------------
    bm25_results = search_bm25(
        query=query,
        top_k=top_k,
        policy_name=policy_name
    )

    combined = {}

    # -----------------------------
    # 3. Add semantic results
    # -----------------------------
    for rank, result in enumerate(semantic_results, start=1):

        key = (
            result["source"],
            result["text"]
        )

        if key not in combined:
            combined[key] = {
                "text": result["text"],
                "source": result["source"],
                "policy_name": result.get(
                    "policy_name",
                    result["source"].replace(".txt", "")
                ),
                "rrf_score": 0.0
            }

        combined[key]["rrf_score"] += (
            1 / (RRF_K + rank)
        )

    # -----------------------------
    # 4. Add BM25 results
    # -----------------------------
    for rank, result in enumerate(bm25_results, start=1):

        key = (
            result["source"],
            result["text"]
        )

        if key not in combined:
            combined[key] = {
                "text": result["text"],
                "source": result["source"],
                "policy_name": result.get(
                    "policy_name",
                    result["source"].replace(".txt", "")
                ),
                "rrf_score": 0.0
            }

        combined[key]["rrf_score"] += (
            1 / (RRF_K + rank)
        )

    # -----------------------------
    # 5. Sort by RRF score
    # -----------------------------
    ranked_results = sorted(
        combined.values(),
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    # -----------------------------
    # 6. Return top results
    # -----------------------------
    return ranked_results[:top_k]
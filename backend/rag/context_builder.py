def build_context(results:list)->str:
    """
    Build a structured context string from all reranked results.

    This function does not perform retrieval or ranking.
    It only converts the retrieved documents into LLM-ready context.
    """

    if not results:
        return "No relevant policy information was found."

    context_parts=[]

    for index, result in enumerate(results,start=1):

        policy_name=result.get(
            "policy_name",
            "Unknown Policy"
        )

        source=result.get(
            "source",
            "Unknown Source"
        )

        text=result.get(
            "text",
            ""
        )

        context_block=f"""
SOURCE {index} 
Policy: {policy_name}
Document: {source}
{text}
"""

        context_parts.append(context_block)

    return "\n\n"+("\n\n"+'='*70+"\n\n").join(context_parts)
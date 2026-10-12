from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_policy_documents(documents):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ".",
            " ",
            ""
        ]
    )

    chunks=[]

    for document in documents:
        document_chunks=splitter.split_text(document["text"])

        for index,chunk_text in enumerate(document_chunks):
            chunks.append({
                "chunk_id":f"{document['policy_name']}_{index}",
                "source":document["source"],
                "policy_name":document["policy_name"],
                "text":chunk_text

            })

    return chunks

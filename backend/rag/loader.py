from pathlib import Path

POLICY_DOCUMENTS_DIR=Path("policy_documents")

def load_policy_documents():

    documents=[]

    for file_path in POLICY_DOCUMENTS_DIR.glob("*.txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text=file.read()

        documents.append({
            "source":file_path.name,
            "policy_name":file_path.stem,
            "text":text
        })
        # print("documents from loader file: ",documents)
    return documents

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.chat_service import process_chat

router =APIRouter(
    prefix="/api",
    tags=["Chat"]
)

class ChatRequest(BaseModel):
    query:str


@router.post("/chat")
def chat(request:ChatRequest):
    """
    Process a user question through the insurance RAG pipeline.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:
        result = process_chat(request.query)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

    
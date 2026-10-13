import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field

from services.chat_service import process_chat

logger=logging.getLogger(__name__)

router =APIRouter(
    prefix="/api",
    tags=["Chat"]
)

class ChatRequest(BaseModel):
    query:str=Field(
        min_length=1,
        max_length=2000,
        description="Insurance-related question,upto 2000 characters."
    )


@router.post("/chat")
def chat(request:ChatRequest):
    """
    Process a user question through the insurance assistant.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:
        result = process_chat(request.query)

        return result

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexcepted error while processing chat query.")

        raise HTTPException(
            status_code=500,
            detail=(
                "The assistant could not process your request."
                "Please try again later."
            ),
        ) from None

    
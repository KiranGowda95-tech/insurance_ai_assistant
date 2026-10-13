import logging

from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field

from services.chat_service import process_chat

from services.interaction_analytics_service import (
    get_interaction_analytics,
)


logger=logging.getLogger(__name__)

router =APIRouter(
    prefix="/api",
    tags=["Chat"]
)

class ChatHistoryMessage(BaseModel):
    role:Literal["user","assistant"]
    content:str=Field(max_length=10000)

class ChatRequest(BaseModel):
    query:str=Field(
        min_length=1,
        max_length=2000,
        description="Insurance-related question,upto 2000 characters."
    )
    history:list[ChatHistoryMessage]=Field(
        default_factory=list,
        max_length=10,
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
        result = process_chat(request.query,history=[item.model_dump() for item in request.history])

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



@router.get("/analytics/interactions")
def interaction_analytics():
    """
    Return customer interaction analytics from the database.
    """
    try:
        return get_interaction_analytics()

    except Exception:
        logger.exception(
            "Unexpected error while fetching interaction analytics."
        )

        raise HTTPException(
            status_code=500,
            detail="Could not retrieve interaction analytics."
        ) from None

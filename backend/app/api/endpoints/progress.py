from fastapi import APIRouter, Query
from app.models.progress import get_user_progress, user_progress_store
from pydantic import BaseModel

router = APIRouter()

class ProgressResponse(BaseModel):
    user_id: str
    general_level: int
    topic_levels: dict

@router.get("", response_model=ProgressResponse)
@router.get("/", response_model=ProgressResponse)
def get_progress(user_id: str = Query(...)):
    progress = get_user_progress(user_id)
    return ProgressResponse(
        user_id=progress.user_id,
        general_level=progress.general_level,
        topic_levels=progress.topic_levels
    )

class ProgressUpdateRequest(BaseModel):
    user_id: str
    topic: str
    amount: int = 1

@router.post("/update", response_model=ProgressResponse)
def update_progress(req: ProgressUpdateRequest):
    # Debug: print empfangene Daten
    print('ProgressUpdateRequest:', req.dict())
    assert req.topic in [
        'variables', 'operators', 'if_else', 'loops', 'lists', 'functions', 'strings', 'dictionaries', 'classes'
    ], f"Invalid topic: {req.topic}"
    progress = get_user_progress(req.user_id)
    progress.increment(req.topic, req.amount)
    return ProgressResponse(
        user_id=progress.user_id,
        general_level=progress.general_level,
        topic_levels=progress.topic_levels
    )

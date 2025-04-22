from pydantic import BaseModel
from typing import Optional

class ExerciseRequest(BaseModel):
    language: str
    skill_level: int
    skill: Optional[str] = None

class ExerciseResponse(BaseModel):
    code: str
    description: str
    example_input: str
    example_output: str
    learning_goal: str

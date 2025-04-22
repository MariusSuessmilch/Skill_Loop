from fastapi import FastAPI
from app.api.endpoints import exercises, code_execution, feedback, progress, auth, assistant

app = FastAPI()

app.include_router(exercises.router, prefix="/api/exercises")
app.include_router(code_execution.router, prefix="/api/code")
app.include_router(feedback.router, prefix="/api/feedback")
app.include_router(progress.router, prefix="/api/progress")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(assistant.router, prefix="/api/assistant")

from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
import openai

router = APIRouter()

# Use the same model as exercises and feedback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
OPENAI_MODEL = "gpt-4.1-mini-2025-04-14"  # Ensure this matches the other endpoints

# Use OpenAI v1+ client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class AssistantRequest(BaseModel):
    code: str
    question: str
    exercise: str = None
    role: str = "assistant"
    instruction: str = ""

@router.post("/")
async def ask_assistant(payload: AssistantRequest):
    prompt = f"{payload.instruction}\n\nAufgabe: {payload.exercise}\n\nCode des Nutzers:\n{payload.code}\n\nFrage: {payload.question}\n\nAntworte als hilfreicher, freundlicher Tutor. Gib Keine Lösungen/Teillösungen an, aber gebe Tipps dazu, welche Funktion zur Lösung verwendet werden könnte und ein Beispiel, wie diese genutzt wird (allerdings ohne eine Teillösung anzugeben!)"
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": payload.instruction},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        import traceback
        print("Assistant endpoint error:", traceback.format_exc())
        return JSONResponse(status_code=500, content={"answer": "Tut mir leid, es ist ein Fehler aufgetreten.", "error": str(e)})

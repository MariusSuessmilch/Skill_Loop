import os
from fastapi import APIRouter
from app.schemas import ExerciseRequest, ExerciseResponse
import openai
from fastapi.responses import JSONResponse
import re

router = APIRouter()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/", response_model=ExerciseResponse)
def generate_exercise(req: ExerciseRequest):
    language_map = {
        'en': 'English',
        'de': 'Deutsch',
        #'es': 'Spanish',
        #'uk': 'Ukrainian'
    }
    language_name = language_map.get(req.language, req.language)
    # Compose a new prompt for the AI to:
    # - Provide a full, motivating exercise description with a short intro and a concrete example for the topic
    # - Output ONLY short comments for the code editor, showing where to implement each part
    prompt = (
        f"Erstelle eine spannende, motivierende Coding-Aufgabe mit Fantasy/Gaming Genre zum Thema: {req.skill}. "
        f"Beachte, dass Aufgaben zu grundlegenden Konzepten keine Teilaufgaben enthalten dürfen, die komplexere Konzepte vorraussetzen. "
        f"Gib zuerst eine sehr kurze Einführung (1-2 Sätze) und ein konkretes code-Beispiel für das Thema, ohne dabei die Aufgabe vorweg zu nehmen."
        f"Formuliere dann die vollständige Aufgabenstellung für Schüler:innen. Verwende dabei keine optionalen oder Bonusaufgaben!" 
        f"Gib diese vollständige Aufgabenbeschreibung als schön formattierten Markdown-Text mit passenden Emojis im Feld 'description' zurück. "
        f"Erstelle zusätzlich ein Python-Code-Snippet, das ausschließlich aus kurzen Kommentaren besteht, die die einzelnen Teilaufgaben wiedergeben (KEINERLEI Lösung, KEIN Fließtext, KEIN Aufgabenbeschreibungstext im Code). "
        f"Beispiel für einen Kommentar: # 1. Lege eine Variable an\n# 2. Schreibe eine Schleife\n usw. "
        f"Die Aufgaben sollen mit wenigen Zeilen Code gelöst werden können. und dürfen niemals die input() funktion benötigen."
        f"Gib das Code-Snippet im Feld 'code' zurück. "
        f"Antwortformat: {{\"description\":\"...\", \"code\":\"...\"}}. "
        f"Sprache: Deutsch. Keine Lösungen, keine doppelten Inhalte."
    )
    response = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[{"role": "system", "content": "Du bist ein hilfreicher Coding Tutor für Schüler."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512,
    )
    content = response.choices[0].message.content
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        import json
        try:
            data = json.loads(match.group(0))
            code = data.get("code", "")
            description = data.get("description", "")
            return {
                "code": code,
                "description": description,
                "example_input": "",
                "example_output": "",
                "learning_goal": ""
            }
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": "Fehler beim Parsen der KI-Antwort.", "raw": content})
    else:
        return JSONResponse(status_code=500, content={"error": "Keine gültige JSON-Antwort von der KI erhalten.", "raw": content})

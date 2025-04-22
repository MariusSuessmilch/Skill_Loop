import os
import re
from fastapi import APIRouter
from pydantic import BaseModel
import openai
from app.models.progress import get_user_progress

router = APIRouter()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FeedbackRequest(BaseModel):
    code: str
    exercise: dict = None  # Full exercise object (description, requirements, etc.)

class FeedbackResponse(BaseModel):
    feedback: str
    solved: bool

@router.post("/", response_model=FeedbackResponse)
def get_feedback(req: FeedbackRequest):
    # --- Early exit: Leerer Code darf niemals als gelöst gelten ---
    if not req.code or not req.code.strip():
        feedback = "# Feedback\n\n⚠️ Du hast noch keinen Code eingegeben. Bitte schreibe deine Lösung in das Codefeld und versuche es erneut!\n\n**Tipp:** Starte mit einem Kommentar oder einer kleinen Codezeile, um loszulegen."
        return FeedbackResponse(feedback=feedback, solved=False)

    def is_only_comments(code: str) -> bool:
        for line in code.splitlines():
            striped = line.strip()
            if striped and not striped.startswith('#'):
                return False
        return True

    if is_only_comments(req.code):
        feedback = "# Feedback\n\n⚠️ Dein Code enthält bisher nur Kommentare, aber noch keine Lösungsschritte. Bitte schreibe echten Python-Code unter die Kommentare, um die Aufgabe zu lösen!\n\n**Tipp:** Starte mit einer Zuweisung oder einer print-Anweisung."
        return FeedbackResponse(feedback=feedback, solved=False)

    # Use the structured exercise object if available
    exercise_desc = None
    if req.exercise:
        # Prefer a 'description' field if present
        exercise_desc = req.exercise.get('description') or str(req.exercise)
    else:
        exercise_desc = None

    # Map language code to full language name
    language_map = {
        'en': 'English',
        'de': 'Deutsch',
        'es': 'Spanish',
        'uk': 'Ukrainian'
    }
    language_code = 'de'
    if exercise_desc:
        lang_marker = re.search(r'\[LANGUAGE:([a-z]{2})\]', exercise_desc, re.IGNORECASE)
        if lang_marker and lang_marker.group(1) in language_map:
            language_code = lang_marker.group(1)
        else:
            for code in language_map:
                if code in exercise_desc.lower() or language_map[code].lower() in exercise_desc.lower():
                    language_code = code
                    break
    language_name = language_map.get(language_code, 'Deutsch')

    # --- Custom system prompt for structured feedback ---
    system_prompt = f"""Überprüfe, ob der folgende Code die Anforderungen der angegebenen Aufgabe erfüllt. 
    Akzeptiere auch alternative, funktionierende Lösungen, solange sie das Ziel der Aufgabe erreichen – 
    Variablennamen, Reihenfolge oder kleine Abweichungen sind in Ordnung, wenn das Ergebnis stimmt. 
    Sei tolerant gegenüber unterschiedlichen Lösungswegen und bewerte nur dann als 'nicht gelöst', 
    wenn wirklich ein wesentlicher Teil fehlt oder die Lösung nicht funktioniert. 
    Beziehe dich ausschließlich auf die Angaben und Beispiele der Aufgabe. 
    Wenn alle Anforderungen erfüllt sind, gib einen JSON-Block {{\"solved\": true}} zurück UND IMMER 
    einen motivierenden, kurzen Feedback-Text in korrekt formatiertem Markdown mit passenden emojis, der 
    mit einer Markdown-Überschrift (z.B. # Feedback) beginnt (z.B. "Super gemacht! Du hast die Aufgabe korrekt gelöst.").

    Wichtig: Gib konstruktives, motivierendes Feedback.
    Gib an welche Aufgaben korrekt abgeschlossen wurden, und Hinweise, wie die nicht abgeschlossenen Aufgaben zu beenden sind. 
    Gib keine Teillösungen oder Lösungen an, sondern nur nützliche Hinweise, oder allgemeine Beispiele! 
    Strukturiere deine Antwort mit Markdown und Emojis. Das Niveau der Antwort soll für Schüler verständlich sein. 
    Nutze Emojis um zu zeigen, welche Aufgaben vollständig gelöst wurden und welche nicht. Halte dich kurz. Hier ein Beispiel: 
    Feedback zu deinem Code
    Aufgabe 1: Zahlen von 1 bis 10 ausgeben
    for i in range(1, 11):
        # TODO: Ausgabe der Zahl i
        pass

    🔄 Nicht abgeschlossen: Du hast die Schleife korrekt erstellt, die Zahlen von 1 bis 10 durchläuft. Jetzt musst du nur noch den print-Befehl verwenden, um die Zahl i auszugeben. Schau dir an, wie man in Python Ausgaben auf der Konsole macht!

    Aufgabe 2: Alle Elemente einer Liste ausgeben
    meine_liste = [3, 5, 7, 9, 11]

    for element in meine_liste:
        # TODO: Ausgabe des Elements
        pass

    🔄 Nicht abgeschlossen: Du hast die Schleife richtig eingerichtet, um durch die Liste zu iterieren. Auch hier fehlt nur noch der print-Befehl, um jedes Element der Liste auszugeben. Denk daran, dass element die einzelnen Werte der Liste repräsentiert!

    Tipps zum Weiterarbeiten
    🖨️ Ausgabe in Python: Um in Python etwas auszugeben, kannst du den print-Befehl verwenden. Zum Beispiel, um die Zahl i auszugeben, könntest du print(i) innerhalb der Schleife verwenden.
    📝 Dokumentation: Wenn du dir unsicher bist, wie etwas funktioniert, schau in der offiziellen Python-Dokumentation nach oder such online nach Beispielen.
    Du bist auf einem guten Weg! Mach weiter so und probiere die print-Anweisungen in deinen Schleifen aus. Du wirst sehen, wie schnell du Fortschritte machst! 🚀

    📝Einhaltung von Code-Prinzipien nach PEP8:
    Variablennamen sollten klein geschrieben werden.
    
    Viel Erfolg und bleib motiviert! 💪

    Wenn etwas fehlt, gib {{\"solved\": false}} zurück und beschreibe nur die fehlenden Teile, ebenfalls IMMER im 
    Markdown-Format mit Überschrift. Gib niemals Hinweise zu Aspekten, die nicht Teil der Aufgabe sind. 
    Schreibe **immer auf Deutsch**.\n\nWICHTIG: Gib NIEMALS die vollständige Lösung oder Korrekturen für 
    den Nutzer-Code an.\n\nHier ist die Aufgabe (inkl. Beispiele und Ziele):\n{exercise_desc}\n\nHier ist der Nutzer-Code:\n{req.code}\n\nAm Ende antworte 
    IMMER mit einem Markdown-Feedback und einem JSON-Block der Form {{\"solved\": true}} oder {{\"solved\": false}}.\n\nBeispiel: 
    Auch wenn im Beispiel 'for i in range(10):' steht, ist 'for zahl in range(10):' genauso korrekt, 
    solange die Aufgabe erfüllt wird."""

    # --- Progress tracking logic ---
    user_id = "demo_user"
    topic_keywords = ['variables','operators','if_else','loops','lists','functions','strings','dictionaries','classes']
    topic = next((t for t in topic_keywords if t in (exercise_desc or '').lower()), None)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": f"Aufgabenstellung: {exercise_desc}\nLösungscode:\n{req.code}\n\nAm Ende antworte mit einem JSON-Block der Form {{\"solved\": true}} oder {{\"solved\": false}}, je nachdem ob die Aufgabe korrekt gelöst wurde."}],
            temperature=0.5,
            max_tokens=500
        )
        feedback = response.choices[0].message.content
        solved = False
        match = re.search(r'\{\s*"solved"\s*:\s*(true|false)\s*\}', feedback)
        if match:
            solved = match.group(1) == 'true'
            # Remove JSON block from feedback for clean display, even if it's in a code block
            feedback = re.sub(r'```json[\s\S]*?\{\s*"solved"\s*:\s*(true|false)\s*\}[\s\S]*?```', '', feedback, flags=re.MULTILINE)
            feedback = re.sub(r'\n*\{\s*"solved"\s*:\s*(true|false)\s*\}\s*', '', feedback, flags=re.MULTILINE)
        # --- Clean up markdown output ---
        feedback = feedback.strip()
        # If no heading present, add one
        if not re.match(r'^#', feedback):
            feedback = '# Feedback\n' + feedback
        # Remove more than two consecutive blank lines
        feedback = re.sub(r'\n{3,}', '\n\n', feedback)
        # Fallback: if feedback is empty, add default text
        if not feedback:
            if solved:
                feedback = '# Feedback\n✅ Super gemacht! Du hast die Aufgabe korrekt gelöst.'
            else:
                feedback = '# Feedback\n❗ Bitte überprüfe deine Lösung – es fehlen noch wichtige Teile.'
        if topic and solved:
            progress = get_user_progress(user_id)
            progress.increment(topic)
        return FeedbackResponse(feedback=feedback, solved=solved)
    except Exception as e:
        return FeedbackResponse(feedback=f"Error: {str(e)}", solved=False)

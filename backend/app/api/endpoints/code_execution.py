from fastapi import APIRouter
from pydantic import BaseModel
from io import StringIO
import sys

router = APIRouter()

class CodeRequest(BaseModel):
    code: str

class CodeResponse(BaseModel):
    output: str

@router.post("/execute", response_model=CodeResponse)
def execute_code(req: CodeRequest):
    # TODO: Sandbox code execution
    try:
        exec_globals = {}
        exec_locals = {}
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(req.code, exec_globals, exec_locals)
        finally:
            sys.stdout = old_stdout
        output = mystdout.getvalue()
        if not output:
            # If nothing was printed, show variable states
            output = str(exec_locals)
        return CodeResponse(output=output)
    except Exception as e:
        return CodeResponse(output=str(e))

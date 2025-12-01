from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AutoRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str

class AutoResponse(BaseModel):
    suggestion: str


@router.post("/autocomplete", response_model=AutoResponse)
async def autocomplete(payload: AutoRequest):

    code = payload.code
    before_cursor = code[:payload.cursorPosition].rstrip()

    # ---------------------------
    # 1. Python-specific logic
    # ---------------------------
    if payload.language == "python":

        # 1. import autocomplete
        if before_cursor.endswith("import"):
            return {"suggestion": " os\nimport sys\nimport json"}

        # 2. from X import ...
        if "from " in before_cursor and before_cursor.endswith(" import"):
            return {"suggestion": " path, listdir"}

        # 3. function definition
        if before_cursor.endswith("def"):
            return {"suggestion": " function_name(param1, param2):\n    pass"}

        if before_cursor.endswith("def "):
            return {"suggestion": "function_name(param1):\n    pass"}

        # 4. class definition
        if before_cursor.endswith("class"):
            return {"suggestion": " MyClass:\n    def __init__(self):\n        pass"}

        if before_cursor.endswith("class "):
            return {"suggestion": "MyClass:\n    def __init__(self):\n        pass"}

        # 5. if statement
        if before_cursor.endswith("if"):
            return {"suggestion": " condition:\n    pass"}

        if before_cursor.endswith("if "):
            return {"suggestion": "condition:\n    pass"}

        # 6. for loops
        if before_cursor.endswith("for"):
            return {"suggestion": " i in range(10):\n    print(i)"}

        if before_cursor.endswith("for "):
            return {"suggestion": "i in items:\n    pass"}

        # 7. while loop
        if before_cursor.endswith("while"):
            return {"suggestion": " condition:\n    pass"}

        # 8. print statement pattern
        if before_cursor.endswith("print("):
            return {"suggestion": "'Hello World')"}

        # 9. list/dict comprehension
        if before_cursor.endswith("["):
            return {"suggestion": "x for x in range(10)]"}

        if before_cursor.endswith("{"):
            return {"suggestion": "key: value for key, value in items}"}

        # 10. detect self. attribute autocomplete
        if "self." in before_cursor.split("\n")[-1]:
            return {"suggestion": "method_name()"}

        # 11. pattern-based multi-line completion
        if "requests.get(" in code:
            return {
                "suggestion": (
                    "\nresponse = requests.get(url)\n"
                    "if response.status_code == 200:\n"
                    "    data = response.json()\n"
                    "    print(data)"
                )
            }

        # 12. Suggest common helper block
        if "try" in before_cursor:
            return {
                "suggestion": (
                    ":\n    # risky code\n    pass\n"
                    "except Exception as e:\n    print(e)"
                )
            }

        # 13. Detect main function structure
        if "if __name__" in before_cursor:
            return {"suggestion": "__ == '__main__':\n    main()"}

        # 14. Decorator autocomplete
        if before_cursor.endswith("@"):
            return {"suggestion": "staticmethod\n    def method():\n        pass"}

        # 15. Default fallback multi-line suggestion
        return {
            "suggestion": (
                "# TODO: implement logic here\n"
                "pass"
            )
        }

    # ---------------------------
    # 2. Add other languages here (TS, JS, Go, etc.)
    # ---------------------------
    return {"suggestion": ""}

from fastapi import  APIRouter

router = APIRouter()
@router.post("/generate/")
def generate_code(prompt: str):
    # Add code generation logic here
    return {"generated_code": "..."}

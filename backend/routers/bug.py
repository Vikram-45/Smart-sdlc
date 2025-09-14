from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import time

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = os.getenv("PROJECT_ID")
MODEL_ID = "ibm/granite-3-2b-instruct"

class BugFixRequest(BaseModel):
    code: str
    programming_language: str = "python"

class BugFixResponse(BaseModel):
    fixed_code: str
    processing_time: float
    raw_response: dict

async def get_bearer_token(api_key: str):
    token_url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()
        return response.json()["access_token"]

@router.post("/fix-bug/", response_model=BugFixResponse)
async def fix_bug_endpoint(req: BugFixRequest):
    try:
        if not req.code.strip():
            raise HTTPException(status_code=400, detail="Code input cannot be empty")

        bearer_token = await get_bearer_token(API_KEY)

        system_prompt = (
            f"You are an expert {req.programming_language} programmer and debugging specialist. "
            "Analyze the provided code and fix all bugs, including syntax errors, logic errors, runtime errors, "
            "performance issues, best practices violations, and security vulnerabilities. "
            "Return only the corrected code as plain text, without any explanations, markdown, or additional formatting."
        )

        user_message = f"Code to analyze and fix:\n{req.code}"

        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 4000,
            "presence_penalty": 0,
            "temperature": 0.1,
            "top_p": 1,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }

        start_time = time.time()
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"WatsonX AI API error: {response.text}")

        response_data = response.json()
        fixed_code = response_data.get("choices", [{}])[0].get("message", {}).get("content", req.code)
        processing_time = time.time() - start_time

        return BugFixResponse(
            fixed_code=fixed_code.strip(),
            processing_time=processing_time,
            raw_response=response_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Bug Fixer"}
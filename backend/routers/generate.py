from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Config
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://us-south.ml.cloud.ibm.com"  # adjust region if needed
PROJECT_ID = os.getenv("PROJECT_ID")  # put your project id in .env
MODEL_ID = "ibm/granite-3-2b-instruct"

# Request schema
class CodeGenRequest(BaseModel):
    prompt: str  # default to Python, can specify other languages

async def get_bearer_token(api_key: str):
    """Get IAM bearer token from IBM Cloud"""
    token_url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()
        return response.json()["access_token"]

@router.post("/generate-code/")
async def codegen_endpoint(req: CodeGenRequest):
    try:
        # Step 1: get bearer token
        bearer_token = await get_bearer_token(API_KEY)

        # Step 2: prepare request with a system prompt for code generation
        system_prompt = (
            f"Generate only the implementation code (do not include test cases, Do not wrap it in markdown (like ``` python ``` or explanations):\n{req.prompt}"
        )

        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 2000,
            "presence_penalty": 0,
            "temperature": 0.2,  # slightly higher for creative code generation
            "top_p": 1,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.prompt}
            ]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }

        # Step 3: make request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body)

        # Step 4: return response
        if response.status_code != 200:
            return {"error": response.text}

        # Extract the generated code from the response
        response_data = response.json()
        generated_code = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return {

            "generated_code": generated_code
        }

    except Exception as e:
        return {"error": str(e)}
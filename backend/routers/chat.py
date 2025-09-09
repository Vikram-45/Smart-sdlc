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
MODEL_ID = "ibm/granite-3-2-8b-instruct"

# Request schema
class ChatRequest(BaseModel):
    message: str


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


@router.post("/chat/")
async def chat_endpoint(req: ChatRequest):
    try:
        # Step 1: get bearer token
        bearer_token = await get_bearer_token(API_KEY)

        # Step 2: prepare request
        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 2000,
            "presence_penalty": 0,
            "temperature": 0,
            "top_p": 1,
            "messages": [
                {"role": "user", "content": req.message}
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

        return response.json()

    except Exception as e:
        return {"error": str(e)}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

router = APIRouter()

# Config
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://us-south.ml.cloud.ibm.com"  # adjust region if needed
PROJECT_ID = os.getenv("PROJECT_ID")  # put your project id in .env
MODEL_ID = "ibm/granite-3-2b-instruct"

# Request schema
class BugFixRequest(BaseModel):
    code: str
    programming_language: str = "python"  # default to Python
    error_message: Optional[str] = None
    description: Optional[str] = None

# Response schema
class BugFixResponse(BaseModel):
    original_code: str
    fixed_code: str
    explanation: str
    programming_language: str
    raw_response: dict

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

@router.post("/fix-bug/", response_model=BugFixResponse)
async def fix_bug_endpoint(req: BugFixRequest):
    """
    Fix bugs in the provided code using IBM WatsonX AI
    """
    try:
        # Step 1: Get bearer token
        bearer_token = await get_bearer_token(API_KEY)

        # Step 2: Prepare request with bug fixing prompt
        system_prompt = (
            f"You are an expert {req.programming_language} programmer and debugging specialist. "
            "Your task is to analyze the provided code, identify bugs, and provide a fixed version. "
            "Please provide your response in the following format:\n\n"
            "**FIXED CODE:**\n"
            "[Insert the corrected code here]\n\n"
            "**EXPLANATION:**\n"
            "[Explain what the bugs were and how you fixed them]\n\n"
            "Focus on:\n"
            "- Syntax errors\n"
            "- Logic errors\n"
            "- Runtime errors\n"
            "- Performance issues\n"
            "- Best practices violations\n"
            "- Security vulnerabilities\n"
            "Provide clean, working code without any markdown formatting or code blocks."
        )

        user_message = f"Code to fix:\n```{req.programming_language}\n{req.code}\n```"
        
        if req.error_message:
            user_message += f"\n\nError message encountered:\n{req.error_message}"
        
        if req.description:
            user_message += f"\n\nAdditional context:\n{req.description}"

        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 3000,
            "presence_penalty": 0,
            "temperature": 0.1,  # Lower temperature for more consistent bug fixing
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

        # Step 3: Make request to WatsonX AI
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=body)

        # Step 4: Process response
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"WatsonX AI API error: {response.text}")

        # Extract the bug fix result from the response
        response_data = response.json()
        ai_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Parse the AI response to extract fixed code and explanation
        fixed_code = ""
        explanation = ""
        
        if "**FIXED CODE:**" in ai_response and "**EXPLANATION:**" in ai_response:
            parts = ai_response.split("**FIXED CODE:**")[1].split("**EXPLANATION:**")
            fixed_code = parts[0].strip() if len(parts) > 0 else ""
            explanation = parts[1].strip() if len(parts) > 1 else ""
        else:
            # Fallback parsing
            lines = ai_response.split('\n')
            code_section = False
            explanation_section = False
            
            for line in lines:
                if "fixed code" in line.lower() or "corrected code" in line.lower():
                    code_section = True
                    explanation_section = False
                    continue
                elif "explanation" in line.lower() or "what" in line.lower() and "fix" in line.lower():
                    explanation_section = True
                    code_section = False
                    continue
                
                if code_section and line.strip():
                    fixed_code += line + "\n"
                elif explanation_section and line.strip():
                    explanation += line + "\n"
        
        # If parsing fails, use the entire response as explanation
        if not fixed_code and not explanation:
            explanation = ai_response
            fixed_code = req.code  # Return original code if no fixed version found
        
        return BugFixResponse(
            original_code=req.code,
            fixed_code=fixed_code.strip(),
            explanation=explanation.strip(),
            programming_language=req.programming_language,
            raw_response=response_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

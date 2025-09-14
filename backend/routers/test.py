from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from typing import Optional, List

# Load environment variables
load_dotenv()

router = APIRouter()

# Config
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://us-south.ml.cloud.ibm.com"  # Adjust region if needed
PROJECT_ID = os.getenv("PROJECT_ID")  # Put your project id in .env
MODEL_ID = "ibm/granite-3-2b-instruct"

# Request schema for generating test cases
class TestCaseGenerateRequest(BaseModel):
    code: str
    programming_language: str = "python"
    test_framework: Optional[str] = None  # e.g., "pytest", "unittest"
    description: Optional[str] = None

# Response schema for generating test cases
class TestCaseGenerateResponse(BaseModel):
    original_code: str
    generated_tests: str
    programming_language: str
    test_framework: str
    message: str
    raw_response: dict

# Request schema for checking test cases
class TestCaseCheckRequest(BaseModel):
    code: str
    test_cases: str
    programming_language: str = "python"
    test_framework: Optional[str] = None
    description: Optional[str] = None

# Response schema for checking test cases
class TestCaseCheckResponse(BaseModel):
    original_code: str
    original_tests: str
    test_analysis: str
    improved_tests: str
    coverage_suggestions: str
    programming_language: str
    test_framework: str
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

@router.post("/generate-test-cases/", response_model=TestCaseGenerateResponse)
async def generate_test_cases_endpoint(req: TestCaseGenerateRequest):
    """
    Generate comprehensive test cases for given code
    """
    try:
        # Validate input
        if not req.code.strip():
            raise HTTPException(status_code=400, detail="Code input cannot be empty")
        
        # Get bearer token
        bearer_token = await get_bearer_token(API_KEY)

        # Prepare request with test case generation prompt
        framework_info = f" using {req.test_framework}" if req.test_framework else ""
        system_prompt = (
            f"You are an expert {req.programming_language} testing specialist. "
            f"Generate comprehensive test cases{framework_info} for the provided code. "
            "Include:\n"
            "- Basic functionality tests\n"
            "- Edge cases and boundary conditions\n"
            "- Error handling tests\n"
            "- Performance considerations\n"
            "- Integration test suggestions\n"
            "Provide clean, executable test code without markdown formatting."
        )

        user_message = f"Generate comprehensive test cases for this {req.programming_language} code:\n```{req.programming_language}\n{req.code}\n```"
        if req.description:
            user_message += f"\n\nAdditional context:\n{req.description}"

        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 3000,
            "presence_penalty": 0,
            "temperature": 0.3,
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

        # Make request to WatsonX AI
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"WatsonX AI API error: {response.text}")

        response_data = response.json()
        generated_tests = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

        return TestCaseGenerateResponse(
            original_code=req.code,
            generated_tests=generated_tests.strip(),
            programming_language=req.programming_language,
            test_framework=req.test_framework or "standard",
            message="Test cases generated successfully",
            raw_response=response_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/check-test-cases/", response_model=TestCaseCheckResponse)
async def check_test_cases_endpoint(req: TestCaseCheckRequest):
    """
    Analyze and improve test cases using IBM WatsonX AI
    """
    try:
        # Validate input
        if not req.code.strip():
            raise HTTPException(status_code=400, detail="Code input cannot be empty")
        if not req.test_cases.strip():
            raise HTTPException(status_code=400, detail="Test cases cannot be empty")

        # Get bearer token
        bearer_token = await get_bearer_token(API_KEY)

        # Prepare request with test case analysis prompt
        system_prompt = (
            f"You are an expert {req.programming_language} developer and testing specialist. "
            "Your task is to analyze the provided code and test cases, then provide comprehensive feedback and improvements. "
            "Please provide your response in the following format:\n\n"
            "**TEST ANALYSIS:**\n"
            "[Analyze the current test cases - what they cover, what they miss, quality assessment]\n\n"
            "**IMPROVED TESTS:**\n"
            "[Provide improved/additional test cases that address the gaps]\n\n"
            "**COVERAGE SUGGESTIONS:**\n"
            "[Suggest specific test scenarios that should be covered]\n\n"
            "Focus on:\n"
            "- Test coverage completeness\n"
            "- Edge cases and boundary conditions\n"
            "- Error handling scenarios\n"
            "- Performance test considerations\n"
            "- Test code quality and maintainability\n"
            "- Best practices for the specified testing framework\n"
            "- Mock/stub usage where appropriate\n"
            "- Test data management\n"
            "Provide clean, well-structured test code without markdown formatting."
        )

        framework_info = f" using {req.test_framework}" if req.test_framework else ""
        user_message = f"""Code to test:
```{req.programming_language}
{req.code}
```

Existing test cases{framework_info}:
```{req.programming_language}
{req.test_cases}
```"""
        
        if req.description:
            user_message += f"\n\nAdditional context:\n{req.description}"

        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 4000,
            "presence_penalty": 0,
            "temperature": 0.2,
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

        # Make request to WatsonX AI
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"WatsonX AI API error: {response.text}")

        # Extract the test analysis result from the response
        response_data = response.json()
        ai_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Parse the AI response to extract different sections
        test_analysis = ""
        improved_tests = ""
        coverage_suggestions = ""
        
        # Try to parse structured response
        if "**TEST ANALYSIS:**" in ai_response:
            sections = ai_response.split("**TEST ANALYSIS:**")[1]
            if "**IMPROVED TESTS:**" in sections:
                parts = sections.split("**IMPROVED TESTS:**")
                test_analysis = parts[0].strip()
                remaining = parts[1]
                
                if "**COVERAGE SUGGESTIONS:**" in remaining:
                    test_parts = remaining.split("**COVERAGE SUGGESTIONS:**")
                    improved_tests = test_parts[0].strip()
                    coverage_suggestions = test_parts[1].strip()
                else:
                    improved_tests = remaining.strip()
            else:
                test_analysis = sections.strip()
        
        # Fallback parsing if structured format not found
        if not test_analysis and not improved_tests:
            lines = ai_response.split('\n')
            current_section = ""
            
            for line in lines:
                line_lower = line.lower().strip()
                if "analysis" in line_lower or "current test" in line_lower:
                    current_section = "analysis"
                    continue
                elif "improved" in line_lower or "better test" in line_lower or "additional test" in line_lower:
                    current_section = "improved"
                    continue
                elif "coverage" in line_lower or "suggestion" in line_lower or "recommend" in line_lower:
                    current_section = "coverage"
                    continue
                
                if line.strip():
                    if current_section == "analysis":
                        test_analysis += line + "\n"
                    elif current_section == "improved":
                        improved_tests += line + "\n"
                    elif current_section == "coverage":
                        coverage_suggestions += line + "\n"
        
        # If parsing completely fails, distribute content
        if not test_analysis and not improved_tests and not coverage_suggestions:
            sections = ai_response.split('\n\n')
            if len(sections) >= 3:
                test_analysis = sections[0]
                improved_tests = sections[1]
                coverage_suggestions = '\n\n'.join(sections[2:])
            else:
                test_analysis = ai_response
        
        return TestCaseCheckResponse(
            original_code=req.code,
            original_tests=req.test_cases,
            test_analysis=test_analysis.strip(),
            improved_tests=improved_tests.strip(),
            coverage_suggestions=coverage_suggestions.strip(),
            programming_language=req.programming_language,
            test_framework=req.test_framework or "standard",
            raw_response=response_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Test Generator"}
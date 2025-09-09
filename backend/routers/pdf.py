
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from typing import List, Dict

# Load environment variables
load_dotenv()

router = APIRouter()

# Config
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://us-south.ml.cloud.ibm.com"  # adjust region if needed
PROJECT_ID = os.getenv("PROJECT_ID")  # put your project id in .env
MODEL_ID = "ibm/granite-3-2b-instruct"

# Response schema
class SDLCClassificationResponse(BaseModel):
    extracted_text: str
    classified_sentences: str
    raw_response: dict

class SentenceClassification(BaseModel):
    sentence: str
    phase: str
    confidence: float = None

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

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        # Create a PDF document from bytes
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        extracted_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            extracted_text += page.get_text() + "\n"
        
        pdf_document.close()
        return extracted_text.strip()
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text from PDF: {str(e)}")

@router.post("/classify-pdf-sdlc/", response_model=SDLCClassificationResponse)
async def classify_pdf_sdlc(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract text, and classify each sentence into SDLC phases
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read PDF content
        pdf_content = await file.read()
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_content)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text found in the PDF")
        
        # Step 1: Get bearer token
        bearer_token = await get_bearer_token(API_KEY)

        # Step 2: Prepare request with SDLC classification prompt
        classification_prompt = (
            "Classify each sentence into specific SDLC phases such as Requirements, Design, Development, Testing, or Deployment. "
            "Analyze the following text and for each sentence, identify which SDLC phase it belongs to. "
            "Format your response as: 'Sentence: [sentence text] | Phase: [SDLC Phase]' for each sentence. "
            "If a sentence doesn't clearly fit into any SDLC phase, classify it as 'General' or 'Other'."
        )

        url = f"{BASE_URL}/ml/v1/text/chat?version=2023-05-29"
        body = {
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "frequency_penalty": 0,
            "max_tokens": 3000,
            "presence_penalty": 0,
            "temperature": 0.1,  # Lower temperature for more consistent classification
            "top_p": 1,
            "messages": [
                {"role": "system", "content": classification_prompt},
                {"role": "user", "content": f"Text to classify:\n\n{extracted_text}"}
            ]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }

        # Step 3: Make request to WatsonX AI
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=body)

        # Step 4: Process response
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"WatsonX AI API error: {response.text}")

        # Extract the classification result from the response
        response_data = response.json()
        classified_sentences = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return SDLCClassificationResponse(
            extracted_text=extracted_text,
            classified_sentences=classified_sentences,
            raw_response=response_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


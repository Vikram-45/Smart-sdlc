from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
import json
import os
from datetime import datetime
import uuid

router = APIRouter()

# Feedback storage directory
FEEDBACK_DIR = "feedback_data"
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, "feedback.json")

# Ensure feedback directory exists
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# Request schema
class FeedbackRequest(BaseModel):
    name: str
    feedback: str
    rating: int
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @validator('feedback')
    def validate_feedback(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Feedback must be at least 10 characters long')
        return v.strip()

# Response schema
class FeedbackResponse(BaseModel):
    message: str
    feedback_id: str
    timestamp: str

# Utility functions
def load_feedback_data():
    """Load feedback data from JSON file"""
    try:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading feedback data: {e}")
        return []

def save_feedback_data(feedback_list):
    """Save feedback data to JSON file"""
    try:
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving feedback data: {e}")
        return False

# API Endpoint
@router.post("/api/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest):
    """Submit new feedback"""
    try:
        # Load existing feedback
        feedback_list = load_feedback_data()
        
        # Create new feedback entry
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        new_feedback = {
            "id": feedback_id,
            "name": feedback.name,
            "feedback": feedback.feedback,
            "rating": feedback.rating,
            "timestamp": timestamp
        }
        
        # Add to list
        feedback_list.append(new_feedback)
        
        # Save to file
        if save_feedback_data(feedback_list):
            return FeedbackResponse(
                message="Feedback submitted successfully",
                feedback_id=feedback_id,
                timestamp=timestamp
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save feedback")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

# Health check endpoint

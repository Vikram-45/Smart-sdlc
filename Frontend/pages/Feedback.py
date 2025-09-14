import streamlit as st
import requests
import json
import time
from datetime import datetime

st.set_page_config(page_title="SmartSDLC - Feedback", layout="wide")

# --- Enhanced Global CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">

    <style>
        /* Hide Streamlit sidebar & default elements */
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="collapsedControl"] {display: none !important;}
        #MainMenu, header, footer {visibility: hidden;}
        
        /* Base styling */
        html, body, .stApp {
            background: #101014 !important;
            color: #f5f5f7 !important;
            font-family: 'Orbitron', sans-serif !important;
            margin: 0;
            padding-top: 80px !important;
        }
        
        /* Header styling */
        .smartsdlc-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 9999;
            background: linear-gradient(135deg, #101014 0%, #1a1a1e 100%);
            padding: 15px 20px;
            box-shadow: 0 2px 20px rgba(0,195,255,0.1);
            border-bottom: 1px solid #23232a;
        }
        
        .smartsdlc-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(120deg, #00c3ff, #7600bc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            display: inline-block;
        }
        
        /* Main container */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Page title with icon */
        .page-title {
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(120deg, #00c3ff, #7600bc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 2rem 0;
            text-shadow: 0 0 30px rgba(0, 195, 255, 0.3);
        }
        
        /* Feature card styling */
        .feature-card {
            background: linear-gradient(135deg, #18181c 0%, #1e1e24 100%);
            border-radius: 1.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid #23232a;
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00c3ff, #7600bc, #00c3ff);
            opacity: 0.7;
        }
        
        .feature-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 195, 255, 0.2);
            border-color: #00c3ff;
        }
        
        /* Form sections styling */
        .form-section {
            background: linear-gradient(135deg, #16161a 0%, #1c1c22 100%);
            border-radius: 1.2rem;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid #2a2a35;
            box-shadow: 0 6px 25px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        
        .form-section:hover {
            border-color: #00c3ff;
            box-shadow: 0 8px 30px rgba(0, 195, 255, 0.15);
        }
        
        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: #00c3ff;
            margin: 0 0 1.5rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(0, 195, 255, 0.3);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            background: #0d0d0f !important;
            color: #f5f5f7 !important;
            border: 2px solid #23232a !important;
            border-radius: 1rem !important;
            font-family: 'Orbitron', sans-serif !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #00c3ff !important;
            box-shadow: 0 0 20px rgba(0, 195, 255, 0.3) !important;
            background: #111115 !important;
        }
        
        .stTextArea > div > div > textarea {
            background: #0d0d0f !important;
            color: #f5f5f7 !important;
            border: 2px solid #23232a !important;
            border-radius: 1rem !important;
            font-family: 'Orbitron', sans-serif !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            padding: 1.2rem !important;
            resize: vertical !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #00c3ff !important;
            box-shadow: 0 0 20px rgba(0, 195, 255, 0.3) !important;
            background: #111115 !important;
        }
        
        /* Star Rating Styling */
        .star-rating {
            display: flex;
            gap: 0.5rem;
            margin: 1rem 0;
            align-items: center;
            justify-content: center;
        }
        
        .star {
            font-size: 2rem;
            color: #23232a;
            cursor: pointer;
            transition: all 0.3s ease;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .star:hover,
        .star.active {
            color: #ffd700;
            text-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
            transform: scale(1.2);
        }
        
        .star.active {
            animation: starGlow 0.5s ease;
        }
        
        @keyframes starGlow {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1.2); }
        }
        
        .rating-label {
            font-family: 'Orbitron', sans-serif;
            color: #b3b3b8;
            font-size: 1rem;
            margin-left: 1rem;
            font-weight: 600;
        }
        
        /* Rating categories */
        .rating-category {
            background: rgba(0, 195, 255, 0.05);
            border: 1px solid rgba(0, 195, 255, 0.2);
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .rating-category:hover {
            background: rgba(0, 195, 255, 0.1);
            border-color: rgba(0, 195, 255, 0.4);
        }
        
        .category-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #00c3ff;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #00c3ff, #7600bc) !important;
            color: white !important;
            border: none !important;
            border-radius: 1rem !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            padding: 1.2rem 4rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 25px rgba(0, 195, 255, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            width: 100% !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #7600bc, #00c3ff) !important;
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 15px 35px rgba(0, 195, 255, 0.6) !important;
        }
        
        /* Result container */
        .unified-result-container {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
            border-radius: 1.5rem;
            padding: 2.5rem;
            margin: 2rem 0;
            border: 1px solid #23232a;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
            text-align: center;
        }
        
        .unified-result-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00c851, #69f0ae, #00c851);
            opacity: 0.8;
        }
        
        .success-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: bounce 1s ease;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-30px); }
            60% { transform: translateY(-15px); }
        }
        
        .success-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: #69f0ae;
            margin-bottom: 1rem;
        }
        
        .success-message {
            font-family: 'Orbitron', sans-serif;
            color: #b3b3b8;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        /* Loading animation */
        .loading-container {
            text-align: center;
            padding: 3rem;
            background: rgba(0, 195, 255, 0.05);
            border-radius: 1rem;
            border: 2px dashed #00c3ff;
            margin: 2rem 0;
        }
        
        .loading-text {
            font-family: 'Orbitron', sans-serif;
            color: #00c3ff;
            font-size: 1.3rem;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        .loading-spinner {
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 4px solid #23232a;
            border-radius: 50%;
            border-top-color: #00c3ff;
            animation: spin 1s linear infinite;
            margin: 1rem 0;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Navigation buttons */
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 3rem 0 2rem 0;
            flex-wrap: wrap;
        }
        
        .nav-button {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: transparent;
            border: 2px solid #00c3ff;
            color: #00c3ff;
            padding: 0.8rem 1.5rem;
            border-radius: 1rem;
            text-decoration: none;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }
        
        .nav-button:hover {
            background: #00c3ff;
            color: #101014;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,195,255,0.4);
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-container {
                padding: 1rem;
            }
            
            .page-title {
                font-size: 2rem;
            }
            
            .feature-card, .form-section {
                padding: 1.5rem;
            }
            
            .star-rating {
                justify-content: flex-start;
            }
            
            .nav-buttons {
                flex-direction: column;
                align-items: center;
            }
        }
        
        a {
            text-decoration: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Backend Integration Class ---
class FeedbackBackend:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000/api/feedback"  # Correct endpoint
    
    def submit_feedback(self, feedback_data: dict) -> dict:
        """
        Submit feedback to backend via POST method
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                self.backend_url,
                json=feedback_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'message': response.json().get('message', 'Feedback submitted successfully!'),
                    'feedback_id': response.json().get('feedback_id', 'N/A'),
                    'timestamp': response.json().get('timestamp', datetime.now().isoformat())
                }
            else:
                return {
                    'success': False,
                    'error': f'Server error: {response.status_code} - {response.text}'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Failed to connect to backend: {str(e)}'
            }

# Initialize backend
@st.cache_resource
def get_feedback_backend():
    return FeedbackBackend()

feedback_backend = get_feedback_backend()

# --- Header ---
st.markdown("""
    <div class="smartsdlc-header">
        <div class="smartsdlc-title">🚀 SmartSDLC - Feedback</div>
    </div>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
    <div class="page-title">
        📬 Share Your Feedback
    </div>
""", unsafe_allow_html=True)

# --- Description Card ---
st.markdown("""
    <div class="feature-card">
        <p style="text-align: center; color: #b3b3b8; font-size: 1.2rem; margin: 0; line-height: 1.6; font-family:'Orbitron', sans-serif;">
            📝 Help us improve SmartSDLC by sharing your experience and suggestions<br>
            <span style="font-size: 1rem; color: #00c3ff;">✨ Your feedback drives our innovation</span>
        </p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for rating
if 'rating' not in st.session_state:
    st.session_state.rating = 0

# --- Personal Information Section ---
st.markdown("""
    <div class="form-section">
        <div class="section-title">
            👤 Personal Information
        </div>
    </div>
""", unsafe_allow_html=True)

# Name input
user_name = st.text_input(
    "",
    placeholder="Enter your full name...",
    key="user_name",
    label_visibility="collapsed"
)

# --- Rating Section ---
st.markdown("""
    <div class="form-section">
        <div class="section-title">
            ⭐ Rate Your Experience
        </div>
    </div>
""", unsafe_allow_html=True)

def create_star_rating(category, current_rating, key):
    """Create interactive star rating component"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        stars_col = st.columns(5)
        for i in range(5):
            with stars_col[i]:
                star_value = i + 1
                if st.button("⭐", key=f"{key}_{star_value}", help=f"Rate {star_value} stars"):
                    st.session_state[key] = star_value
    
    with col2:
        rating_text = ["Poor", "Fair", "Good", "Very Good", "Excellent"]
        if current_rating > 0:
            st.markdown(f'<div class="rating-label">{rating_text[current_rating-1]}</div>', unsafe_allow_html=True)

# Single Overall Rating
st.markdown("""
    <div class="rating-category">
        <div class="category-title">🌟 Overall Experience</div>
    </div>
""", unsafe_allow_html=True)
create_star_rating("Overall Experience", st.session_state.rating, "rating")

# --- Feedback Section ---
st.markdown("""
    <div class="form-section">
        <div class="section-title">
            💬 Your Detailed Feedback
        </div>
    </div>
""", unsafe_allow_html=True)

feedback_input = st.text_area(
    "",
    placeholder="""Share your thoughts and suggestions...

What did you like most about SmartSDLC?
What features would you like to see improved?
Any bugs or issues you encountered?
Suggestions for new functionality?
How can we make your experience better?

Your detailed feedback helps us build better tools for developers!""",
    height=200,
    key="feedback_input",
    label_visibility="collapsed"
)

# --- Submit Button ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Submit Feedback"):
        # Validation
        if not user_name.strip():
            st.error("⚠️ Please enter your name")
        elif len(user_name.strip()) < 2:
            st.error("⚠️ Name must be at least 2 characters long")
        elif not feedback_input.strip():
            st.error("⚠️ Please share your feedback")
        elif len(feedback_input.strip()) < 10:
            st.error("⚠️ Feedback must be at least 10 characters long")
        elif st.session_state.rating == 0:
            st.error("⚠️ Please provide a rating")
        else:
            # Create placeholder for result
            result_placeholder = st.empty()
            
            # Show loading
            result_placeholder.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">📤 Submitting your feedback...</div>
                    <p style="color: #b3b3b8; margin-top: 1rem; font-family: 'Orbitron', sans-serif;">
                        Processing • Saving • Almost done...
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Prepare feedback data to match backend schema
            feedback_data = {
                "name": user_name.strip(),
                "feedback": feedback_input.strip(),
                "rating": st.session_state.rating
            }
            
            # Submit to backend
            result = feedback_backend.submit_feedback(feedback_data)
            
            if result.get('success'):
                # Show success message
                result_placeholder.markdown(f"""
                    <div class="unified-result-container">
                        <div class="success-icon">🎉</div>
                        <div class="success-title">Thank You, {user_name}!</div>
                        <div class="success-message">
                            Your feedback has been successfully submitted!<br><br>
                            <strong>Feedback ID:</strong> {result.get('feedback_id', 'N/A')}<br>
                            <strong>Rating:</strong> {'⭐' * st.session_state.rating} ({st.session_state.rating}/5)<br>
                            <strong>Timestamp:</strong> {result.get('timestamp')}<br><br>
                            We truly appreciate your time and input. Your suggestions help us make SmartSDLC better for everyone!
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Reset form
                # st.session_state.rating = 0
                # st.session_state.user_name = ""
                # st.session_state.feedback_input = ""
                
                # # Auto-refresh after 3 seconds
                # time.sleep(3)
                # st.experimental_rerun()
                
            else:
                result_placeholder.error(f"❌ Error: {result.get('error', 'Unknown error occurred')}")

# --- Navigation Buttons ---
st.markdown("""
    <div class="nav-buttons">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/Code_Generator" class="nav-button">💻 Code Generator</a>
        <a href="/Bug_Fixer" class="nav-button">🐛 Bug Fixer</a>
        <a href="/Test_Generator" class="nav-button">🧪 Test Generator</a>
        <a href="/ChatBot" class="nav-button">🤖 Chat Bot</a>
        <a href="/Upload_and_Classify" class="nav-button">📁 Upload and Classify</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
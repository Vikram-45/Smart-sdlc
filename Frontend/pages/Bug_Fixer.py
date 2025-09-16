import streamlit as st
import requests
import time
import json

st.set_page_config(page_title="SmartSDLC - Bug Fixer", layout="wide")

# --- Enhanced Global CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">

""", unsafe_allow_html=True)



def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call with your file name
load_css("style/bug.css")




# --- Backend Integration Class ---
class BugFixerBackend:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000/fix-bug/"

    def send_to_backend(self, code: str, programming_language: str = "python") -> dict:
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            payload = {
                'code': code,
                'programming_language': programming_language,
                'analysis_type': 'comprehensive'
            }
            response = requests.post(
                self.backend_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code in [200, 201]:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {'error': 'Invalid JSON response from backend'}
            else:
                return {'error': f'Backend error: {response.status_code} - {response.text}'}
        except requests.exceptions.RequestException as e:
            return {'error': f'Failed to connect to backend: {str(e)}'}

# Initialize backend
@st.cache_resource
def get_bug_fixer():
    return BugFixerBackend()

bug_fixer = get_bug_fixer()

# --- Header ---
st.markdown("""
    <div class="smartsdlc-header">
        <div class="smartsdlc-title">🐛 SmartSDLC - Bug Fixer</div>
    </div>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
    <div class="page-title">
        🐛 AI Bug Fixer
    </div>
""", unsafe_allow_html=True)

# --- Description Card ---
st.markdown("""
    <div class="feature-card">
        <p style="text-align: center; color: #b3b3b8; font-size: 1.2rem; margin: 0; line-height: 1.6; font-family:'Orbitron', sans-serif;">
            🔍 Automatically detect, analyze, and fix bugs in your code<br>
            <span style="font-size: 1rem; color: #00c3ff;">✨ Powered by AI • Real-time Analysis • Comprehensive Fixes</span>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Code Input Section ---
st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
            📝 Paste Your Buggy Code or Upload File
        </h3>
    </div>
""", unsafe_allow_html=True)

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Upload a code file (.py, .js, .java, etc.)",
    type=["py", "js", "java", "cpp", "cs"],
    key="code_file"
)

# --- Text Area for Code Input ---
code = st.text_area(
    "",
    placeholder="""# Paste your buggy code here or upload a file...
# Example:
def calculate_average(numbers):
    sum = 0
    for i in range(len(numbers) + 1):  # Bug: IndexError
        sum += numbers[i]
    return sum / len(numbers)

# The AI will detect and fix issues like:
# - Index out of range errors
# - Logic errors
# - Type mismatches
# - Performance issues
# - Security vulnerabilities""",
    height=300,
    key="bug_code_input"
)

# Process uploaded file
if uploaded_file is not None:
    try:
        code = uploaded_file.read().decode("utf-8")
        st.session_state.bug_code_input = code
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

# --- Fix Button with Backend Integration ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔧 Analyze & Fix Bugs"):
        if not code.strip():
            st.error("⚠️ Please provide code by pasting it or uploading a file")
        else:
            result_placeholder = st.empty()
            result_placeholder.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">🤖 AI is analyzing your code...</div>
                </div>
            """, unsafe_allow_html=True)
            
            result = bug_fixer.send_to_backend(code)
            
            result_placeholder.empty()  # Clear the loading animation
            
            
            # Check for error in response
            if 'error' in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                # Extract fields
                fixed_code = result.get('fixed_code', code)
                processing_time = result.get('processing_time', 'N/A')
                raw_response = result.get('raw_response', {})
                warnings = raw_response.get('system', {}).get('warnings', [])
                
                
                # Display fixed code
                if fixed_code and fixed_code != code:
                    st.markdown("""
                        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem;">
                            🛠️ Fixed Code
                        </h3>
                    """, unsafe_allow_html=True)
                    st.code(fixed_code, language="python")
                else:
                    st.success("🎉 No bugs found or no changes made to your code!")
                
                # Display response metadata
                
# --- Navigation Buttons ---
st.markdown("""
    <div class="nav-buttons">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/Code_Generator" class="nav-button">🚀 Code Generator</a>
        <a href="/Test_Generator" class="nav-button">🧪 Test Generator</a>
        <a href="/Chat_Bot" class="nav-button">🤖 Chat Bot</a>
        <a href="/Upload_and_Classify" class="nav-button">📁 Upload and Classify</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
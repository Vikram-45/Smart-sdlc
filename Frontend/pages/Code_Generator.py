import streamlit as st
import requests
import json

st.set_page_config(page_title="SmartSDLC - Code Generator", layout="wide")
def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call with your file name
load_css("style/code_generator.css")

# --- Enhanced Global CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="smartsdlc-header">
        <div class="smartsdlc-title">🚀 SmartSDLC - Code Generator</div>
    </div>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
    <div class="page-title">
        🚀 AI Code Generator
    </div>
""", unsafe_allow_html=True)

# --- Description Card ---
st.markdown("""
    <div class="feature-card">
        <p style="text-align: center; color: #b3b3b8; font-size: 1.2rem; margin: 0; line-height: 1.6; font-family:'Orbitron', sans-serif;">
            ✍️ Generate clean, efficient, and functional code based on your requirements<br>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Code Requirements Input Section ---
st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
            📝 Describe Your Code Requirements
        </h3>
    </div>
""", unsafe_allow_html=True)

# Language selection

code_requirements = st.text_area(
    "",
    placeholder="""# Describe what you want the code to do...
# Example:
# Create a Python function that:
# - Takes a list of integers as input
# - Returns a sorted list in ascending order
# - Handles edge cases like empty lists or non-integer inputs
# - Uses type hints for better clarity""",
    height=300,
    key="code_requirements_input"
)

# --- Generate Button ---
if st.button("🚀 Generate Code"):
    if code_requirements.strip():
        # API call with loading animation
        API_URL = "http://localhost:8000/generate-code/"  # Adjust to your FastAPI server URL
        with st.spinner("Generating code..."):
            try:
                payload = {
                    "prompt": code_requirements,
                }
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                data = response.json()

                # Check for error in response
                if "error" in data:
                    st.markdown(f"""
                        <div class="stError">
                            Error: {data['error']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Display generated code
                    code = data.get("generated_code", "")
                    st.markdown(f"""
                        
                            <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
                                Generated Code
                            </h3>
                        
                    """, unsafe_allow_html=True)
                    st.code(code)
            except requests.RequestException as e:
                st.markdown(f"""
                    <div class="stError">
                        Failed to connect to API: {str(e)}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="stError">
                Please enter code requirements.
            </div>
        """, unsafe_allow_html=True)
# --- Navigation Buttons ---
st.markdown("""
    <div class="nav-buttons">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/Bug_Fixer" class="nav-button">🐛 Bug Fixer</a>
        <a href="/Test_Generator" class="nav-button">🧪 Test Generator</a>
        <a href="/Chat_Bot" class="nav-button">🤖 Chat bot</a>
        <a href="/Upload_and_Classify" class="nav-button">📁 Upload and Classify</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
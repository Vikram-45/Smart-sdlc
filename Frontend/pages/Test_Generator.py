import streamlit as st
import requests
import time

st.set_page_config(page_title="SmartSDLC - Test Generator", layout="wide")

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
        
        /* Input styling (for file uploader and text area) */
        .stFileUploader > div > div > div > input {
            background: #0d0d0f !important;
            color: #f5f5f7 !important;
            border: 2px solid #23232a !important;
            border-radius: 1rem !important;
            font-family: 'Courier New', monospace !important;
            font-size: 0.9rem !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader > div > div > div > input:focus {
            border-color: #00c3ff !important;
            box-shadow: 0 0 20px rgba(0, 195, 255, 0.3) !important;
            background: #111115 !important;
        }
        
        .stTextArea > div > div > textarea {
            background: #0d0d0f !important;
            color: #f5f5f7 !important;
            border: 2px solid #23232a !important;
            border-radius: 1rem !important;
            font-family: 'Courier New', monospace !important;
            font-size: 0.9rem !important;
            line-height: 1.6 !important;
            padding: 1rem !important;
            resize: vertical !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #00c3ff !important;
            box-shadow: 0 0 20px rgba(0, 195, 255, 0.3) !important;
            background: #111115 !important;
        }
        
        /* File uploader button styling */
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #00c3ff, #7600bc) !important;
            color: white !important;
            border: none !important;
            border-radius: 1rem !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.8rem 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 25px rgba(0, 195, 255, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            outline: none !important;
        }
        
        div[data-testid="stFileUploader"] button:hover {
            background: linear-gradient(135deg, #7600bc, #00c3ff) !important;
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 15px 35px rgba(0, 195, 255, 0.6) !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #00c3ff, #7600bc) !important;
            color: white !important;
            border: none !important;
            border-radius: 1rem !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            padding: 1rem 3rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 25px rgba(0, 195, 255, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #7600bc, #00c3ff) !important;
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 15px 35px rgba(0, 195, 255, 0.6) !important;
        }
        
        /* Result container */
        .result-container {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
            border-radius: 1.5rem;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid #23232a;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
        }
        
        .result-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00c851, #69f0ae, #00c851);
            opacity: 0.8;
        }
        
        /* Code block styling */
        .stCode {
            background: #0a0a0c !important;
            border: 1px solid #23232a !important;
            border-radius: 1rem !important;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.3) !important;
        }
        
        /* Success/Error styling */
        .stSuccess {
            background: linear-gradient(135deg, #1b2d1b 0%, #0f1b0f 100%) !important;
            color: #69f0ae !important;
            border: 1px solid #2e7d32 !important;
            border-radius: 1rem !important;
        }
        
        .stError {
            background: linear-gradient(135deg, #2d1b1b 0%, #1b0f0f 100%) !important;
            color: #ff7777 !important;
            border: 1px solid #d32f2f !important;
            border-radius: 1rem !important;
        }
        
        /* Loading animation */
        .loading-container {
            text-align: center;
            padding: 2rem;
            background: rgba(0, 195, 255, 0.05);
            border-radius: 1rem;
            border: 1px dashed #00c3ff;
            margin: 2rem 0;
        }
        
        .loading-text {
            font-family: 'Orbitron', sans-serif;
            color: #00c3ff;
            font-size: 1.2rem;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        .loading-spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
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
            
            .feature-card {
                padding: 1.5rem;
            }
            
            .nav-buttons {
                flex-direction: column;
                align-items: center;
            }
            a {
                text-decoration: none;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- Backend Integration Class ---
class TestGeneratorBackend:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000/generate-test-cases/"

    def generate_test_cases(self, code: str, programming_language: str = "python", test_framework: str = None) -> dict:
        """
        Submit code to backend to generate test cases
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            data = {
                "code": code,
                "programming_language": programming_language,
                "test_framework": test_framework
            }
            
            response = requests.post(
                self.backend_url,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'data': response.json()
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
def get_test_generator_backend():
    return TestGeneratorBackend()

backend = get_test_generator_backend()

# --- Header ---
st.markdown("""
    <div class="smartsdlc-header">
        <div class="smartsdlc-title">🚀 SmartSDLC - Test Generator</div>
    </div>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
    <div class="page-title">
        🧪 AI Test Generator
    </div>
""", unsafe_allow_html=True)

# --- Description Card ---
st.markdown("""
    <div class="feature-card">
        <p style="text-align: center; color: #b3b3b8; font-size: 1.2rem; margin: 0; line-height: 1.6; font-family:'Orbitron', sans-serif;">
            🧪 Generate comprehensive test cases for your code<br>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
            📝 Provide Code or Upload File
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
code_input = st.text_area(
    "",
    placeholder="""# Paste your code here or upload a file...
# Example:
# def add_numbers(a: int, b: int) -> int:
#     return a + b

# The AI will generate:
# - Unit tests for the provided code
# - Edge case coverage
# - Documentation for test cases
# - Adherence to testing best practices""",
    height=300,
    key="code_input"
)

# Process uploaded file
if uploaded_file is not None:
    try:
        code_input = uploaded_file.read().decode("utf-8")
        st.session_state.code_input = code_input
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

# --- Generate Tests Button ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Generate Tests"):
        if not code_input.strip():
            st.error("⚠️ Please provide code by pasting it or uploading a file")
        else:
            # Create placeholder for result
            result_placeholder = st.empty()
            
            # Show loading animation
            result_placeholder.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">🤖 AI is generating your tests...</div>
                    <p style="color: #b3b3b8; margin-top: 1rem;">
                        Analyzing code • Generating test cases • Optimizing output
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Submit to backend
            result = backend.generate_test_cases(
                code=code_input,
                programming_language="python",  # Default to Python, can be extended for other languages
                test_framework="pytest"  # Default to pytest
            )
            
            if result.get('success'):
                # Display results
                result_placeholder.markdown("""
                    <div class="result-container">
                        <h3 style="color: #69f0ae; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
                            ✅ Generated Test Cases
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display original code
                st.markdown("**Original Code**")
                st.code(result['data']['original_code'], language="python")
                
                # Display generated tests
                st.markdown("**Generated Test Cases**")
                st.code(result['data']['generated_tests'], language="python")
                
                # Display message
                st.success(result['data']['message'])
                
                # Reset form
                
                
            else:
                result_placeholder.error(f"❌ Error: {result.get('error', 'Unknown error occurred')}")

# --- Navigation Buttons ---
st.markdown("""
    <div class="nav-buttons">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/Code_Generator" class="nav-button">💻 Code Generator</a>
        <a href="/Bug_Fixer" class="nav-button">🐛 Bug Fixer</a>
        <a href="/ChatBot" class="nav-button">🤖 Chat Bot</a>
        <a href="/Upload_and_Classify" class="nav-button">📁 Upload and Classify</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
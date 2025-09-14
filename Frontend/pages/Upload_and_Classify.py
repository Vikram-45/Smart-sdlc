import streamlit as st
import requests
import json
import re

st.set_page_config(page_title="SmartSDLC - Upload and Classify", layout="wide")

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
        
        /* SDLC Phase Cards */
        .phase-card {
            background: linear-gradient(135deg, #1a1a1f 0%, #232329 100%);
            border-radius: 1rem;
            margin: 1rem 0;
            border: 1px solid #34343a;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .phase-card:hover {
            border-color: #00c3ff;
            box-shadow: 0 8px 25px rgba(0, 195, 255, 0.15);
        }
        
        .phase-header {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #34343a;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .phase-content {
            padding: 1.5rem;
        }
        
        .sentence-item {
            background: rgba(0,0,0,0.2);
            border-radius: 0.5rem;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0;
            border-left: 2px solid rgba(0, 195, 255, 0.3);
            font-size: 0.95rem;
            line-height: 1.5;
            transition: all 0.2s ease;
        }
        
        .sentence-item:hover {
            background: rgba(0, 195, 255, 0.05);
            border-left-color: #00c3ff;
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
            
            .result-container {
                padding: 1.5rem;
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

# Configuration
API_BASE_URL = "http://localhost:8000"

# Function to make API request
def classify_pdf(uploaded_file):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        with st.spinner("🤖 AI is analyzing your PDF..."):
            response = requests.post(f"{API_BASE_URL}/classify-pdf-sdlc/", files=files, timeout=120)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the API server. Please ensure the FastAPI server is running.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The file might be too large or the server is busy.")
        return None
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        return None

# Function to parse classified sentences string into a dictionary
def parse_classified_sentences(classified_sentences: str) -> dict:
    try:
        # Initialize dictionary for SDLC phases
        result = {
            "requirements": [],
            "design": [],
            "development": [],
            "testing": [],
            "deployment": [],
            "general": [],
            "other": []
        }
        
        # Split the string into lines, handling numbered or unnumbered formats
        lines = classified_sentences.strip().split("\n")
        
        # Regex to match "Sentence: [text] | Phase: [phase]" with optional numbering
        pattern = r"(?:\d+\.\s*)?Sentence:\s*(.*?)\s*\|\s*Phase:\s*([^|]+)"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                sentence = match.group(1).strip()
                phase = match.group(2).strip().lower()
                # Map phase to one of the expected keys, default to 'other' if unrecognized
                phase_key = phase if phase in result else "other"
                result[phase_key].append(sentence)
            else:
                # Log unparseable lines for debugging
                st.warning(f"⚠️ Could not parse line: {line}")
        
        return result
    except Exception as e:
        st.error(f"❌ Failed to parse classified sentences: {str(e)}")
        return {}

# --- Header ---
st.markdown("""
    <div class="smartsdlc-header">
        <div class="smartsdlc-title">🚀 SmartSDLC - Upload and Classify</div>
    </div>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
    <div class="page-title">
        📁 AI PDF SDLC Classifier
    </div>
""", unsafe_allow_html=True)

# --- Description Card ---
st.markdown("""
    <div class="feature-card">
        <p style="text-align: center; color: #b3b3b8; font-size: 1.2rem; margin: 0; line-height: 1.6; font-family:'Orbitron', sans-serif;">
            📤 Upload PDF files and let AI classify content into SDLC phases<br>
            <span style="color: #00c3ff; font-size: 1rem;">Requirements • Design • Development • Testing • Deployment</span>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- File Upload Section ---
st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
            📤 Upload Your PDF File
        </h3>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["pdf"],
    key="file_uploader"
)

# --- Debug Toggle ---
# debug_mode = st.checkbox("Show raw backend response for debugging", value=False)

# --- Classify Button ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Classify PDF"):
        if uploaded_file is not None:
            # Loading animation
            result_placeholder = st.empty()
            result_placeholder.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">🤖 AI is classifying your PDF...</div>
                    <p style="color: #b3b3b8; margin-top: 1rem;">
                        Extracting text • Analyzing content • Classifying sentences
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Make API call
            result = classify_pdf(uploaded_file)
            
            # Clear loading animation
            result_placeholder.empty()
            
            if result and "classified_sentences" in result:
                # Display raw response if debug mode is enabled
                # if debug_mode:
                #     st.subheader("Raw Backend Response")
                #     st.code(json.dumps(result, indent=2))
                
                # Parse the classified_sentences string
                classified_sentences = parse_classified_sentences(result["classified_sentences"])
                
                if not any(classified_sentences.values()):
                    st.error("❌ No valid classifications found. Raw backend response:")
                    st.code(json.dumps(result, indent=2))
                else:
                    # Start result container
                    st.markdown("""
                        <div class="result-container">
                            <h2 style="color: #00c851; font-family: 'Orbitron', sans-serif; text-align: center; margin-bottom: 2rem;">
                                ✅ Classification Results
                            </h2>
                    """, unsafe_allow_html=True)
                    
                    # Define SDLC phases and their display colors
                    phases = [
                        ("Requirements", "#ff6b35"),
                        ("Design", "#00c3ff"),
                        ("Development", "#69f0ae"),
                        ("Testing", "#ffca28"),
                        ("Deployment", "#ab47bc"),
                        ("General", "#b0bec5"),
                        ("Other", "#78909c")
                    ]
                    
                    # Display each phase with its sentences
                    for phase, color in phases:
                        sentences = classified_sentences.get(phase.lower(), [])
                        if sentences:
                            st.markdown(f"""
                                <div class="phase-card">
                                    <div class="phase-header">
                                        <span style="font-size: 1.5rem;">📋</span>
                                        <span style="color: {color}; font-family: 'Orbitron', sans-serif;">{phase}</span>
                                    </div>
                                    <div class="phase-content">
                            """, unsafe_allow_html=True)
                            
                            for sentence in sentences:
                                st.markdown(f"""
                                    <div class="sentence-item">
                                        {sentence}
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("</div></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="phase-card">
                                    <div class="phase-header">
                                        <span style="font-size: 1.5rem;">📋</span>
                                        <span style="color: {color}; font-family: 'Orbitron', sans-serif;">{phase}</span>
                                    </div>
                                    <div class="phase-content">
                                        <div class="sentence-item">
                                            No sentences classified for this phase.
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Close result container
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("❌ Failed to classify the PDF. Please check the file and try again.")
                if result:
                    st.error("Raw backend response:")
                    st.code(json.dumps(result, indent=2))
        else:
            st.warning("⚠️ Please upload a PDF file first!")

# Show file info if uploaded
if uploaded_file is not None:
    st.info(f"📁 **File uploaded:** {uploaded_file.name} ({uploaded_file.size} bytes)")

# --- Navigation Buttons ---
st.markdown("""
    <div class="nav-buttons">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/Code_Generator" class="nav-button">💻 Code Generator</a>
        <a href="/Bug_Fixer" class="nav-button">🐛 Bug Fixer</a>
        <a href="/Test_Generator" class="nav-button">🧪 Test Generator</a>
        <a href="/ChatBot" class="nav-button">🤖 Chat Bot</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
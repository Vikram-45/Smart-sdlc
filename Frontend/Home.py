import streamlit as st
from streamlit_lottie import st_lottie
import json, os

st.set_page_config(page_title="SmartSDLC Dashboard", layout="wide")
st.sidebar.empty()

# Also hide the toggle button
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="collapsedControl"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)
# Inject font + style
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">

    <div style="
            display: flex;
            align-items: center;
            justify-content: start;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 9999;
            background: #101014;
            border-bottom: 1px solid #23232a;
            padding: 1rem 2rem;
        ">
    <h1 style="
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #00c3ff, #7600bc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: left;
        margin: 0;">
        SmartSDLC
    </h1>
    </div>
""", unsafe_allow_html=True)


# Hide Streamlit junk
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}

        html, body, .stApp {
            background: #101014 !important;
            color: #f5f5f7 !important;
            font-family: 'Orbitron', sans-serif !important;
            margin: 0;  
        }
        .ai-hero{
            border-radius: 1rem;
            padding: 1rem;
        }

        .feature-card {
            background: #18181c;
            border-radius: 1rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #23232a;
            text-align: center;
            transition: all 0.25s ease;
        }
        .feature-card:hover {
            transform: translateY(-6px) scale(1.03);
            box-shadow: 0 12px 24px rgba(0,195,255,0.25);
            border-color: #00c3ff;
        }
        .card-button {
            background: transparent;
            border: none;
            font-size: 1.2rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            color: #00c3ff;
            cursor: pointer;
            width: 100%;
            padding: 1rem;
            border-radius: 0.8rem;
            transition: all 0.25s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Load lottie animation
def load_lottie_file(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

lottie_path = os.path.join(os.path.dirname(__file__), "lottie", "developer skills.json")
lottie_json = load_lottie_file(lottie_path)
st_lottie(lottie_json, height=300, key="ai-hero")

# Hero
st.markdown("""
    <h1 style="
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #00c3ff, #7600bc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
    ">
        SmartSDLC
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #b3b3b8;
        text-align: left;
        max-width: 800px;
        margin:20px;">
        <b>SmartSDLC</b> is an AI-driven platform that automates the 
        <span style="color:#00c3ff; font-weight:600;">Software Development Lifecycle</span>.  
    </p>
""", unsafe_allow_html=True)

# Features list
features = [
    {"title": "Upload & Classify Requirements", "page": "Upload_and_Classify"},
    {"title": "Code Generator", "page": "Code_Generator"},
    {"title": "Test Generator", "page": "Test_Generator"},
    {"title": "Bug Fixer", "page": "Bug_Fixer"},
    {"title": "Chat Bot", "page": "Chat_Bot"},
    {"title": "Feedback", "page": "Feedback"},
]

cols = st.columns(3)
for idx, feature in enumerate(features):
    with cols[idx % 3]:
        st.markdown(f"""
            <div class="feature-card">
                <form action="/{feature['page']}" target="_self">
                    <button class="card-button" type="submit">{feature['title']}</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

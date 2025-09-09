import streamlit as st
import requests
import json


st.set_page_config(page_title="SmartSDLC - Chatbot", layout="wide")
st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
        """, unsafe_allow_html=True)


API_BASE_URL = "http://127.0.0.1:8000/"  
CHAT_ENDPOINT = f"{API_BASE_URL}/chat/"
def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call with your file name
load_css("style/chatbot.css")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

# Function to call the chat API
def call_chat_api(message: str):
    """Call the FastAPI chat endpoint"""
    try:
        payload = {"message": message}
        response = requests.post(
            CHAT_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "message": f"API Error {response.status_code}: {response.text}"
            }
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "Request timed out. Please try again."
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "message": "Could not connect to the API server. Please check if the server is running."
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"An unexpected error occurred: {str(e)}"
        }



# --- Header ---
st.markdown("""
    <div class="smartsdlc-header">
        <div class="smartsdlc-title">🚀 SmartSDLC - Chatbot</div>
    </div>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
    <div class="page-title">
        🤖 AI Chatbot
    </div>
""", unsafe_allow_html=True)

# --- Description Card ---
st.markdown("""
    <div class="feature-card">
        <h3 style="text-align: center; color: #b3b3b8; font-size: 1.2rem; margin: 0; line-height: 1.6; font-family:'Orbitron', sans-serif;">
            💬 Interact with our AI to get instant coding assistance and answers
        </h3>
    </div>
""", unsafe_allow_html=True)

# --- Chat Display Section ---
st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
            💬 Chat History
        </h3>
    </div>
""", unsafe_allow_html=True)


chat_container = st.container()
with chat_container:
    if st.session_state.chat_history:
        # Use st.markdown for the container
        
        for message in st.session_state.chat_history:
                    
                if message['role'] == 'user':
                    # Clean content and convert newlines to <br>
                    clean_content = message['content'].replace('\n', '<br>')
                    st.markdown(f'''
                    <div class="chat-message user-message">
                        <strong>👤 You:</strong><br>
                        {clean_content}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                elif message['role'] == 'assistant':
                    # Clean content and convert newlines to <br>
                    clean_content = message['content'].replace('\n', '<br>')
                    st.markdown(f'''
                    <div class="chat-message ai-message">
                        <strong>🤖 AI Assistant:</strong><br>
                        {clean_content}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                elif message['role'] == 'error':
                    # Clean content and convert newlines to <br>
                    clean_content = message['content'].replace('\n', '<br>')
                    st.markdown(f'''
                    <div class="chat-message error-message">
                        <strong>❌ Error:</strong><br>
                        {clean_content}
                    </div>
                    ''', unsafe_allow_html=True)
       
    else:
        st.markdown("""
                <p style="color: #b3b3b8; font-size: 1rem; text-align: center;font-family: 'Orbitron', sans-serif;">
                    Your conversation with the AI will appear here...</p>""", unsafe_allow_html=True)

# --- Chat Input Section ---
st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #00c3ff; font-family: 'Orbitron', sans-serif; font-size: 1.5rem; margin-bottom: 1rem;">
            📩 Send a Message
        </h3>
    </div>
""", unsafe_allow_html=True)

# Create columns for input and buttons
col1, col2 = st.columns([3, 1])

with col1:
    chat_input = st.text_input(
        "",
        placeholder="Type your message or question here...",
        key=f"chat_input_{st.session_state.message_count}",  # Dynamic key to force refresh
        disabled=st.session_state.is_loading
    )

with col2:
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

# --- Send Message Button ---
if st.button("🚀 Send Message", disabled=st.session_state.is_loading or not chat_input.strip()):
    if chat_input.strip():
        # Set loading state
        st.session_state.is_loading = True
        
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': chat_input.strip()
        })
        
        # Show loading animation
        with st.spinner("🤖 AI is processing your message..."):
            # Call the API
            response = call_chat_api(chat_input.strip())
            
            if response.get('error'):
                # Add error message to chat history
                st.session_state.chat_history.append({
                    'role': 'error',
                    'content': response['message']
                })
            else:
                # Add AI response to chat history
                # IBM Watson ML uses OpenAI-compatible response format
                try:
                    ai_response = response['choices'][0]['message']['content']
                    if not ai_response or ai_response.strip() == "":
                        ai_response = "Empty response received from AI"
                except (KeyError, IndexError, TypeError) as e:
                    ai_response = f"Error parsing response: {str(e)}. Full response: {json.dumps(response, indent=2)}"
                ai_response = ai_response.strip()

                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response
                })
        
        # Reset loading state and increment message count to clear input
        st.session_state.is_loading = False
        st.session_state.message_count += 1  # This will create a new input widget with empty value
        
        # Rerun to update display
        st.rerun()

st.markdown("""
    <div class="nav-buttons">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/Code_Generator" class="nav-button" >💻 Code Generator</a>
        <a href="/Bug_Fixer" class="nav-button">🐛 Bug Fixer</a>
        <a href="/Test_Generator" class="nav-button">🧪 Test Generator</a>
        <a href="/Code_Summarizer" class="nav-button">📊 Code Summarizer</a>
        <a href="/Upload_and_Classify" class="nav-button">📁 Upload and Classify</a>
        <a href="/Feedback" class="nav-button">📬 Feedback</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container

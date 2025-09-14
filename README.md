# 🚀 SmartSDLC

A comprehensive AI-powered Software Development Lifecycle (SDLC) tool that helps developers with code generation, bug fixing, testing, and document classification.

## ✨ Features

- **🤖 AI Code Generator**: Generate code snippets and functions using IBM Watson AI
- **🐛 Bug Fixer**: Automated bug detection and fixing suggestions
- **🧪 Test Generator**: Generate comprehensive test cases for your code
- **💬 Chat Bot**: Interactive AI assistant for development queries
- **📄 PDF Classification**: Upload and classify documents into SDLC phases
- **📝 Feedback System**: Collect and manage user feedback




## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- IBM Watson AI account
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smartsdlc.git
   cd smartsdlc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example backend/.env
   ```
   Edit `backend/.env` with your IBM Watson credentials:
   - `API_KEY`: Your IBM Watson API key
   - `PROJECT_ID`: Your Watson project ID
   - `URL`: Regional endpoint URL

4. **Start the backend server**
   ```bash
   cd backend
   python main.py
   ```

5. **Start the frontend (in a new terminal)**
   ```bash
   streamlit run Frontend/Home.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`


## 📖 Usage

### Code Generator
- Navigate to the Code Generator page
- Enter your code requirements
- Get AI-generated code snippets

### Bug Fixer
- Paste your buggy code
- Receive automated bug detection and fixes

### Test Generator
- Input your code
- Generate comprehensive test cases

### PDF Classifier
- Upload PDF documents
- Get content classified into SDLC phases:
  - Requirements
  - Design
  - Development
  - Testing
  - Deployment

### Chat Bot
- Ask development-related questions
- Get AI-powered assistance


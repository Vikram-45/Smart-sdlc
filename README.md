# 🚀 SmartSDLC

A comprehensive AI-powered Software Development Lifecycle (SDLC) tool that helps developers with code generation, bug fixing, testing, and document classification.

## ✨ Features

- **🤖 AI Code Generator**: Generate code snippets and functions using IBM Watson AI
- **🐛 Bug Fixer**: Automated bug detection and fixing suggestions
- **🧪 Test Generator**: Generate comprehensive test cases for your code
- **💬 Chat Bot**: Interactive AI assistant for development queries
- **📄 PDF Classification**: Upload and classify documents into SDLC phases
- **📝 Feedback System**: Collect and manage user feedback

## 🏗️ Project Structure

```
smartsdlc/
├── backend/                 # FastAPI backend
│   ├── routers/            # API route handlers
│   │   ├── chat.py         # Chat functionality
│   │   ├── pdf.py          # PDF processing
│   │   └── feedback.py     # Feedback system
│   ├── main.py             # FastAPI application
│   └── .env                # Environment variables
├── Frontend/               # Streamlit frontend
│   ├── pages/              # Application pages
│   ├── static/             # CSS and assets
│   └── Home.py             # Main application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

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

## 🔧 Configuration

### IBM Watson Setup

1. Create an IBM Cloud account
2. Set up a Watson Machine Learning instance
3. Create a project in watsonx.ai
4. Get your API credentials from Service Credentials
5. Update the `.env` file with your credentials

### Regional Endpoints

- **US South**: `https://us-south.ml.cloud.ibm.com`
- **EU Germany**: `https://eu-de.ml.cloud.ibm.com`
- **EU UK**: `https://eu-gb.ml.cloud.ibm.com`
- **Asia Pacific**: `https://jp-tok.ml.cloud.ibm.com`
- **Australia**: `https://au-syd.ml.cloud.ibm.com`

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

## 🛠️ API Endpoints

- `POST /chat/` - Chat with AI assistant
- `POST /classify-pdf-sdlc/` - Classify PDF content
- `POST /classify-text-sdlc/` - Classify text content
- `POST /submit-feedback/` - Submit user feedback
- `GET /models/` - List available AI models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/smartsdlc/issues) page
2. Create a new issue with detailed information
3. Use the feedback system within the application

## 🙏 Acknowledgments

- IBM Watson AI for powering the AI features
- Streamlit for the frontend framework
- FastAPI for the backend framework
- PyMuPDF for PDF processing

---

**Made with ❤️ for developers by developers**
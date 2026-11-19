# Mahesh AI Resume Assistant 💼🤖

A modern, text-based interactive AI chatbot application built with **Python**, **Streamlit**, and the **Google Gemini API** (powered by the modern `google-genai` Python SDK). The assistant is strictly grounded on the verified professional background, education, projects, certifications, and technical skills of **Mahesh Darapureddy**.

---

## 👨‍💻 Candidate Overview: Mahesh Darapureddy

- **Official Portfolio**: [https://maheshdarapureddy.in](https://maheshdarapureddy.in)
- **Role**: AI Developer, Full-Stack Software Engineer, ServiceNow CSA & CAD Certified
- **Education**: 
  - **B.Tech in Electronics & Communication Engineering (ECE)** — BVCITS (2022–2026), **CGPA 7.5**
  - **Intermediate (MPC)** — Educare Junior College (2020–2022), **GPA 7.4**
  - **SSC (10th Standard)** — Educare E.M School (2020), **GPA 9.8**
- **Certifications**:
  - **ServiceNow Certified System Administrator (CSA)**
  - **ServiceNow Certified Application Developer (CAD)**
- **Internships**:
  - Python Development — AICTE
  - Python Full Stack — Eduskills
  - Frontend Development — AICTE

### 🚀 Live Featured Projects
| Project | Tech Stack | Live Demo |
| :--- | :--- | :--- |
| **Multi-Modal AI Chatbot** | Next.js, FastAPI, MongoDB, RBAC, Clerk, GPT-4.1, GPT-4o-mini, Gemini 2.0 Pro, DeepSeek V3 | [chat.maheshdarapureddy.in](https://chat.maheshdarapureddy.in) |
| **AI Analyzer** | Next.js, FastAPI, LangChain, HuggingFace Embeddings, GPT-4.1, BeautifulSoup, Clerk | [chatai.maheshdarapureddy.in](https://chatai.maheshdarapureddy.in) |
| **Diabetes Predictor** | Next.js, Flask, MongoDB, Machine Learning, Clerk | [diabetes.maheshdarapureddy.in](https://diabetes.maheshdarapureddy.in) |
| **Kidney Stone Detection** | HTML, CSS, JavaScript, Flask, TensorFlow, Keras (CNN) | [detect.maheshdarapureddy.in](https://detect.maheshdarapureddy.in) |

---

## ✨ Features & Architecture

1. **Modern, Responsive Streamlit UI**:
   - Custom styling with clean gradients, card containers, and profile badges.
   - Fully responsive on desktop and mobile screens.
2. **Text-Based Only**:
   - Focused, clean text conversational interface without voice or microphone clutter.
3. **Strict Grounding (Anti-Hallucination)**:
   - Powered by `resume.txt` as the sole source of truth.
   - The assistant never invents facts, past employers, or unlisted credentials.
   - If an inquiry is not covered in the resume, it honestly informs the user and directs them to Mahesh's portfolio.
4. **Interview-Style Answers**:
   - Responds articulately to common interview questions (*"Tell me about yourself"*, *"What are your strengths?"*, *"Why should we hire Mahesh?"*).
5. **Interactive Suggested Questions**:
   - Clickable quick-action buttons for immediate queries about skills, projects, certifications, and background.
6. **Persistent Chat History & Clear Button**:
   - Tracks the entire conversational session with one-click chat reset.
7. **Secure API Key Management**:
   - Automatically reads `GEMINI_API_KEY` from `.env`, environment variables, or Streamlit secrets.
   - Alternatively allows visitors to safely enter their API key directly in the sidebar.
8. **Latest Supported Gemini Models**:
   - Configured with high-speed, modern Gemini models (`gemini-3.1-flash-lite`, `gemini-3.5-flash-lite`, `gemini-3.5-flash`, `gemini-3.8-flash`) with automatic fallback.
9. **Streaming Responses**:
   - Real-time token streaming for a fast, snappy user experience.

---

## 📁 Project Structure

```
mahesh_chatbot/
├── .env.example          # Sample environment configuration template
├── .gitignore             # Git ignore rules (protects API keys & virtual envs)
├── app.py                # Main Streamlit application and Gemini SDK integration
├── README.md             # Comprehensive setup, run, and usage documentation
├── requirements.txt      # Python dependencies
└── resume.txt            # Candidate resume knowledge base (source of truth)
```

---

## 🛠️ Windows Installation & Setup Guide

Follow these step-by-step instructions to run the chatbot locally on Windows.

### Prerequisites
- **Python 3.10, 3.11, or 3.12** installed on Windows.
  *(Ensure "Add python.exe to PATH" was checked during Python installation)*
- A free **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

### Step 1: Open Terminal in Project Directory
Open **PowerShell** or **Command Prompt** and navigate to the project directory:
```powershell
cd "c:\Users\Mahesh Darapureddy\Downloads\mahesh_chatbot"
```

---

### Step 2: Create & Activate a Virtual Environment (Recommended)
Creating an isolated virtual environment keeps dependencies clean:

```powershell
# Create virtual environment named 'venv'
python -m venv venv

# Activate virtual environment on Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

> **Note for PowerShell execution policy**: If you see an error about script execution being disabled, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Or in **Command Prompt (cmd.exe)**, run:
> ```cmd
> venv\Scripts\activate.bat
> ```

---

### Step 3: Install Required Dependencies
Install the required packages using `pip`:

```powershell
pip install -r requirements.txt
```

This installs:
- `streamlit` (Modern web application framework)
- `google-genai` (Official modern Google GenAI Python SDK)
- `python-dotenv` (Loads environment variables from `.env`)

---

### Step 4: Configure your Google Gemini API Key

You have two easy options to configure your API key:

#### Option A: Using `.env` File (Recommended)
1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
2. Open `.env` in any text editor (Notepad, VS Code) and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
   ```

#### Option B: Through the Streamlit Sidebar
If you prefer not creating a `.env` file, simply start the app and paste your Gemini API key into the **Gemini API Configuration** input in the left sidebar. The key is securely held only in the browser session memory.

---

### Step 5: Run the Chatbot
Start the Streamlit application by running:

```powershell
streamlit run app.py
```

Your default web browser will automatically open to:
```
http://localhost:8501
```

---

## 💬 Example Questions to Try

You can type any question or click the suggested buttons:
- *"Tell me about Mahesh's educational background and his CGPA."*
- *"What projects has Mahesh deployed live?"*
- *"Explain his experience with ServiceNow and which certifications he holds."*
- *"What technologies did he use to build the Multi-Modal AI Chatbot?"*
- *"Give me an interview response: Why should we hire Mahesh?"*
- *"What machine learning and deep learning models has he developed?"*
- *"What is Mahesh's favorite food?"* *(Watch the assistant honestly state that this is not in his verified resume!)*

---

## 🔒 Security & Privacy
- **No hardcoded secrets**: API keys are never stored in source code.
- **`.gitignore` protected**: The `.env` file and sensitive local directories are excluded from Git commits.
- **Strict Guardrails**: Prevents prompt injection and information fabrication by bounding answers strictly to `resume.txt`.

---

## 📜 License
Developed for Mahesh Darapureddy. All rights reserved.
For portfolio and contact details, visit [https://maheshdarapureddy.in](https://maheshdarapureddy.in).

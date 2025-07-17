# 🧠 AI Document Verification API

This FastAPI-powered service automatically detects the type of uploaded documents (e.g., CDL, Medical Card, COI, etc.) and uses **Google Gemini AI** to extract required fields into a clean, structured JSON response.

---

## 🚀 Features

- 🔍 Auto-detects document type
- 📄 Extracts relevant fields as structured JSON
- 🤖 Uses Google Gemini LLM for extraction
- ⚡ Built with FastAPI for speed and scalability
- 🧪 Easily testable and extendable

---

## 📁 Supported Document Types

- `cdl` – Commercial Driver’s License  
- `medical_card` – DOT Medical Examiner Certificate  
- `coi` – Certificate of Insurance  
- `operating_authority` – FMCSA Operating Authority  
- `w9` – IRS W-9 Form  
- `broker_authority` – Broker Authority Letter  
- `surety_bond` – Freight Broker Surety Bond

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Hammadwakeel/TMS.git
cd TMS
````

### 2. Create and activate virtual environment

#### For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### For Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the sample environment file and configure your API key:

```bash
cp .env.sample .env
```

Then update the `.env` file:

```
API_KEY=your_google_gemini_api_key
```

---

## 🧪 Running the Server

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

---

## 📤 Usage Example

Send a file using `curl`:

```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/upload
```

Or use tools like **Postman** to send a `POST` request to:

```
http://localhost:8000/upload
```

The API will:

* Auto-detect the document type
* Extract fields using Gemini
* Return a structured JSON object

---

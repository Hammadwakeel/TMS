# AI Document Verification API

This service auto‐detects the uploaded document type (CDL, Medical Card, COI, etc.)
and uses Google Gemini to extract required fields into a JSON response.

## Getting Started

1. Copy `.env.sample` → `.env` and set `API_KEY`.
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`
4. POST a file to `http://localhost:8000/upload`.

Supported document types:
- cdl
- medical_card
- coi
- operating_authority
- w9
- broker_authority
- surety_bond

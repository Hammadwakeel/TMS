# app/OCR/document_processor.py

import json
import logging
from typing import List, Dict
from fastapi import HTTPException

from app.OCR.extractor import extract_text_with_prompt
from app.OCR.image_utils import convert_pdf_to_images, load_image_from_bytes
from app.OCR.prompts import (
    DOC_NAME_PROMPT,
    CDL_PROMPT,
    MEDICAL_CARD_PROMPT,
    COI_PROMPT,
    OPERATING_AUTHORITY_PROMPT,
    W9_PROMPT,
    BROKER_AUTHORITY_PROMPT,
    SURETY_BOND_PROMPT,
)

logger = logging.getLogger("app.OCR.document_processor")

# Map detected document type to its extraction prompt
SUPPORTED = {
    "cdl": CDL_PROMPT,
    "medical_card": MEDICAL_CARD_PROMPT,
    "coi": COI_PROMPT,
    "operating_authority": OPERATING_AUTHORITY_PROMPT,
    "w9": W9_PROMPT,
    "broker_authority": BROKER_AUTHORITY_PROMPT,
    "surety_bond": SURETY_BOND_PROMPT,
}

def process_images(file_bytes: bytes, is_pdf: bool) -> List:
    """
    Convert the uploaded bytes into a list of PIL.Image objects.
    If PDF, generate one image per page; otherwise load single image.
    """
    logger.debug(f"process_images called (is_pdf={is_pdf})")
    if is_pdf:
        images = convert_pdf_to_images(file_bytes)
    else:
        images = [load_image_from_bytes(file_bytes)]
    logger.debug(f"Number of image(s) to process: {len(images)}")
    return images

def detect_document_type(image) -> str:
    """
    Identify the document type by calling Gemini with DOC_NAME_PROMPT.
    Returns one of the keys in SUPPORTED.
    """
    logger.info("Detecting document type")
    raw = extract_text_with_prompt(image, DOC_NAME_PROMPT)
    name = raw.strip().lower()
    logger.info(f"Detected document type: '{name}'")
    if name not in SUPPORTED:
        logger.error(f"Unsupported document type detected: '{name}'")
        raise HTTPException(status_code=400, detail=f"Unsupported document type: '{name}'")
    return name

def extract_structured(prompt: str, image) -> Dict:
    """
    Run Gemini with the given prompt + image, extract the first {...} block,
    and parse it as JSON.
    """
    logger.info("Extracting structured data")
    raw = extract_text_with_prompt(image, prompt)
    cleaned = raw.strip()
    logger.debug(f"Raw payload from GenAI:\n{cleaned!r}")

    # Find the JSON object boundaries
    start = cleaned.find('{')
    end = cleaned.rfind('}')
    if start == -1 or end == -1 or start > end:
        logger.error("Could not locate JSON object in GenAI response", extra={"response": cleaned})
        raise HTTPException(
            status_code=500,
            detail=f"Failed to locate JSON object in GenAI response. Raw: {cleaned}"
        )

    json_text = cleaned[start:end+1]
    logger.debug(f"Extracted JSON text:\n{json_text}")

    try:
        data = json.loads(json_text)
        logger.debug(f"Parsed JSON data: {data}")
        return data
    except json.JSONDecodeError as e:
        logger.error("JSON parsing error", exc_info=e, extra={"json_text": json_text})
        raise HTTPException(
            status_code=500,
            detail=f"GenAI returned invalid JSON. Extracted: {json_text}"
        )

def process_document(file_bytes: bytes, is_pdf: bool) -> Dict:
    """
    Full end-to-end processing:
      1) Turn file into images
      2) Detect document type on first image
      3) Extract structured JSON with the matching prompt
    Returns a dict: {"doc_type": <type>, "data": <parsed JSON>}
    """
    logger.info("Starting document processing")
    images = process_images(file_bytes, is_pdf)
    doc_type = detect_document_type(images[0])
    prompt = SUPPORTED[doc_type]
    data = extract_structured(prompt, images[0])
    logger.info(f"Completed extraction for document type: {doc_type}")
    return {"doc_type": doc_type, "data": data}

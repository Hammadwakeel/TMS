import time
import logging
from fastapi import HTTPException
from google import genai
from google.genai.errors import ClientError
from app.OCR.config import API_KEY

logger = logging.getLogger("app.OCR.extractor")
client = genai.Client(api_key=API_KEY)

def extract_text_with_prompt(image, prompt: str) -> str:
    """
    Calls Gemini with the given prompt + image, with retry on 429.
    Returns the raw text response.
    """
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        logger.debug(f"Attempt {attempt}/{max_retries} for extract_text_with_prompt")
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[prompt, image]
            )
            logger.info("Received response from Gemini")
            return resp.text
        except ClientError as e:
            code = e.args[0] if e.args and isinstance(e.args[0], int) else None
            logger.warning(f"GenAI ClientError (code={code}) on attempt {attempt}: {e}")
            if code == 429 and attempt < max_retries:
                backoff = 2 ** attempt
                logger.info(f"Rate limited, backing off for {backoff}s")
                time.sleep(backoff)
                continue
            logger.error("Raising HTTPException due to GenAI error", exc_info=e)
            raise HTTPException(status_code=500, detail=f"GenAI error: {str(e)}")
    logger.critical("Exhausted all retries for GenAI call")
    raise HTTPException(status_code=503, detail="API resource exhausted. Try again later.")

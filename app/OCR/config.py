import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("app.OCR.config")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    logger.error("API_KEY environment variable is not set")
    raise ValueError("API_KEY environment variable is not set")
else:
    logger.info("API_KEY successfully loaded")

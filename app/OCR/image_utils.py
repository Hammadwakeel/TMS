import io
import logging
import PIL.Image
from pdf2image import convert_from_bytes
from fastapi import HTTPException

logger = logging.getLogger("app.OCR.image_utils")

def convert_pdf_to_images(pdf_bytes: bytes):
    logger.info("Converting PDF bytes to images")
    try:
        images = convert_from_bytes(pdf_bytes, dpi=200)
        logger.info(f"Converted PDF to {len(images)} image(s)")
        return images
    except Exception as e:
        logger.error("Error converting PDF to images", exc_info=e)
        raise HTTPException(status_code=500, detail=f"Error converting PDF: {e}")

def load_image_from_bytes(image_bytes: bytes):
    logger.info("Loading image from bytes")
    try:
        img = PIL.Image.open(io.BytesIO(image_bytes))
        logger.info(f"Image format detected: {img.format}, size: {img.size}")
        return img
    except Exception as e:
        logger.error("Uploaded file is not a valid image", exc_info=e)
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

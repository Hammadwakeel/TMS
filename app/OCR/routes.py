import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.OCR.document_processor import process_document

logger = logging.getLogger("app.OCR.routes")
router = APIRouter()

@router.post("/upload", summary="Upload a document and auto-extract fields")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"Received upload request: filename={file.filename}")
    if not file.filename:
        logger.error("No file provided in upload")
        raise HTTPException(status_code=400, detail="No file provided")

    contents = await file.read()
    is_pdf = file.filename.lower().endswith(".pdf")
    logger.debug(f"File treated as PDF: {is_pdf}")

    try:
        result = process_document(contents, is_pdf)
    except HTTPException as he:
        logger.warning(f"HTTPException during processing: {he.detail}")
        raise
    except Exception as e:
        logger.exception("Unexpected error during document processing")
        raise HTTPException(status_code=500, detail=str(e))

    logger.info(f"Successfully processed document: type={result['doc_type']}")
    return JSONResponse(content=result)

@router.get("/", summary="Health check")
def root():
    logger.info("Health check endpoint called")
    return {"message": "AI Document Verification API is running"}

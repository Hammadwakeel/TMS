import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.OCR.routes import router as ocr_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("app.main")

app = FastAPI(title="AI Document Verification API")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AI Document Verification API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception during request")
    return JSONResponse(status_code=500, content={"detail": str(exc)})

app.include_router(ocr_router)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down AI Document Verification API")

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends

from app.preprocessing import process_file
from app.extraction import (
    test_gemini,
    extract_marksheet_from_image
)

from app.auth import (
    create_access_token,
    verify_token
)

app = FastAPI(
    title="Marksheet Extractor API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Marksheet Extractor API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/test-gemini")
def gemini_test():
    return {
        "response": test_gemini()
    }


@app.post("/token")
def generate_token():
    return {
        "access_token": create_access_token(),
        "token_type": "bearer"
    }


@app.post("/extract")
async def extract_marksheet(
    file: UploadFile = File(...),
    _: bool = Depends(verify_token)
):
    allowed_types = (
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf"
    )

    if not file.filename.lower().endswith(allowed_types):
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and PDF files are allowed"
        )

    file_bytes = await file.read()

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB"
        )

    pages = process_file(
        file_bytes,
        file.filename
    )

    result = extract_marksheet_from_image(
        pages[0]
    )

    return {
        "filename": file.filename,
        "pages_processed": len(pages),
        "extracted_data": result
    }
from fastapi import UploadFile, File, APIRouter
import fitz

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes= await file.read()
    text=""
    doc = fitz.open( stream=file_bytes, filetype="pdf" )
    for page in doc:
        text += page.get_text()
    return {"text": text}

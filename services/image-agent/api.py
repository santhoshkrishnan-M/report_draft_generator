"""
FastAPI service for medical image analysis
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import tempfile
import json
from pathlib import Path

from image_processor import process_diagnostic_image

app = FastAPI(title="Medical Image Analysis Service")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("/tmp/medical_images")
UPLOAD_DIR.mkdir(exist_ok=True)

class ImageAnalysisResponse(BaseModel):
    status: str
    image_type: str
    observations: list
    features: Dict[str, Any]
    image_dimensions: Dict[str, int]
    disclaimer: str

@app.get("/")
async def root():
    return {
        "service": "Medical Image Analysis Service",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    image_type: str = Form(default="xray"),
    patient_id: Optional[str] = Form(default=None),
    study_date: Optional[str] = Form(default=None)
):
    """
    Analyze a medical diagnostic image
    
    Parameters:
    - file: Image file (JPEG, PNG, BMP)
    - image_type: Type of image (xray, mri, ct)
    - patient_id: Optional patient identifier
    - study_date: Optional study date
    
    Returns:
    - Structured observations and features
    """
    
    # Validate image type
    valid_types = ['xray', 'mri', 'ct']
    if image_type.lower() not in valid_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid image_type. Must be one of: {valid_types}"
        )
    
    # Validate file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed: {allowed_extensions}"
        )
    
    try:
        # Save uploaded file temporarily
        file_path = UPLOAD_DIR / f"{patient_id or 'temp'}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Prepare metadata
        metadata = {
            "patient_id": patient_id,
            "study_date": study_date,
            "filename": file.filename
        }
        
        # Process image
        result = process_diagnostic_image(
            str(file_path),
            image_type,
            metadata
        )
        
        # Clean up temporary file (optional - keep for review)
        # os.remove(file_path)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

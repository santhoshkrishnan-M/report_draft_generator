"""
Medical Report Workflow Steps
Handles image upload and analysis workflow
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os
import importlib.util

# Import image processor dynamically
def get_image_processor():
    spec = importlib.util.spec_from_file_location(
        "image_processor",
        os.path.join(os.path.dirname(__file__), '../../services/image-agent/image_processor.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.process_diagnostic_image

process_diagnostic_image = get_image_processor()

class ImageUploadRequest(BaseModel):
    """Request schema for image upload"""
    patient_id: str
    patient_name: str
    age: str
    gender: str
    study_date: str
    image_type: str  # xray, mri, ct
    image_path: str  # Path to uploaded image

class ImageAnalysisResponse(BaseModel):
    """Response schema for image analysis"""
    status: str
    session_id: str
    patient_id: str
    message: str

# Step 1: Image Upload and Analysis
config = {
    "type": "api",
    "name": "ImageAnalysisAPI",
    "description": "Upload and analyze diagnostic images",
    "flows": ["medical-report"],
    "method": "POST",
    "path": "/medical/analyze-image",
    "bodySchema": ImageUploadRequest.model_json_schema(),
    "responseSchema": {
        200: ImageAnalysisResponse.model_json_schema(),
    },
    "emits": ["image-analyzed"],
}

async def handler(req, context):
    """
    Handle image upload and trigger analysis
    """
    body = req.get("body", {})
    context.logger.info("Medical Workflow - Image Analysis Started", {"patient_id": body.get("patient_id")})
    
    try:
        # Extract request data
        patient_id = body.get("patient_id")
        patient_name = body.get("patient_name")
        age = body.get("age")
        gender = body.get("gender")
        study_date = body.get("study_date")
        image_type = body.get("image_type", "xray")
        image_path = body.get("image_path")
        
        # Process image
        metadata = {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "age": age,
            "gender": gender,
            "study_date": study_date
        }
        
        analysis_result = process_diagnostic_image(image_path, image_type, metadata)
        
        # Generate session ID
        session_id = f"SESSION-{patient_id}-{study_date}"
        
        # Store analysis result in state
        await context.state.set(
            f"imaging_result_{session_id}",
            analysis_result
        )
        
        # Store patient info
        await context.state.set(
            f"patient_info_{session_id}",
            {
                "patient_id": patient_id,
                "patient_name": patient_name,
                "age": age,
                "gender": gender,
                "study_date": study_date
            }
        )
        
        # Emit event for next step
        await context.emit({
            "topic": "image-analyzed",
            "data": {
                "session_id": session_id,
                "patient_id": patient_id,
                "status": analysis_result.get("status"),
                "observations_count": len(analysis_result.get("observations", []))
            }
        })
        
        context.logger.info("Image Analysis Completed", {
            "session_id": session_id,
            "status": analysis_result.get("status")
        })
        
        return {
            "status": 200,
            "body": {
                "status": "success",
                "session_id": session_id,
                "patient_id": patient_id,
                "message": "Image analysis completed successfully"
            }
        }
        
    except Exception as e:
        context.logger.error("Image Analysis Failed", {"error": str(e)})
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": str(e)
            }
        }

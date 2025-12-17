"""
Laboratory Results Analysis Step
Handles lab data input and analysis
"""

from pydantic import BaseModel
from typing import Dict, Any
import sys
import os
import importlib.util

# Import lab analyzer dynamically
def get_lab_analyzer():
    spec = importlib.util.spec_from_file_location(
        "lab_analyzer",
        os.path.join(os.path.dirname(__file__), '../../services/lab-agent/lab_analyzer.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.analyze_lab_results

analyze_lab_results = get_lab_analyzer()

class LabResultsRequest(BaseModel):
    """Request schema for lab results"""
    session_id: str
    lab_data: Dict[str, float]  # test_name: value pairs

class LabAnalysisResponse(BaseModel):
    """Response schema for lab analysis"""
    status: str
    session_id: str
    message: str
    abnormal_count: int
    critical_count: int

# Step 2: Lab Results Analysis
config = {
    "type": "api",
    "name": "LabAnalysisAPI",
    "description": "Analyze laboratory results",
    "flows": ["medical-report"],
    "method": "POST",
    "path": "/medical/analyze-labs",
    "bodySchema": LabResultsRequest.model_json_schema(),
    "responseSchema": {
        200: LabAnalysisResponse.model_json_schema(),
    },
    "emits": ["labs-analyzed"],
}

async def handler(req, context):
    """
    Handle lab results analysis
    """
    body = req.get("body", {})
    session_id = body.get("session_id")
    
    context.logger.info("Medical Workflow - Lab Analysis Started", {"session_id": session_id})
    
    try:
        lab_data = body.get("lab_data", {})
        
        # Analyze lab results
        analysis_result = analyze_lab_results(lab_data)
        
        # Store lab result in state
        await context.state.set(
            "medical_reports",
            f"lab_result_{session_id}",
            analysis_result
        )
        
        # Emit event
        await context.emit({
            "topic": "labs-analyzed",
            "data": {
                "session_id": session_id,
                "status": analysis_result.get("status"),
                "abnormal_count": analysis_result.get("summary", {}).get("abnormal_count", 0),
                "critical_count": analysis_result.get("summary", {}).get("critical_count", 0)
            }
        })
        
        context.logger.info("Lab Analysis Completed", {
            "session_id": session_id,
            "abnormal_count": analysis_result.get("summary", {}).get("abnormal_count", 0)
        })
        
        return {
            "status": 200,
            "body": {
                "status": "success",
                "session_id": session_id,
                "message": "Lab analysis completed successfully",
                "abnormal_count": analysis_result.get("summary", {}).get("abnormal_count", 0),
                "critical_count": analysis_result.get("summary", {}).get("critical_count", 0)
            }
        }
        
    except Exception as e:
        context.logger.error("Lab Analysis Failed", {"error": str(e)})
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": str(e)
            }
        }

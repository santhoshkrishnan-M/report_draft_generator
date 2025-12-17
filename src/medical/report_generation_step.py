"""
Report Generation Step
Generates draft medical report from imaging and lab results
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os
import importlib.util

# Import report generator dynamically
def get_report_generator():
    spec = importlib.util.spec_from_file_location(
        "report_generator",
        os.path.join(os.path.dirname(__file__), '../../services/report-agent/report_generator.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_medical_report

generate_medical_report = get_report_generator()

class ReportGenerationRequest(BaseModel):
    """Request schema for report generation"""
    session_id: str

class ReportGenerationResponse(BaseModel):
    """Response schema for report generation"""
    status: str
    session_id: str
    report_id: str
    message: str
    requires_approval: bool

# Step 3: Generate Draft Report
config = {
    "type": "api",
    "name": "GenerateReportAPI",
    "description": "Generate draft medical report",
    "flows": ["medical-report"],
    "method": "POST",
    "path": "/medical/generate-report",
    "bodySchema": ReportGenerationRequest.model_json_schema(),
    "responseSchema": {
        200: ReportGenerationResponse.model_json_schema(),
    },
    "emits": ["report-generated"],
}

async def handler(req, context):
    """
    Generate complete medical report from all data
    """
    body = req.get("body", {})
    session_id = body.get("session_id")
    
    context.logger.info("Medical Workflow - Report Generation Started", {"session_id": session_id})
    
    try:
        # Retrieve stored data from state
        patient_info = await context.state.get("medical_reports", f"patient_info_{session_id}")
        imaging_result = await context.state.get("medical_reports", f"imaging_result_{session_id}")
        lab_result = await context.state.get("medical_reports", f"lab_result_{session_id}")
        
        if not patient_info:
            raise ValueError("Patient information not found. Please complete image analysis first.")
        
        # Generate report
        report = generate_medical_report(
            patient_data=patient_info,
            imaging_data=imaging_result,
            lab_data=lab_result
        )
        
        # Store draft report in state
        await context.state.set(
            "medical_reports",
            f"draft_report_{session_id}",
            report
        )
        
        report_id = report.get("report_id")
        
        # Emit event for human review
        await context.emit({
            "topic": "report-generated",
            "data": {
                "session_id": session_id,
                "report_id": report_id,
                "requires_approval": True,
                "requires_urgent_review": report.get("metadata", {}).get("requires_urgent_review", False)
            }
        })
        
        context.logger.info("Report Generated - Awaiting Approval", {
            "session_id": session_id,
            "report_id": report_id
        })
        
        return {
            "status": 200,
            "body": {
                "status": "success",
                "session_id": session_id,
                "report_id": report_id,
                "message": "Draft report generated. Awaiting radiologist review.",
                "requires_approval": True
            }
        }
        
    except Exception as e:
        context.logger.error("Report Generation Failed", {"error": str(e)})
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": str(e)
            }
        }

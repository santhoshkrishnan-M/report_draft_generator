"""
Get Report Step
Retrieve generated reports and PDF
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class GetReportRequest(BaseModel):
    """Request schema for retrieving report"""
    session_id: str

class GetReportResponse(BaseModel):
    """Response schema for report retrieval"""
    status: str
    session_id: str
    report: Optional[Dict[str, Any]] = None
    pdf_path: Optional[str] = None

# Step 5: Get Report (for UI display)
config = {
    "type": "api",
    "name": "GetReportAPI",
    "description": "Retrieve generated medical report",
    "flows": ["medical-report"],
    "method": "GET",
    "path": "/medical/report/{session_id}",
    "responseSchema": {
        200: GetReportResponse.model_json_schema(),
    },
    "emits": [],
}

async def handler(req, context):
    """
    Retrieve report for display in UI
    """
    params = req.get("params", {})
    session_id = params.get("session_id")
    
    context.logger.info("Retrieving Report", {"session_id": session_id})
    
    try:
        # Try to get final report first
        final_report = await context.state.get(f"final_report_{session_id}")
        pdf_path = await context.state.get(f"pdf_path_{session_id}")
        
        if final_report:
            return {
                "status": 200,
                "body": {
                    "status": "approved",
                    "session_id": session_id,
                    "report": final_report,
                    "pdf_path": pdf_path
                }
            }
        
        # If no final report, get draft
        draft_report = await context.state.get(f"draft_report_{session_id}")
        
        if draft_report:
            return {
                "status": 200,
                "body": {
                    "status": "draft",
                    "session_id": session_id,
                    "report": draft_report,
                    "pdf_path": None
                }
            }
        
        # No report found
        return {
            "status": 404,
            "body": {
                "status": "not_found",
                "session_id": session_id,
                "report": None,
                "pdf_path": None
            }
        }
        
    except Exception as e:
        context.logger.error("Report Retrieval Failed", {"error": str(e)})
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": str(e)
            }
        }

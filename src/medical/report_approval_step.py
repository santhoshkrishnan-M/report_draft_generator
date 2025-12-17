"""
Report Approval and Finalization Step
Human-in-the-loop review and approval
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os
import importlib.util

# Import PDF generator dynamically
def get_pdf_generator():
    spec = importlib.util.spec_from_file_location(
        "pdf_generator",
        os.path.join(os.path.dirname(__file__), '../../services/pdf-service/pdf_generator.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.export_report_to_pdf

export_report_to_pdf = get_pdf_generator()

class ReportApprovalRequest(BaseModel):
    """Request schema for report approval"""
    session_id: str
    report_id: str
    approved: bool
    reviewer_name: str
    reviewer_comments: Optional[str] = None
    edited_report: Optional[Dict[str, Any]] = None  # If user edited the report

class ReportApprovalResponse(BaseModel):
    """Response schema for report approval"""
    status: str
    session_id: str
    report_id: str
    pdf_path: Optional[str] = None
    message: str

# Step 4: Report Approval and PDF Generation
config = {
    "type": "api",
    "name": "ApproveReportAPI",
    "description": "Human review and approval of medical report",
    "flows": ["medical-report"],
    "method": "POST",
    "path": "/medical/approve-report",
    "bodySchema": ReportApprovalRequest.model_json_schema(),
    "responseSchema": {
        200: ReportApprovalResponse.model_json_schema(),
    },
    "emits": ["report-approved", "report-rejected"],
}

async def handler(req, context):
    """
    Handle human review and approval
    Generate final PDF if approved
    """
    body = req.get("body", {})
    session_id = body.get("session_id")
    report_id = body.get("report_id")
    approved = body.get("approved", False)
    reviewer_name = body.get("reviewer_name")
    reviewer_comments = body.get("reviewer_comments")
    edited_report = body.get("edited_report")
    
    context.logger.info("Medical Workflow - Report Review", {
        "session_id": session_id,
        "approved": approved,
        "reviewer": reviewer_name
    })
    
    try:
        # Get draft report from state
        draft_report = await context.state.get(f"draft_report_{session_id}")
        
        if not draft_report:
            raise ValueError("Draft report not found")
        
        if not approved:
            # Report rejected - store rejection info
            rejection_info = {
                "reviewer_name": reviewer_name,
                "comments": reviewer_comments,
                "rejected_at": context.trace_id
            }
            
            await context.state.set(f"rejection_{session_id}", rejection_info)
            
            await context.emit({
                "topic": "report-rejected",
                "data": {
                    "session_id": session_id,
                    "report_id": report_id,
                    "reviewer": reviewer_name
                }
            })
            
            context.logger.info("Report Rejected", {"session_id": session_id})
            
            return {
                "status": 200,
                "body": {
                    "status": "rejected",
                    "session_id": session_id,
                    "report_id": report_id,
                    "message": "Report rejected and returned for revision"
                }
            }
        
        # Report approved
        final_report = edited_report if edited_report else draft_report
        
        # Update report status
        final_report["status"] = "approved"
        final_report["reviewer_name"] = reviewer_name
        final_report["reviewer_comments"] = reviewer_comments
        final_report["requires_approval"] = False
        
        # Ensure PDF output directory exists
        pdf_output_dir = os.path.join(os.path.dirname(__file__), '../../outputs/pdfs')
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # Generate PDF
        pdf_path = export_report_to_pdf(final_report, pdf_output_dir)
        
        # Store final report
        await context.state.set(f"final_report_{session_id}", final_report)
        await context.state.set(f"pdf_path_{session_id}", pdf_path)
        
        # Emit approval event
        await context.emit({
            "topic": "report-approved",
            "data": {
                "session_id": session_id,
                "report_id": report_id,
                "pdf_path": pdf_path,
                "reviewer": reviewer_name
            }
        })
        
        context.logger.info("Report Approved and Finalized", {
            "session_id": session_id,
            "pdf_path": pdf_path
        })
        
        return {
            "status": 200,
            "body": {
                "status": "approved",
                "session_id": session_id,
                "report_id": report_id,
                "pdf_path": pdf_path,
                "message": "Report approved and PDF generated successfully"
            }
        }
        
    except Exception as e:
        context.logger.error("Report Approval Failed", {"error": str(e)})
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": str(e)
            }
        }

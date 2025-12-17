"""
PDF Download Endpoint
Serves the final approved PDF report for download
"""

from pydantic import BaseModel
from typing import Optional
import os

class PDFDownloadResponse(BaseModel):
    """Response schema for PDF download"""
    status: str
    message: str
    report_id: Optional[str] = None
    file_available: bool = False

# Step: Download PDF Report
config = {
    "type": "api",
    "name": "DownloadPDFAPI",
    "description": "Download final approved medical report as PDF",
    "flows": ["medical-report"],
    "method": "GET",
    "path": "/medical/report/:sessionId/download",
    "responseSchema": {
        200: {
            "content": {
                "application/pdf": {}
            }
        },
        404: PDFDownloadResponse.model_json_schema(),
    },
    "emits": [],
}

async def handler(req, context):
    """
    Serve PDF file for download
    """
    params = req.get("params", {})
    session_id = params.get("sessionId")
    
    context.logger.info("PDF Download Request", {"session_id": session_id})
    
    try:
        # Get PDF path from state
        pdf_path = await context.state.get(f"pdf_path_{session_id}")
        
        if not pdf_path:
            context.logger.warn("PDF not found", {"session_id": session_id})
            return {
                "status": 404,
                "body": {
                    "status": "not_found",
                    "message": "PDF report not found. Ensure the report has been approved.",
                    "file_available": False
                }
            }
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            context.logger.error("PDF file missing", {"path": pdf_path})
            return {
                "status": 404,
                "body": {
                    "status": "error",
                    "message": "PDF file not found on server",
                    "file_available": False
                }
            }
        
        # Get final report for metadata
        final_report = await context.state.get(f"final_report_{session_id}")
        report_id = final_report.get('report_id', 'report') if final_report else 'report'
        
        # Read PDF file
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        context.logger.info("PDF Download Successful", {
            "session_id": session_id,
            "file_size": len(pdf_content)
        })
        
        # Return PDF with proper headers
        return {
            "status": 200,
            "headers": {
                "Content-Type": "application/pdf",
                "Content-Disposition": f'attachment; filename="{report_id}.pdf"',
                "Content-Length": str(len(pdf_content)),
                "Cache-Control": "no-cache"
            },
            "body": pdf_content
        }
        
    except Exception as e:
        context.logger.error("PDF Download Failed", {"error": str(e)})
        return {
            "status": 500,
            "body": {
                "status": "error",
                "message": f"Failed to download PDF: {str(e)}",
                "file_available": False
            }
        }

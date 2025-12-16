"""
PDF Export Service for Medical Reports
Generates professional medical-grade PDF reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Frame, PageTemplate
from reportlab.lib.colors import HexColor
from datetime import datetime
from typing import Dict, Any, List
import os

class MedicalReportPDFGenerator:
    """Generate professional PDF medical reports"""
    
    def __init__(self):
        self.page_width, self.page_height = letter
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for medical reports"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=HexColor('#2c5aa0'),
            borderPadding=5,
            backColor=HexColor('#f0f4f8')
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Disclaimer style
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.red,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Critical finding
        self.styles.add(ParagraphStyle(
            name='Critical',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.red,
            fontName='Helvetica-Bold'
        ))
    
    def _create_header(self, canvas, doc):
        """Create page header"""
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(HexColor('#1a5490'))
        canvas.drawString(inch, self.page_height - 0.5*inch, "AI-ASSISTED MEDICAL DIAGNOSTIC REPORT")
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(inch, self.page_height - 0.65*inch, "DRAFT - FOR REVIEW ONLY")
        canvas.line(inch, self.page_height - 0.75*inch, 
                   self.page_width - inch, self.page_height - 0.75*inch)
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        """Create page footer"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page_num = canvas.getPageNumber()
        text = f"Page {page_num} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        canvas.drawString(inch, 0.5*inch, text)
        canvas.drawRightString(self.page_width - inch, 0.5*inch, 
                              "Confidential Medical Document")
        canvas.restoreState()
    
    def _create_patient_info_table(self, patient_info: Dict[str, str]) -> Table:
        """Create patient information table"""
        data = [
            ['Patient ID:', patient_info.get('patient_id', 'N/A'),
             'Study Date:', patient_info.get('study_date', 'N/A')],
            ['Patient Name:', patient_info.get('patient_name', 'N/A'),
             'Age/Gender:', f"{patient_info.get('age', 'N/A')} / {patient_info.get('gender', 'N/A')}"]
        ]
        
        table = Table(data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f0f8')),
            ('BACKGROUND', (2, 0), (2, -1), HexColor('#e8f0f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _format_findings_list(self, findings: List[str]) -> List[Paragraph]:
        """Format findings as paragraphs"""
        paragraphs = []
        
        for finding in findings:
            # Check for critical markers
            if '⚠️ CRITICAL' in finding or 'CRITICAL VALUES:' in finding:
                para = Paragraph(finding, self.styles['Critical'])
            else:
                para = Paragraph(finding, self.styles['ReportBody'])
            paragraphs.append(para)
        
        return paragraphs
    
    def generate_pdf(self, report_data: Dict[str, Any], output_path: str) -> str:
        """
        Generate PDF from report data
        Returns path to generated PDF
        """
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Container for PDF elements
        story = []
        
        # Title
        title = Paragraph("MEDICAL DIAGNOSTIC REPORT", self.styles['ReportTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Report ID and status
        report_info = f"<b>Report ID:</b> {report_data.get('report_id', 'N/A')} | " \
                     f"<b>Status:</b> {report_data.get('status', 'DRAFT').upper()}"
        story.append(Paragraph(report_info, self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Patient Information
        story.append(Paragraph("PATIENT INFORMATION", self.styles['SectionHeading']))
        patient_table = self._create_patient_info_table(
            report_data.get('patient_information', {})
        )
        story.append(patient_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Examination Summary
        story.append(Paragraph("EXAMINATION SUMMARY", self.styles['SectionHeading']))
        exam_summary = report_data.get('examination_summary', 'N/A')
        story.append(Paragraph(exam_summary, self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Imaging Findings
        imaging = report_data.get('imaging_findings', {})
        if imaging.get('status') == 'completed':
            story.append(Paragraph("IMAGING FINDINGS", self.styles['SectionHeading']))
            imaging_paras = self._format_findings_list(imaging.get('findings', []))
            for para in imaging_paras:
                story.append(para)
            story.append(Spacer(1, 0.2*inch))
        
        # Laboratory Findings
        lab = report_data.get('laboratory_findings', {})
        if lab.get('status') == 'completed':
            story.append(Paragraph("LABORATORY FINDINGS", self.styles['SectionHeading']))
            lab_paras = self._format_findings_list(lab.get('findings', []))
            for para in lab_paras:
                story.append(para)
            story.append(Spacer(1, 0.2*inch))
        
        # Interpretive Notes
        story.append(Paragraph("INTERPRETIVE NOTES", self.styles['SectionHeading']))
        notes = report_data.get('interpretive_notes', [])
        for note in notes:
            story.append(Paragraph(note, self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("RECOMMENDATIONS", self.styles['SectionHeading']))
        recommendations = report_data.get('recommendations', [])
        for rec in recommendations:
            story.append(Paragraph(rec, self.styles['ReportBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        disclaimer_lines = report_data.get('disclaimer', [])
        for line in disclaimer_lines:
            if line.strip() and '═' not in line:
                story.append(Paragraph(line, self.styles['Disclaimer']))
        
        # Build PDF with header and footer
        doc.build(story, 
                 onFirstPage=self._create_header,
                 onLaterPages=self._create_header)
        
        return output_path


def export_report_to_pdf(report_data: Dict[str, Any], output_dir: str = "/tmp") -> str:
    """
    Main entry point for PDF export
    Returns path to generated PDF file
    """
    generator = MedicalReportPDFGenerator()
    
    # Generate filename
    report_id = report_data.get('report_id', 'report')
    filename = f"{report_id}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Generate PDF
    pdf_path = generator.generate_pdf(report_data, output_path)
    
    return pdf_path


if __name__ == "__main__":
    # Test PDF generation
    test_report = {
        'report_id': 'RPT-TEST-001',
        'status': 'draft',
        'patient_information': {
            'patient_id': 'P12345',
            'patient_name': 'Test Patient',
            'age': '45',
            'gender': 'M',
            'study_date': '2025-12-16'
        },
        'examination_summary': 'Test examination summary.',
        'imaging_findings': {
            'status': 'completed',
            'findings': ['Test finding 1', 'Test finding 2']
        },
        'laboratory_findings': {
            'status': 'completed',
            'findings': ['Test lab result 1']
        },
        'interpretive_notes': ['Test note'],
        'recommendations': ['Test recommendation'],
        'disclaimer': ['This is a test disclaimer']
    }
    
    pdf_path = export_report_to_pdf(test_report)
    print(f"PDF generated: {pdf_path}")

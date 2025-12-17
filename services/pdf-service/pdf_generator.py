"""
PDF Export Service for Medical Reports
Generates professional medical-grade PDF reports with comprehensive details
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.platypus import Frame, PageTemplate, Image as RLImage
from reportlab.lib.colors import HexColor
from datetime import datetime
from typing import Dict, Any, List, Optional
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
        """Create professional page header with hospital branding"""
        canvas.saveState()
        
        # Header background
        canvas.setFillColor(HexColor('#1a5490'))
        canvas.rect(0.5*inch, self.page_height - 0.9*inch, self.page_width - inch, 0.4*inch, fill=1, stroke=0)
        
        # Title
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.white)
        canvas.drawString(0.7*inch, self.page_height - 0.75*inch, "MEDICAL DIAGNOSTIC REPORT")
        
        # Document status on right
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(self.page_width - 0.7*inch, self.page_height - 0.75*inch, 
                              f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        """Create professional page footer"""
        canvas.saveState()
        
        # Footer line
        canvas.setStrokeColor(HexColor('#cccccc'))
        canvas.setLineWidth(0.5)
        canvas.line(0.5*inch, 0.7*inch, self.page_width - 0.5*inch, 0.7*inch)
        
        # Page number and confidentiality notice
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page_num = canvas.getPageNumber()
        canvas.drawString(0.5*inch, 0.5*inch, f"Page {page_num}")
        canvas.drawCentredString(self.page_width / 2, 0.5*inch, 
                                "CONFIDENTIAL MEDICAL DOCUMENT")
        canvas.drawRightString(self.page_width - 0.5*inch, 0.5*inch, 
                              "AI-Assisted Report")
        
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
        Generate comprehensive, detailed PDF from report data
        Returns path to generated PDF
        """
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1.2*inch,
            bottomMargin=inch
        )
        
        # Container for PDF elements
        story = []
        
        # Document Header Section
        header_data = [
            [Paragraph("<b><font size=18 color='#1a5490'>MEDICAL DIAGNOSTIC REPORT</font></b>", 
                      self.styles['Normal'])]
        ]
        header_table = Table(header_data, colWidths=[7*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.extend([header_table, Spacer(1, 0.15*inch)])
        
        # Report Metadata
        report_id = report_data.get('report_id', 'N/A')
        status = report_data.get('status', 'DRAFT').upper()
        status_color = '#22c55e' if status == 'APPROVED' else '#f59e0b'
        
        meta_text = f"<b>Report ID:</b> {report_id} | <b><font color='{status_color}'>Status: {status}</font></b>"
        if report_data.get('reviewer_name'):
            meta_text += f" | <b>Reviewed by:</b> {report_data.get('reviewer_name')}"
        
        story.extend([Paragraph(meta_text, self.styles['ReportBody']), Spacer(1, 0.25*inch)])
        
        # Patient Information Section
        story.append(Paragraph("PATIENT INFORMATION", self.styles['SectionHeading']))
        patient_info = report_data.get('patient_information', {})
        
        patient_data = [
            ['<b>Patient ID:</b>', patient_info.get('patient_id', 'N/A'),
             '<b>Study Date:</b>', patient_info.get('study_date', 'N/A')],
            ['<b>Patient Name:</b>', patient_info.get('patient_name', 'N/A'),
             '<b>Age:</b>', str(patient_info.get('age', 'N/A'))],
            ['<b>Gender:</b>', patient_info.get('gender', 'N/A'),
             '<b>Image Type:</b>', patient_info.get('image_type', 'N/A')]
        ]
        
        patient_table = Table(patient_data, colWidths=[1.4*inch, 2.1*inch, 1.4*inch, 2.1*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f4f8')),
            ('BACKGROUND', (2, 0), (2, -1), HexColor('#f0f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.extend([patient_table, Spacer(1, 0.3*inch)])
        
        # Examination Summary
        exam_summary = report_data.get('examination_summary', 'No examination summary provided.')
        story.extend([
            Paragraph("EXAMINATION SUMMARY", self.styles['SectionHeading']),
            Paragraph(exam_summary, self.styles['ReportBody']),
            Spacer(1, 0.25*inch)
        ])
        
        # Imaging Findings Section
        imaging = report_data.get('imaging_findings', {})
        if imaging and imaging.get('status') == 'completed':
            story.append(Paragraph("IMAGING FINDINGS", self.styles['SectionHeading']))
            
            findings_list = imaging.get('findings', [])
            if findings_list:
                finding_elements = []
                for i, finding in enumerate(findings_list, 1):
                    # Check for critical findings
                    is_critical = any(marker in finding.upper() for marker in ['CRITICAL', 'URGENT', 'IMMEDIATE', '⚠️'])
                    
                    finding_text = (f"<b><font color='red'>{i}. {finding}</font></b>" if is_critical 
                                  else f"{i}. {finding}")
                    
                    finding_elements.extend([Paragraph(finding_text, self.styles['ReportBody']), Spacer(1, 0.08*inch)])
                story.extend(finding_elements)
            else:
                story.append(Paragraph("No significant imaging findings reported.", self.styles['ReportBody']))
            
            # Image metadata if available
            if imaging.get('metadata'):
                metadata = imaging.get('metadata', {})
                meta_lines = []
                if metadata.get('mean_intensity'):
                    meta_lines.append(f"Mean Intensity: {metadata.get('mean_intensity'):.2f}")
                if metadata.get('edge_density'):
                    meta_lines.append(f"Edge Density: {metadata.get('edge_density'):.4f}")
                
                if meta_lines:
                    story.append(Spacer(1, 0.1*inch))
                    meta_text = " | ".join(meta_lines)
                    story.append(Paragraph(f"<i><font size=9 color='gray'>{meta_text}</font></i>", 
                                         self.styles['Normal']))
            
            story.append(Spacer(1, 0.25*inch))
        
        # Laboratory Findings Section
        lab = report_data.get('laboratory_findings', {})
        if lab and lab.get('status') == 'completed':
            story.append(Paragraph("LABORATORY FINDINGS", self.styles['SectionHeading']))
            
            findings_list = lab.get('findings', [])
            if findings_list:
                lab_elements = []
                # Create detailed lab table if we have structured data
                if lab.get('abnormal_findings') or lab.get('critical_findings'):
                    lab_elements.extend([Paragraph("Abnormal Results:", self.styles['ReportBody']), Spacer(1, 0.1*inch)])
                
                for i, finding in enumerate(findings_list, 1):
                    is_critical = 'CRITICAL' in finding.upper() or '⚠️' in finding
                    
                    finding_text = (f"<b><font color='red'>{i}. {finding}</font></b>" if is_critical
                                  else f"{i}. {finding}")
                    
                    lab_elements.extend([Paragraph(finding_text, self.styles['ReportBody']), Spacer(1, 0.08*inch)])
                story.extend(lab_elements)
            else:
                story.append(Paragraph("All laboratory values within normal limits.", self.styles['ReportBody']))
            
            story.append(Spacer(1, 0.25*inch))
        
        # Interpretive Notes
        story.append(Paragraph("INTERPRETIVE NOTES", self.styles['SectionHeading']))
        notes = report_data.get('interpretive_notes', [])
        if notes:
            note_elements = []
            for note in notes:
                if note and note.strip():
                    note_elements.extend([Paragraph(f"• {note}", self.styles['ReportBody']), Spacer(1, 0.08*inch)])
            story.extend(note_elements)
        else:
            story.append(Paragraph("No additional interpretive notes.", self.styles['ReportBody']))
        story.append(Spacer(1, 0.25*inch))
        
        # Recommendations
        story.append(Paragraph("RECOMMENDATIONS", self.styles['SectionHeading']))
        recommendations = report_data.get('recommendations', [])
        if recommendations:
            rec_elements = []
            for rec in recommendations:
                if rec and rec.strip():
                    rec_elements.extend([Paragraph(f"• {rec}", self.styles['ReportBody']), Spacer(1, 0.08*inch)])
            story.extend(rec_elements)
        else:
            story.append(Paragraph("No specific recommendations at this time. Follow up as clinically indicated.", 
                                 self.styles['ReportBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # Reviewer Comments (if approved)
        if report_data.get('reviewer_comments'):
            story.append(Paragraph("REVIEWER NOTES", self.styles['SectionHeading']))
            story.append(Paragraph(report_data.get('reviewer_comments'), self.styles['ReportBody']))
            story.append(Spacer(1, 0.3*inch))
        
        # Signature Section (if approved)
        if status == 'APPROVED' and report_data.get('reviewer_name'):
            story.append(Spacer(1, 0.2*inch))
            sig_data = [
                ['', ''],
                ['_________________________________', '_________________________________'],
                [f"<b>{report_data.get('reviewer_name')}</b>", 
                 f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
                ['Reviewing Radiologist/Physician', '']
            ]
            sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
            sig_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
            ]))
            story.append(sig_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer Box
        story.append(Spacer(1, 0.2*inch))
        disclaimer_lines = report_data.get('disclaimer', [
            '⚠️ IMPORTANT DISCLAIMER',
            'This report has been generated with AI assistance and reviewed by a licensed medical professional.',
            'The findings and recommendations are based on available data and should be correlated with clinical context.',
            'This document is for medical professional use only and should not be used for self-diagnosis.',
            'All medical decisions should be made in consultation with qualified healthcare providers.'
        ])
        
        disclaimer_text = "<br/>".join([line for line in disclaimer_lines if line.strip() and '═' not in line])
        disclaimer_para = Paragraph(f"<font size=9>{disclaimer_text}</font>", self.styles['Disclaimer'])
        
        disclaimer_table = Table([[disclaimer_para]], colWidths=[7*inch])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#fff3cd')),
            ('BORDER', (0, 0), (-1, -1), 1, HexColor('#ff9800')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(disclaimer_table)
        
        # Build PDF with header and footer
        doc.build(story, 
                 onFirstPage=self._create_footer,
                 onLaterPages=self._create_footer)
        
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

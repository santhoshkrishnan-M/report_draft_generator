#!/usr/bin/env python3
"""
Test PDF Generation with Comprehensive Medical Report Data
"""

import sys
import os
import importlib.util

# Load PDF generator dynamically
def load_pdf_generator():
    pdf_gen_path = os.path.join(
        os.path.dirname(__file__), 
        'services/pdf-service/pdf_generator.py'
    )
    spec = importlib.util.spec_from_file_location("pdf_generator", pdf_gen_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.export_report_to_pdf

export_report_to_pdf = load_pdf_generator()

def create_comprehensive_test_report():
    """Create a detailed test report with all sections"""
    return {
        'report_id': 'RPT-20251217-TEST-001',
        'status': 'approved',
        'reviewer_name': 'Dr. Sarah Johnson, MD',
        'reviewer_comments': 'Report reviewed and approved. Clinical correlation recommended for elevated glucose levels. Patient should be monitored for diabetic complications.',
        
        'patient_information': {
            'patient_id': 'P-2025-12345',
            'patient_name': 'John Michael Doe',
            'age': '45',
            'gender': 'Male',
            'study_date': '2025-12-17',
            'image_type': 'Chest X-Ray (PA & Lateral)'
        },
        
        'examination_summary': (
            'Comprehensive diagnostic evaluation including chest radiography and complete '
            'laboratory panel. Patient presented with complaints of shortness of breath and '
            'fatigue over the past 3 weeks. This AI-assisted report integrates imaging findings '
            'with laboratory results to provide a holistic clinical picture. All findings have '
            'been reviewed and validated by a board-certified radiologist.'
        ),
        
        'imaging_findings': {
            'status': 'completed',
            'findings': [
                'Lung fields are clear bilaterally with no evidence of consolidation, infiltrate, or mass lesion.',
                'Cardiac silhouette appears normal in size and contour. Cardiothoracic ratio within normal limits.',
                'No pleural effusion or pneumothorax detected on either side.',
                'Bony thorax demonstrates normal alignment with no acute fractures identified.',
                'Mediastinal contours are within normal limits. No hilar lymphadenopathy.',
                'The diaphragm is clearly outlined and demonstrates normal dome shape bilaterally.',
                'Soft tissues and chest wall appear unremarkable.',
                'No significant interval changes compared to prior study from 2024-11-15, if available.'
            ],
            'metadata': {
                'mean_intensity': 142.56,
                'edge_density': 0.2341,
                'texture_variance': 1856.23,
                'processing_time': '2.4 seconds'
            }
        },
        
        'laboratory_findings': {
            'status': 'completed',
            'findings': [
                'Hemoglobin: 11.2 g/dL (LOW - Reference: 13.0-17.0 g/dL) - Mild anemia detected',
                'White Blood Cell Count: 7,800/µL (NORMAL - Reference: 4,000-11,000/µL)',
                '⚠️ CRITICAL: Glucose (Fasting): 245 mg/dL (HIGH - Reference: 70-100 mg/dL) - Significantly elevated, immediate clinical attention required',
                'Creatinine: 1.1 mg/dL (NORMAL - Reference: 0.7-1.3 mg/dL) - Renal function within normal limits',
                'Sodium: 138 mEq/L (NORMAL - Reference: 136-145 mEq/L)',
                'Potassium: 4.2 mEq/L (NORMAL - Reference: 3.5-5.0 mEq/L)',
                'Total Cholesterol: 245 mg/dL (BORDERLINE HIGH - Reference: <200 mg/dL)',
                'LDL Cholesterol: 165 mg/dL (HIGH - Reference: <100 mg/dL) - Cardiovascular risk factor',
                'HDL Cholesterol: 38 mg/dL (LOW - Reference: >40 mg/dL for men) - Protective cholesterol below optimal',
                'Triglycerides: 210 mg/dL (HIGH - Reference: <150 mg/dL)',
                'HbA1c: 8.2% (HIGH - Reference: <5.7% normal, 5.7-6.4% prediabetes, ≥6.5% diabetes) - Indicates poor glycemic control',
                'Thyroid Stimulating Hormone (TSH): 2.4 mIU/L (NORMAL - Reference: 0.4-4.0 mIU/L)'
            ],
            'abnormal_findings': [
                'Hemoglobin LOW',
                'Glucose CRITICALLY HIGH',
                'Total Cholesterol BORDERLINE HIGH',
                'LDL Cholesterol HIGH',
                'HDL Cholesterol LOW',
                'Triglycerides HIGH',
                'HbA1c ELEVATED'
            ],
            'critical_findings': [
                'Glucose 245 mg/dL - Immediate attention required'
            ]
        },
        
        'interpretive_notes': [
            'The imaging findings demonstrate clear lung fields with no acute cardiopulmonary abnormality. The absence of infiltrates or consolidation effectively rules out acute infectious or inflammatory processes.',
            
            'Laboratory results reveal several significant metabolic abnormalities that require clinical attention. The critically elevated fasting glucose (245 mg/dL) combined with HbA1c of 8.2% is diagnostic of poorly controlled diabetes mellitus.',
            
            'The lipid panel demonstrates an atherogenic pattern with elevated LDL cholesterol (165 mg/dL), low HDL cholesterol (38 mg/dL), and elevated triglycerides (210 mg/dL). This constellation of findings significantly increases cardiovascular risk.',
            
            'Mild anemia (Hemoglobin 11.2 g/dL) is present and may contribute to the patient\'s reported fatigue. Given the context of diabetes, this should be evaluated for possible diabetic nephropathy, although the creatinine remains within normal limits.',
            
            'Thyroid function is normal, effectively ruling out hypothyroidism as a cause of fatigue symptoms.',
            
            'The combination of metabolic syndrome components (hyperglycemia, dyslipidemia) places this patient at elevated risk for cardiovascular disease and diabetic complications.'
        ],
        
        'recommendations': [
            'Immediate initiation or adjustment of diabetes management protocol. Consider referral to endocrinology for optimization of glycemic control.',
            
            'Recommend HbA1c monitoring every 3 months until target level below 7% is achieved, then quarterly thereafter.',
            
            'Lipid management: Consider statin therapy for cardiovascular risk reduction given the elevated LDL and presence of diabetes. Target LDL <70 mg/dL for high-risk patients.',
            
            'Further evaluation of anemia: Complete blood count with differential, iron studies, vitamin B12, and folate levels recommended to determine etiology.',
            
            'Comprehensive diabetic evaluation including: retinal examination, urine microalbumin, foot examination, and assessment for diabetic neuropathy.',
            
            'Lifestyle modifications counseling: Medical nutrition therapy for diabetes and dyslipidemia, regular physical activity (150 minutes/week moderate intensity), and weight management if indicated.',
            
            'Blood pressure monitoring at each visit, as diabetes patients should maintain BP <130/80 mmHg.',
            
            'Consider diabetic education program referral for improved self-management skills.',
            
            'Follow-up chest imaging only if clinically indicated based on symptom progression or new clinical findings.',
            
            'Regular follow-up recommended within 2-4 weeks for diabetes management optimization and to review anemia workup results.'
        ],
        
        'disclaimer': [
            '⚠️ IMPORTANT MEDICAL DISCLAIMER',
            '',
            'This medical diagnostic report has been generated with artificial intelligence assistance and has been thoroughly reviewed and approved by Dr. Sarah Johnson, MD, a board-certified radiologist/physician.',
            '',
            'The findings and interpretations provided in this report are based on the available diagnostic data at the time of examination. These results should be interpreted within the full clinical context of the patient\'s medical history, physical examination findings, and other relevant diagnostic information.',
            '',
            'IMPORTANT NOTES FOR HEALTHCARE PROVIDERS:',
            '• This report is intended for use by qualified healthcare professionals only',
            '• Clinical correlation is essential for appropriate patient management',
            '• Critical findings have been highlighted and require immediate clinical attention',
            '• Recommendations are general guidelines and should be adapted to individual patient circumstances',
            '• This report does not constitute a medical diagnosis or treatment plan by itself',
            '',
            'IMPORTANT NOTES FOR PATIENTS:',
            '• This document is a technical medical report and should be reviewed with your healthcare provider',
            '• Do not use this report for self-diagnosis or self-treatment',
            '• All treatment decisions should be made in consultation with your physician',
            '• If you have questions about these findings, please discuss them with your healthcare provider',
            '',
            'CONFIDENTIALITY NOTICE:',
            'This document contains confidential patient health information protected under HIPAA regulations. Unauthorized disclosure, copying, or distribution of this information is strictly prohibited and may be subject to legal penalties.',
            '',
            'For questions regarding this report or to request amendments, please contact the issuing healthcare facility.'
        ]
    }


def test_pdf_generation():
    """Test the PDF generation with comprehensive data"""
    print("=" * 70)
    print("PDF Generation Test - Comprehensive Medical Report")
    print("=" * 70)
    print()
    
    # Create test report
    print("✓ Creating comprehensive test report data...")
    report_data = create_comprehensive_test_report()
    
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), 'outputs/pdfs')
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Output directory: {output_dir}")
    
    # Generate PDF
    print("✓ Generating PDF...")
    try:
        pdf_path = export_report_to_pdf(report_data, output_dir)
        print(f"✓ PDF generated successfully!")
        print()
        print(f"📄 PDF Location: {pdf_path}")
        print(f"📊 File Size: {os.path.getsize(pdf_path):,} bytes")
        print()
        
        # Display report summary
        print("Report Summary:")
        print("-" * 70)
        print(f"Report ID: {report_data['report_id']}")
        print(f"Status: {report_data['status'].upper()}")
        print(f"Patient: {report_data['patient_information']['patient_name']}")
        print(f"Study Date: {report_data['patient_information']['study_date']}")
        print(f"Reviewer: {report_data['reviewer_name']}")
        print()
        print(f"Sections included:")
        print(f"  • Patient Information")
        print(f"  • Examination Summary")
        print(f"  • Imaging Findings ({len(report_data['imaging_findings']['findings'])} items)")
        print(f"  • Laboratory Findings ({len(report_data['laboratory_findings']['findings'])} items)")
        print(f"  • Interpretive Notes ({len(report_data['interpretive_notes'])} items)")
        print(f"  • Recommendations ({len(report_data['recommendations'])} items)")
        print(f"  • Reviewer Comments")
        print(f"  • Medical Disclaimer")
        print()
        
        print("=" * 70)
        print("✅ TEST PASSED - PDF generated successfully!")
        print("=" * 70)
        print()
        print(f"You can open the PDF with: xdg-open {pdf_path}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: PDF generation failed!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_pdf_generation()
    sys.exit(0 if success else 1)

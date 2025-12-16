"""
Medical Report Generation Service
Template-based report generation from imaging and lab results
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class MedicalReportGenerator:
    """Generate structured medical diagnostic reports"""
    
    def __init__(self):
        self.report_version = "1.0.0"
    
    def generate_patient_info_section(self, patient_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate patient information section"""
        return {
            'patient_id': patient_data.get('patient_id', 'N/A'),
            'patient_name': patient_data.get('patient_name', 'N/A'),
            'age': patient_data.get('age', 'N/A'),
            'gender': patient_data.get('gender', 'N/A'),
            'study_date': patient_data.get('study_date', datetime.now().strftime('%Y-%m-%d'))
        }
    
    def generate_examination_summary(self, imaging_data: Dict[str, Any], 
                                    lab_data: Dict[str, Any]) -> str:
        """Generate examination summary section"""
        summary_parts = []
        
        # Imaging summary
        if imaging_data and imaging_data.get('status') == 'success':
            image_type = imaging_data.get('image_type', 'diagnostic').upper()
            summary_parts.append(
                f"{image_type} imaging study completed. "
                f"Image quality assessed and processed for diagnostic review."
            )
        
        # Lab summary
        if lab_data and lab_data.get('status') == 'success':
            summary = lab_data.get('summary', {})
            total = summary.get('total_tests', 0)
            abnormal = summary.get('abnormal_count', 0)
            summary_parts.append(
                f"Laboratory panel consisting of {total} tests analyzed. "
                f"{abnormal} value(s) outside normal reference ranges."
            )
        
        return ' '.join(summary_parts) if summary_parts else 'Examination data pending.'
    
    def generate_imaging_findings(self, imaging_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate imaging findings section"""
        if not imaging_data or imaging_data.get('status') != 'success':
            return {
                'status': 'pending',
                'findings': ['Imaging analysis pending or unavailable.']
            }
        
        findings = []
        observations = imaging_data.get('observations', [])
        
        # Add header
        image_type = imaging_data.get('image_type', 'diagnostic').upper()
        findings.append(f"{image_type} EXAMINATION:")
        findings.append("")
        
        # Add observations
        for idx, obs in enumerate(observations, 1):
            findings.append(f"{idx}. {obs}")
        
        # Add technical details
        dimensions = imaging_data.get('image_dimensions', {})
        if dimensions:
            findings.append("")
            findings.append(f"Technical details: Image resolution {dimensions.get('width')}×{dimensions.get('height')} pixels.")
        
        return {
            'status': 'completed',
            'image_type': image_type,
            'findings': findings,
            'observations_count': len(observations)
        }
    
    def generate_laboratory_findings(self, lab_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate laboratory findings section"""
        if not lab_data or lab_data.get('status') != 'success':
            return {
                'status': 'pending',
                'findings': ['Laboratory analysis pending or unavailable.']
            }
        
        findings = []
        findings.append("LABORATORY RESULTS:")
        findings.append("")
        
        # Summary
        summary_text = lab_data.get('summary_text', '')
        if summary_text:
            findings.append(f"Summary: {summary_text}")
            findings.append("")
        
        # All results
        findings.append("Detailed Results:")
        results = lab_data.get('results', [])
        for result in results:
            test_name = result.get('test_name')
            value = result.get('value')
            unit = result.get('unit')
            ref_range = result.get('reference_range')
            flag = result.get('flag', '')
            
            findings.append(
                f"  {flag} {test_name}: {value} {unit} (Reference: {ref_range})"
            )
        
        # Highlight abnormal findings
        abnormal = lab_data.get('abnormal_findings', [])
        critical = lab_data.get('critical_findings', [])
        
        if critical:
            findings.append("")
            findings.append("CRITICAL VALUES:")
            for result in critical:
                findings.append(f"  • {result.get('test_name')}: {result.get('interpretation')}")
        
        if abnormal and not critical:
            findings.append("")
            findings.append("ABNORMAL VALUES:")
            for result in abnormal:
                findings.append(f"  • {result.get('test_name')}: {result.get('interpretation')}")
        
        return {
            'status': 'completed',
            'findings': findings,
            'abnormal_count': len(abnormal),
            'critical_count': len(critical)
        }
    
    def generate_interpretive_notes(self, imaging_data: Dict[str, Any], 
                                   lab_data: Dict[str, Any]) -> List[str]:
        """Generate interpretive notes (non-diagnostic)"""
        notes = []
        
        notes.append("INTERPRETIVE NOTES:")
        notes.append("")
        
        # Check for critical findings
        has_critical = False
        if lab_data and lab_data.get('critical_findings'):
            has_critical = True
            notes.append("• Critical laboratory values identified requiring immediate clinical attention.")
        
        # General interpretation guidance
        has_abnormal_imaging = (imaging_data and 
                               imaging_data.get('observations') and 
                               any('review recommended' in obs.lower() or 'correlation' in obs.lower() 
                                   for obs in imaging_data.get('observations', [])))
        
        has_abnormal_labs = (lab_data and 
                            lab_data.get('abnormal_count', 0) > 0)
        
        if has_abnormal_imaging:
            notes.append("• Imaging findings noted require radiologist review and clinical correlation.")
        
        if has_abnormal_labs:
            notes.append("• Laboratory abnormalities require clinical correlation with patient presentation.")
        
        if not has_critical and not has_abnormal_imaging and not has_abnormal_labs:
            notes.append("• Examination findings within expected parameters.")
            notes.append("• Routine clinical follow-up as appropriate.")
        else:
            notes.append("• Comprehensive clinical assessment recommended.")
        
        notes.append("• These findings are AI-generated and require expert medical review.")
        
        return notes
    
    def generate_recommendations(self, imaging_data: Dict[str, Any], 
                                lab_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations (non-prescriptive)"""
        recommendations = []
        
        recommendations.append("RECOMMENDATIONS:")
        recommendations.append("")
        
        # Check severity
        has_critical = lab_data and lab_data.get('critical_findings')
        
        if has_critical:
            recommendations.append("1. Immediate physician review recommended for critical values.")
            recommendations.append("2. Clinical correlation with patient symptoms and history.")
            recommendations.append("3. Consider repeat testing if clinically indicated.")
        else:
            recommendations.append("1. Radiologist review and interpretation required.")
            recommendations.append("2. Clinical correlation with patient presentation recommended.")
            recommendations.append("3. Follow-up imaging or laboratory studies as clinically indicated.")
        
        recommendations.append("4. All findings should be interpreted in the context of complete patient evaluation.")
        
        return recommendations
    
    def generate_disclaimer(self) -> List[str]:
        """Generate medical disclaimer"""
        return [
            "",
            "═" * 80,
            "IMPORTANT DISCLAIMER",
            "═" * 80,
            "",
            "This report is AI-GENERATED and is intended as a DRAFT for review purposes only.",
            "",
            "• NOT a medical diagnosis or treatment recommendation",
            "• NOT a substitute for professional medical judgment",
            "• MUST be reviewed and validated by a licensed radiologist/physician",
            "• AI analysis may contain errors or omissions",
            "• Clinical correlation with patient history and examination is essential",
            "",
            "This draft report requires human expert review and approval before clinical use.",
            "",
            "═" * 80
        ]
    
    def generate_complete_report(self, 
                                patient_data: Dict[str, Any],
                                imaging_data: Optional[Dict[str, Any]] = None,
                                lab_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate complete structured medical report
        """
        # Generate all sections
        patient_info = self.generate_patient_info_section(patient_data)
        examination_summary = self.generate_examination_summary(imaging_data or {}, lab_data or {})
        imaging_findings = self.generate_imaging_findings(imaging_data or {})
        lab_findings = self.generate_laboratory_findings(lab_data or {})
        interpretive_notes = self.generate_interpretive_notes(imaging_data or {}, lab_data or {})
        recommendations = self.generate_recommendations(imaging_data or {}, lab_data or {})
        disclaimer = self.generate_disclaimer()
        
        # Compile report
        report = {
            'report_id': f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_date': datetime.now().isoformat(),
            'report_version': self.report_version,
            'status': 'draft',
            'requires_approval': True,
            
            'patient_information': patient_info,
            'examination_summary': examination_summary,
            'imaging_findings': imaging_findings,
            'laboratory_findings': lab_findings,
            'interpretive_notes': interpretive_notes,
            'recommendations': recommendations,
            'disclaimer': disclaimer,
            
            'metadata': {
                'has_imaging': imaging_data is not None,
                'has_labs': lab_data is not None,
                'requires_urgent_review': (lab_data and lab_data.get('critical_findings', [])) is not None
            }
        }
        
        return report


def generate_medical_report(patient_data: Dict[str, Any],
                           imaging_data: Optional[Dict[str, Any]] = None,
                           lab_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Main entry point for report generation
    """
    generator = MedicalReportGenerator()
    return generator.generate_complete_report(patient_data, imaging_data, lab_data)


if __name__ == "__main__":
    # Test report generation
    test_patient = {
        'patient_id': 'P12345',
        'patient_name': 'Test Patient',
        'age': '45',
        'gender': 'M',
        'study_date': '2025-12-16'
    }
    
    report = generate_medical_report(test_patient)
    print(json.dumps(report, indent=2))

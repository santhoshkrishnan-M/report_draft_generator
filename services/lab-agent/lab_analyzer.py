"""
Laboratory Result Analysis Service
Rule-based analyzer for common lab tests
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

class TestStatus(Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    CRITICAL_LOW = "critical_low"
    CRITICAL_HIGH = "critical_high"

@dataclass
class ReferenceRange:
    """Reference range for a lab test"""
    name: str
    min_normal: float
    max_normal: float
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None
    unit: str = ""
    
# Standard reference ranges for common lab tests
REFERENCE_RANGES = {
    # Hematology
    'hemoglobin': ReferenceRange('Hemoglobin', 12.0, 16.0, 7.0, 20.0, 'g/dL'),
    'wbc': ReferenceRange('White Blood Cell Count', 4.0, 11.0, 2.0, 30.0, '×10³/μL'),
    'platelets': ReferenceRange('Platelet Count', 150, 400, 50, 1000, '×10³/μL'),
    'hematocrit': ReferenceRange('Hematocrit', 36, 48, 20, 60, '%'),
    'rbc': ReferenceRange('Red Blood Cell Count', 4.0, 5.5, 2.0, 7.0, '×10⁶/μL'),
    
    # Chemistry
    'glucose': ReferenceRange('Glucose', 70, 100, 40, 400, 'mg/dL'),
    'creatinine': ReferenceRange('Creatinine', 0.6, 1.2, 0.2, 10.0, 'mg/dL'),
    'bun': ReferenceRange('Blood Urea Nitrogen', 7, 20, 2, 100, 'mg/dL'),
    'sodium': ReferenceRange('Sodium', 136, 145, 120, 160, 'mEq/L'),
    'potassium': ReferenceRange('Potassium', 3.5, 5.0, 2.5, 7.0, 'mEq/L'),
    'calcium': ReferenceRange('Calcium', 8.5, 10.5, 6.0, 14.0, 'mg/dL'),
    'alt': ReferenceRange('ALT (Liver)', 7, 56, 0, 1000, 'U/L'),
    'ast': ReferenceRange('AST (Liver)', 10, 40, 0, 1000, 'U/L'),
    'bilirubin_total': ReferenceRange('Total Bilirubin', 0.1, 1.2, 0, 20, 'mg/dL'),
    
    # Lipid Panel
    'cholesterol_total': ReferenceRange('Total Cholesterol', 125, 200, 0, 500, 'mg/dL'),
    'hdl': ReferenceRange('HDL Cholesterol', 40, 60, 10, 150, 'mg/dL'),
    'ldl': ReferenceRange('LDL Cholesterol', 0, 100, 0, 300, 'mg/dL'),
    'triglycerides': ReferenceRange('Triglycerides', 0, 150, 0, 1000, 'mg/dL'),
}

class LabResultAnalyzer:
    """Analyze laboratory results against reference ranges"""
    
    def __init__(self):
        self.reference_ranges = REFERENCE_RANGES
    
    def analyze_value(self, test_name: str, value) -> Dict[str, Any]:
        """
        Analyze a single lab test value
        Returns status and interpretation
        """
        # Extract numeric value if it's a dict
        if isinstance(value, dict):
            value = value.get('value', value)
        
        # Convert to float
        try:
            value = float(value)
        except (ValueError, TypeError):
            return {
                'test_name': test_name,
                'value': str(value),
                'status': 'error',
                'message': f'Invalid numeric value: {value}'
            }
        
        test_name_lower = test_name.lower().replace(' ', '_')
        
        if test_name_lower not in self.reference_ranges:
            return {
                'test_name': test_name,
                'value': value,
                'status': 'unknown',
                'message': 'Reference range not available for this test'
            }
        
        ref = self.reference_ranges[test_name_lower]
        
        # Determine status
        status = TestStatus.NORMAL
        flag = ''
        interpretation = ''
        
        if ref.critical_low and value < ref.critical_low:
            status = TestStatus.CRITICAL_LOW
            flag = '⚠️ CRITICAL LOW'
            interpretation = f'Value critically below normal range. Immediate clinical attention recommended.'
        elif ref.critical_high and value > ref.critical_high:
            status = TestStatus.CRITICAL_HIGH
            flag = '⚠️ CRITICAL HIGH'
            interpretation = f'Value critically above normal range. Immediate clinical attention recommended.'
        elif value < ref.min_normal:
            status = TestStatus.LOW
            flag = '↓ LOW'
            interpretation = f'Value below normal range. Clinical correlation advised.'
        elif value > ref.max_normal:
            status = TestStatus.HIGH
            flag = '↑ HIGH'
            interpretation = f'Value above normal range. Clinical correlation advised.'
        else:
            flag = '✓'
            interpretation = 'Value within normal range.'
        
        return {
            'test_name': ref.name,
            'value': value,
            'unit': ref.unit,
            'reference_range': f'{ref.min_normal}-{ref.max_normal}',
            'status': status.value,
            'flag': flag,
            'interpretation': interpretation
        }
    
    def analyze_panel(self, lab_results: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze a complete lab panel
        Returns comprehensive analysis with abnormal value highlighting
        """
        analyzed_results = []
        abnormal_findings = []
        critical_findings = []
        
        for test_name, value in lab_results.items():
            result = self.analyze_value(test_name, value)
            analyzed_results.append(result)
            
            if result['status'] in ['low', 'high']:
                abnormal_findings.append(result)
            
            if result['status'] in ['critical_low', 'critical_high']:
                critical_findings.append(result)
        
        # Generate summary
        total_tests = len(analyzed_results)
        abnormal_count = len(abnormal_findings)
        critical_count = len(critical_findings)
        
        summary = {
            'total_tests': total_tests,
            'normal_count': total_tests - abnormal_count,
            'abnormal_count': abnormal_count,
            'critical_count': critical_count
        }
        
        # Generate interpretive summary text
        summary_text = []
        if critical_count > 0:
            summary_text.append(f'{critical_count} critical value(s) requiring immediate attention.')
        if abnormal_count > 0:
            summary_text.append(f'{abnormal_count} abnormal value(s) noted.')
        if abnormal_count == 0 and critical_count == 0:
            summary_text.append('All values within normal reference ranges.')
        
        return {
            'status': 'success',
            'summary': summary,
            'summary_text': ' '.join(summary_text),
            'results': analyzed_results,
            'abnormal_findings': abnormal_findings,
            'critical_findings': critical_findings,
            'disclaimer': 'Laboratory results for clinical correlation only. Not a medical diagnosis.'
        }
    
    def parse_csv_results(self, csv_data: str) -> Dict[str, float]:
        """
        Parse CSV format lab results
        Expected format: test_name,value
        """
        results = {}
        lines = csv_data.strip().split('\n')
        
        for line in lines[1:]:  # Skip header
            if ',' in line:
                parts = line.split(',')
                if len(parts) >= 2:
                    test_name = parts[0].strip().lower().replace(' ', '_')
                    try:
                        value = float(parts[1].strip())
                        results[test_name] = value
                    except ValueError:
                        continue
        
        return results


def analyze_lab_results(lab_data: Dict[str, float]) -> Dict[str, Any]:
    """
    Main entry point for lab analysis
    """
    analyzer = LabResultAnalyzer()
    return analyzer.analyze_panel(lab_data)


if __name__ == "__main__":
    # Test the analyzer
    test_data = {
        'hemoglobin': 11.5,
        'glucose': 110,
        'sodium': 138,
        'potassium': 3.8
    }
    
    result = analyze_lab_results(test_data)
    print(json.dumps(result, indent=2))

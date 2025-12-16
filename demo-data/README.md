# Demo Data for Medical Report Drafting System

This directory contains sample data for testing the medical report system.

## Sample Patient Data

### Patient 1
- **ID**: P12345
- **Name**: John Doe
- **Age**: 45
- **Gender**: M
- **Study Date**: 2025-12-16
- **Image Type**: X-Ray

### Lab Results (Patient 1)
```json
{
  "hemoglobin": 11.5,
  "wbc": 8.2,
  "glucose": 110,
  "creatinine": 0.9,
  "sodium": 138,
  "potassium": 3.8
}
```

### Patient 2
- **ID**: P67890
- **Name**: Jane Smith
- **Age**: 52
- **Gender**: F
- **Study Date**: 2025-12-16
- **Image Type**: MRI

### Lab Results (Patient 2)
```json
{
  "hemoglobin": 13.2,
  "wbc": 7.5,
  "glucose": 95,
  "creatinine": 1.0,
  "sodium": 140,
  "potassium": 4.2,
  "alt": 45,
  "ast": 32
}
```

## Sample CSV Format

For bulk lab imports, use this CSV format:

```csv
test_name,value
hemoglobin,11.5
wbc,8.2
glucose,110
creatinine,0.9
sodium,138
potassium,3.8
```

## Test Images

For testing, use any of the following:
- Chest X-Ray images (PNG, JPG)
- MRI scan images
- CT scan images

Place test images in `/tmp/medical_images/` before analysis.

## API Testing

### Upload and Analyze Image
```bash
curl -X POST http://localhost:3000/medical/analyze-image \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P12345",
    "patient_name": "John Doe",
    "age": "45",
    "gender": "M",
    "study_date": "2025-12-16",
    "image_type": "xray",
    "image_path": "/tmp/medical_images/test_xray.jpg"
  }'
```

### Analyze Lab Results
```bash
curl -X POST http://localhost:3000/medical/analyze-labs \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION-P12345-2025-12-16",
    "lab_data": {
      "hemoglobin": 11.5,
      "wbc": 8.2,
      "glucose": 110,
      "creatinine": 0.9,
      "sodium": 138,
      "potassium": 3.8
    }
  }'
```

### Generate Report
```bash
curl -X POST http://localhost:3000/medical/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION-P12345-2025-12-16"
  }'
```

### Approve Report
```bash
curl -X POST http://localhost:3000/medical/approve-report \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION-P12345-2025-12-16",
    "report_id": "RPT-20251216-123456",
    "approved": true,
    "reviewer_name": "Dr. Smith",
    "reviewer_comments": "Report reviewed and approved"
  }'
```

### Get Report
```bash
curl http://localhost:3000/medical/report/SESSION-P12345-2025-12-16
```

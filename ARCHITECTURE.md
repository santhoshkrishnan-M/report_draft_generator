# Medical Report Drafting System - Architecture & Workflows

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                  (React + Tailwind CSS)                         │
│                                                                 │
│  Dashboard → Processing → Report Review → Final Report         │
│               Status                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      MOTIA BACKEND                              │
│                 (Workflow Orchestration)                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  WORKFLOW STEPS                          │  │
│  │                                                          │  │
│  │  1. Image Analysis Step (API)                          │  │
│  │      ↓                                                  │  │
│  │  2. Lab Analysis Step (API)                            │  │
│  │      ↓                                                  │  │
│  │  3. Report Generation Step (API)                       │  │
│  │      ↓                                                  │  │
│  │  4. Report Approval Step (API - Human Review)          │  │
│  │      ↓                                                  │  │
│  │  5. Get Report Step (API)                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              STATE MANAGEMENT                            │  │
│  │  • Patient Info      • Lab Results                       │  │
│  │  • Imaging Results   • Draft Reports                     │  │
│  │  • Final Reports     • PDF Paths                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────┬─────────────────────┘
             │                            │
             │ Python                     │ Python
             │                            │
┌────────────▼──────────┐    ┌────────────▼──────────┐
│   IMAGE AGENT         │    │   LAB AGENT           │
│   (Python/OpenCV)     │    │   (Python Rules)      │
│                       │    │                       │
│  • Image Loading      │    │  • Reference Ranges   │
│  • Preprocessing      │    │  • Value Comparison   │
│  • Feature Extract    │    │  • Flag Abnormals     │
│  • Observation Gen    │    │  • Critical Detection │
└───────────────────────┘    └───────────────────────┘
             │                            │
             │                            │
             └────────────┬───────────────┘
                          │
             ┌────────────▼──────────┐
             │   REPORT AGENT        │
             │   (Python NLP)        │
             │                       │
             │  • Template Engine    │
             │  • Section Generator  │
             │  • Safe Language      │
             │  • Structured Output  │
             └────────────┬──────────┘
                          │
             ┌────────────▼──────────┐
             │   PDF SERVICE         │
             │   (ReportLab)         │
             │                       │
             │  • Medical Layout     │
             │  • Professional Style │
             │  • Header/Footer      │
             │  • Export to PDF      │
             └───────────────────────┘
```

## Workflow Sequences

### Workflow 1: Image Analysis

```
User → Dashboard → Upload Image
                   ↓
              Image Analysis API
                   ↓
          Image Processor (OpenCV)
          • Load image
          • Normalize & enhance
          • Extract features
          • Generate observations
                   ↓
           Store in State
           (imaging_result_*)
                   ↓
        Emit "image-analyzed" event
                   ↓
           Return session_id
```

### Workflow 2: Laboratory Analysis

```
User → Processing Status → Enter Lab Values
                           ↓
                    Lab Analysis API
                           ↓
                  Lab Analyzer (Rules)
                  • Parse values
                  • Compare to ranges
                  • Flag abnormals
                  • Detect critical values
                           ↓
                   Store in State
                   (lab_result_*)
                           ↓
              Emit "labs-analyzed" event
                           ↓
           Auto-trigger Report Generation
```

### Workflow 3: Report Generation

```
Processing Status → Generate Report API
                           ↓
                  Retrieve from State:
                  • Patient info
                  • Imaging results
                  • Lab results
                           ↓
               Report Generator (NLP)
               • Patient info section
               • Exam summary
               • Imaging findings
               • Lab findings
               • Interpretive notes
               • Recommendations
               • Disclaimer
                           ↓
                   Store Draft Report
                   (draft_report_*)
                           ↓
              Emit "report-generated" event
                           ↓
              Navigate to Review Page
```

### Workflow 4: Human Review & Approval

```
User → Report Review → Review Draft
                       ↓
            Radiologist Decision
                   ↙       ↘
              APPROVE      REJECT
                ↓            ↓
        Approval API    Rejection API
                ↓            ↓
       PDF Generation   Store Rejection
              ↓              ↓
      Store Final      Return to Edit
      (final_report_*)
              ↓
    Emit "report-approved"
              ↓
       Navigate to Final
```

### Workflow 5: PDF Download

```
User → Final Report → Download Button
                      ↓
               Get PDF Path from State
                      ↓
               Serve PDF File
                      ↓
            Browser Download
```

## State Management

### State Keys

```javascript
// Patient Information
patient_info_{session_id}

// Analysis Results
imaging_result_{session_id}
lab_result_{session_id}

// Reports
draft_report_{session_id}
final_report_{session_id}

// Metadata
pdf_path_{session_id}
rejection_{session_id}
```

### State Flow

```
Session Creation (Image Upload)
    ↓
patient_info_* ────────────────┐
imaging_result_* ──────────────┤
    ↓                          │
lab_result_* ──────────────────┤ → Report Generation
    ↓                          │
draft_report_* ────────────────┘
    ↓
Human Review
    ↓
final_report_*
pdf_path_*
```

## API Contracts

### Image Analysis Endpoint

**Request:**
```typescript
{
  patient_id: string
  patient_name: string
  age: string
  gender: "M" | "F" | "O"
  study_date: string (YYYY-MM-DD)
  image_type: "xray" | "mri" | "ct"
  image_path: string
}
```

**Response:**
```typescript
{
  status: "success" | "error"
  session_id: string
  patient_id: string
  message: string
}
```

### Lab Analysis Endpoint

**Request:**
```typescript
{
  session_id: string
  lab_data: {
    [test_name: string]: number
  }
}
```

**Response:**
```typescript
{
  status: "success" | "error"
  session_id: string
  message: string
  abnormal_count: number
  critical_count: number
}
```

### Report Generation Endpoint

**Request:**
```typescript
{
  session_id: string
}
```

**Response:**
```typescript
{
  status: "success" | "error"
  session_id: string
  report_id: string
  message: string
  requires_approval: boolean
}
```

### Report Approval Endpoint

**Request:**
```typescript
{
  session_id: string
  report_id: string
  approved: boolean
  reviewer_name: string
  reviewer_comments?: string
  edited_report?: ReportObject
}
```

**Response:**
```typescript
{
  status: "approved" | "rejected" | "error"
  session_id: string
  report_id: string
  pdf_path?: string
  message: string
}
```

## Data Models

### Patient Information
```typescript
{
  patient_id: string
  patient_name: string
  age: string
  gender: string
  study_date: string
}
```

### Imaging Result
```typescript
{
  status: "success" | "error"
  image_type: string
  image_path: string
  observations: string[]
  features: {
    mean_intensity: number
    std_intensity: number
    edge_density: number
    texture_variance: number
    ...
  }
  image_dimensions: {
    height: number
    width: number
  }
  disclaimer: string
}
```

### Lab Result
```typescript
{
  status: "success"
  summary: {
    total_tests: number
    normal_count: number
    abnormal_count: number
    critical_count: number
  }
  results: Array<{
    test_name: string
    value: number
    unit: string
    reference_range: string
    status: "normal" | "low" | "high" | "critical_low" | "critical_high"
    flag: string
    interpretation: string
  }>
  abnormal_findings: Array<TestResult>
  critical_findings: Array<TestResult>
  disclaimer: string
}
```

### Medical Report
```typescript
{
  report_id: string
  generated_date: string (ISO)
  report_version: string
  status: "draft" | "approved" | "rejected"
  requires_approval: boolean
  
  patient_information: PatientInfo
  examination_summary: string
  
  imaging_findings: {
    status: string
    findings: string[]
  }
  
  laboratory_findings: {
    status: string
    findings: string[]
  }
  
  interpretive_notes: string[]
  recommendations: string[]
  disclaimer: string[]
  
  metadata: {
    has_imaging: boolean
    has_labs: boolean
    requires_urgent_review: boolean
  }
  
  reviewer_name?: string
  reviewer_comments?: string
}
```

## Security Considerations

### Data Protection
- Patient data stored in Motia state (in-memory)
- Session-based isolation
- No persistent database (demo version)

### Authentication (Future)
- User login required
- Role-based access (radiologist, physician, admin)
- Session tokens

### Audit Trail (Future)
- Log all report access
- Track modifications
- Record approval/rejection

## Performance Metrics

### Expected Processing Times
- Image Analysis: 2-5 seconds
- Lab Analysis: < 1 second
- Report Generation: 1-2 seconds
- PDF Generation: 2-3 seconds

### Scalability
- Concurrent sessions: Limited by Motia state
- Images per hour: ~720 (single instance)
- Reports per day: ~5,000 (single instance)

## Error Handling

### Service Failures
```
Image Analysis Fails → Return error, log, notify user
Lab Analysis Fails → Return error, log, allow retry
Report Generation Fails → Return error, log, preserve state
PDF Generation Fails → Return error, log, allow retry
```

### State Errors
```
Missing Session → 404 error, user redirected
Missing Data → Prompt user to complete workflow
State Timeout → Session expired message
```

## Monitoring & Logging

### Key Metrics
- API response times
- Error rates
- Report approval rates
- Workflow completion rates
- Critical findings count

### Log Levels
- INFO: Workflow progression
- WARN: Abnormal values, missing data
- ERROR: Service failures, exceptions
- CRITICAL: Data loss, security issues

---

**Version**: 1.0.0  
**Last Updated**: December 16, 2025

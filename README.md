# Medical Report Generation System

An AI-assisted medical diagnostic report drafting system built with Motia framework.

## 🎯 Features

✨ **Complete Medical Workflow**
- Image analysis with OpenCV preprocessing
- Laboratory result analysis with reference ranges
- AI-assisted report generation
- Human-in-the-loop review and approval
- **Professional PDF download** with hospital-grade formatting

🏥 **Clinical-Grade Output**
- Detailed patient information
- Comprehensive imaging and lab findings
- Clinical interpretations and recommendations
- Critical findings highlighted
- Reviewer signature and approval tracking

📄 **PDF Download** (NEW!)
- One-click download from website
- Hospital-style professional formatting
- Complete report with all sections
- Ready for clinical use

## What is Motia?

Motia is an open-source, unified backend framework that eliminates runtime fragmentation by bringing **APIs, background jobs, queueing, streaming, state, workflows, AI agents, observability, scaling, and deployment** into one unified system using a single core primitive, the **Step**.

## Quick Start

```bash
# Start the development server
npm run dev
# or
yarn dev
# or
pnpm dev
```

This starts the Motia runtime and the **Workbench** - a powerful UI for developing and debugging your workflows. By default, it's available at [`http://localhost:3000`](http://localhost:3000).

1. **Open the Workbench** in your browser at [`http://localhost:3000`](http://localhost:3000)
2. **Click the `Tutorial`** button on the top right of the workbench
3. **Complete the `Tutorial`** to get an understanding of the basics of Motia and using the Workbench

## Step Types

Every Step has a `type` that defines how it triggers:

| Type | When it runs | Use case |
|------|--------------|----------|
| **`api`** | HTTP request | REST APIs, webhooks |
| **`event`** | Event emitted | Background jobs, workflows |
| **`cron`** | Schedule | Cleanup, reports, reminders |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Backend dependencies
npm install

# Frontend dependencies
cd frontend && npm install
```

### 2. Start Servers

**Terminal 1 - Backend:**
```bash
npm run dev
```
Backend runs at: http://localhost:3000

**Terminal 2 - Frontend:**
```bash
cd frontend && npm run dev
```
Frontend runs at: http://localhost:5173

### 3. Use the Application

1. Open http://localhost:5173
2. Upload medical image and patient data
3. Enter laboratory results
4. Review AI-generated report
5. Approve report
6. **Download PDF** ⬇️

📖 **Detailed Guide**: See [QUICKSTART_PDF.md](./QUICKSTART_PDF.md)

## 📄 PDF Download Feature

The system generates professional, hospital-grade PDF reports:

- ✅ Comprehensive patient information
- ✅ Detailed imaging and lab findings
- ✅ Clinical interpretations
- ✅ Reviewer approval signature
- ✅ Medical disclaimers
- ✅ Critical findings highlighted

**Test PDF Generation:**
```bash
python_modules/bin/python test_pdf_generation.py
```

📘 **Full Documentation**: [PDF_DOWNLOAD_GUIDE.md](./PDF_DOWNLOAD_GUIDE.md)

## Development Commands

```bash
# Start backend development server
npm run dev

# Start frontend development server
cd frontend && npm run dev

# Test PDF generation
python_modules/bin/python test_pdf_generation.py

# Run with custom port
npm run dev -- --port 3001
```

## Project Structure

```
steps/              # Your Step definitions (or use src/)
src/                 # Shared services and utilities
motia.config.ts      # Motia configuration
requirements.txt     # Python dependencies
```

Steps are auto-discovered from your `steps/` or `src/` directories - no manual registration required. You can write Steps in Python, TypeScript, or JavaScript, all in the same project.

## Tutorial

This project includes an interactive tutorial that will guide you through:
- Understanding Steps and their types
- Creating API endpoints
- Building event-driven workflows
- Using state management
- Observing your flows in the Workbench

## Learn More

- [Documentation](https://motia.dev/docs) - Complete guides and API reference
- [Quick Start Guide](https://motia.dev/docs/getting-started/quick-start) - Detailed getting started tutorial
- [Core Concepts](https://motia.dev/docs/concepts/overview) - Learn about Steps and Motia architecture
- [Discord Community](https://discord.gg/motia) - Get help and connect with other developers

---

# Medical Report Drafting System

## 🏥 Overview

An AI-assisted medical report drafting system built on the Motia framework that helps radiologists and physicians generate structured diagnostic reports from imaging studies and laboratory results.

**IMPORTANT**: This system generates DRAFT reports only. All reports require human expert review and approval before clinical use.

## ✨ Features

- **Image Analysis**: Process X-ray, MRI, and CT scan images using OpenCV
- **Laboratory Analysis**: Analyze lab results against reference ranges with automatic flagging
- **Report Generation**: Template-based medical report generation with safe, non-diagnostic language
- **Human-in-the-Loop**: Mandatory radiologist review and approval workflow
- **PDF Export**: Professional medical-grade PDF report generation
- **Clean Medical UI**: React + Tailwind CSS interface designed for medical professionals

## 🏗️ Architecture

### Tech Stack

- **Backend**: Motia framework + Node.js
- **Workflow**: Motia Steps (API, Event-driven)
- **Image Processing**: Python + OpenCV + NumPy
- **Lab Analysis**: Python rule-based analyzer
- **Report Generation**: Python template-based NLP
- **PDF Export**: ReportLab
- **Frontend**: React + Tailwind CSS
- **State Management**: Motia State Plugin

### Workflow Pipeline

```
1. Image Upload → Image Preprocessing → Feature Extraction → Observations JSON
2. Lab Input → Reference Range Comparison → Abnormal Value Highlighting → Lab Summary JSON
3. Observations + Lab Summary → Structured Report Template → Draft Report
4. Draft Report → Editable Review UI → Approve/Edit → Final Report + PDF
```

## 📁 Project Structure

```
reportgen/
├── src/
│   ├── medical/                      # Medical workflow steps
│   │   ├── image_analysis_step.py    # Image upload & analysis
│   │   ├── lab_analysis_step.py      # Lab results analysis
│   │   ├── report_generation_step.py # Report generation
│   │   ├── report_approval_step.py   # Human review & approval
│   │   └── get_report_step.py        # Report retrieval
│   └── petstore/                     # Original tutorial steps
│
├── services/
│   ├── image-agent/                  # Image processing service
│   │   ├── image_processor.py        # OpenCV image analysis
│   │   └── api.py                    # FastAPI service
│   ├── lab-agent/                    # Lab analysis service
│   │   └── lab_analyzer.py           # Reference range analyzer
│   ├── report-agent/                 # Report generation service
│   │   └── report_generator.py       # Template-based report builder
│   └── pdf-service/                  # PDF export service
│       └── pdf_generator.py          # ReportLab PDF creator
│
├── frontend/                         # React UI
│   └── src/
│       ├── components/
│       │   ├── Dashboard.jsx         # Upload interface
│       │   ├── ProcessingStatus.jsx  # Workflow status
│       │   ├── ReportReview.jsx      # Review & approval
│       │   └── FinalReport.jsx       # Final report & PDF download
│       ├── App.jsx                   # Main app
│       └── main.jsx                  # Entry point
│
├── demo-data/                        # Sample test data
├── motia.config.ts                   # Motia configuration
├── requirements.txt                  # Python dependencies
└── package.json                      # Node dependencies
```

## 🚀 Setup & Installation

### Prerequisites

- Node.js 18+
- Python 3.9+
- npm/yarn/pnpm

### Installation

```bash
# Install Node dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Or use the existing virtual environment
source python_modules/bin/activate
pip install -r requirements.txt
```

### Development

```bash
# Start Motia backend (includes Workbench)
npm run dev

# In another terminal, start the frontend
cd frontend
npm install
npm run dev
```

The system will be available at:
- **Frontend UI**: http://localhost:3001
- **Motia Workbench**: http://localhost:3000
- **API Endpoints**: http://localhost:3000/medical/*

## 📋 API Endpoints

### Medical Report Workflow

#### 1. Analyze Image
```http
POST /medical/analyze-image
Content-Type: application/json

{
  "patient_id": "P12345",
  "patient_name": "John Doe",
  "age": "45",
  "gender": "M",
  "study_date": "2025-12-16",
  "image_type": "xray",
  "image_path": "/tmp/medical_images/xray.jpg"
}
```

#### 2. Analyze Labs
```http
POST /medical/analyze-labs
Content-Type: application/json

{
  "session_id": "SESSION-P12345-2025-12-16",
  "lab_data": {
    "hemoglobin": 11.5,
    "wbc": 8.2,
    "glucose": 110,
    "creatinine": 0.9,
    "sodium": 138,
    "potassium": 3.8
  }
}
```

#### 3. Generate Report
```http
POST /medical/generate-report
Content-Type: application/json

{
  "session_id": "SESSION-P12345-2025-12-16"
}
```

#### 4. Approve Report
```http
POST /medical/approve-report
Content-Type: application/json

{
  "session_id": "SESSION-P12345-2025-12-16",
  "report_id": "RPT-20251216-123456",
  "approved": true,
  "reviewer_name": "Dr. Smith",
  "reviewer_comments": "Reviewed and approved"
}
```

#### 5. Get Report
```http
GET /medical/report/{session_id}
```

## 🧪 Testing

### Using the UI

1. Open http://localhost:3001
2. Fill in patient information
3. Upload a diagnostic image
4. Enter laboratory results
5. Review the generated draft report
6. Approve or reject the report
7. Download the final PDF

### Using cURL

See `demo-data/README.md` for sample API calls.

### Sample Data

Sample patient data and lab results are available in the `demo-data/` directory.

## 🔐 Medical Compliance & Safety

### Disclaimers

⚠️ **CRITICAL SAFETY INFORMATION**

- This system generates **DRAFT REPORTS ONLY**
- **NOT a medical diagnosis or treatment recommendation**
- **NOT a substitute for professional medical judgment**
- **MUST be reviewed by a licensed radiologist/physician**
- AI analysis may contain errors or omissions
- Clinical correlation with patient history is essential

### Language Safety

The system uses only safe, non-diagnostic language:
- "Findings suggest..." (not "Diagnosis:")
- "Clinical correlation recommended"
- "For radiologist review only"
- "Further evaluation advised"

### Human-in-the-Loop

- **Mandatory radiologist approval** before finalization
- Editable report sections
- Reviewer identification tracked
- Reject/revise workflow available

## 📊 Supported Lab Tests

The system includes reference ranges for:

**Hematology**: Hemoglobin, WBC, Platelets, Hematocrit, RBC

**Chemistry**: Glucose, Creatinine, BUN, Sodium, Potassium, Calcium, ALT, AST, Bilirubin

**Lipid Panel**: Total Cholesterol, HDL, LDL, Triglycerides

## 🎨 UI Features

- Clean medical-grade design
- Professional color scheme (blue, white, gray)
- Real-time workflow status
- Highlight critical findings
- Mobile-responsive layout
- Accessible interface

## 🐛 Troubleshooting

### Python Module Not Found

```bash
# Activate virtual environment
source python_modules/bin/activate
pip install -r requirements.txt
```

### Frontend Not Loading

```bash
cd frontend
npm install
npm run dev
```

### Motia Workbench Issues

```bash
# Clean and restart
npm run clean
npm install
npm run dev
```

## 📝 License

This project is for educational and demonstration purposes. Medical report systems must comply with local healthcare regulations (HIPAA, etc.) before clinical use.

## 🤝 Contributing

This is a hackathon/demo project. For production medical systems, consult healthcare IT specialists and ensure regulatory compliance.

## 📞 Support

For Motia framework questions:
- [Motia Documentation](https://motia.dev/docs)
- [Discord Community](https://discord.gg/motia)

---

**Built with ❤️ using the Motia Framework**
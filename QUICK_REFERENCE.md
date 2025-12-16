# Medical Report Drafting System - Quick Reference

## 🚀 Quick Start Commands

```bash
# Start everything
./start.sh

# Or manual start
npm run dev                    # Backend (Terminal 1)
cd frontend && npm run dev     # Frontend (Terminal 2)
```

## 🌐 URLs

- **Frontend UI**: http://localhost:3001
- **Motia Workbench**: http://localhost:3000
- **API Base**: http://localhost:3000/medical

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/medical/analyze-image` | Upload & analyze diagnostic image |
| POST | `/medical/analyze-labs` | Analyze laboratory results |
| POST | `/medical/generate-report` | Generate draft medical report |
| POST | `/medical/approve-report` | Approve/reject report (human review) |
| GET | `/medical/report/{session_id}` | Retrieve report |

## 📊 Common Lab Tests

| Test | Normal Range | Unit | Critical Low | Critical High |
|------|--------------|------|--------------|---------------|
| Hemoglobin | 12.0-16.0 | g/dL | < 7.0 | > 20.0 |
| WBC | 4.0-11.0 | ×10³/μL | < 2.0 | > 30.0 |
| Glucose | 70-100 | mg/dL | < 40 | > 400 |
| Creatinine | 0.6-1.2 | mg/dL | < 0.2 | > 10.0 |
| Sodium | 136-145 | mEq/L | < 120 | > 160 |
| Potassium | 3.5-5.0 | mEq/L | < 2.5 | > 7.0 |

## 🔄 Workflow Steps

1. **Dashboard** → Upload image + patient info → Get session_id
2. **Processing** → Enter lab results → Auto-generate report
3. **Review** → Radiologist reviews draft → Approve/Reject
4. **Final** → Download PDF report

## 📁 Key Files

### Backend
```
src/medical/
  ├── image_analysis_step.py      # Image upload endpoint
  ├── lab_analysis_step.py        # Lab analysis endpoint
  ├── report_generation_step.py   # Report generation
  ├── report_approval_step.py     # Human review
  └── get_report_step.py          # Report retrieval
```

### Services
```
services/
  ├── image-agent/image_processor.py   # OpenCV processing
  ├── lab-agent/lab_analyzer.py        # Lab analysis logic
  ├── report-agent/report_generator.py # Report templates
  └── pdf-service/pdf_generator.py     # PDF creation
```

### Frontend
```
frontend/src/
  ├── App.jsx                     # Main app
  └── components/
      ├── Dashboard.jsx           # Upload interface
      ├── ProcessingStatus.jsx    # Lab entry + status
      ├── ReportReview.jsx        # Review UI
      └── FinalReport.jsx         # PDF download
```

## 🧪 Testing

### Test with Demo Data
```bash
# View sample data
cat demo-data/sample_patient_1.json
cat demo-data/sample_labs_1.json

# Test API
curl -X POST http://localhost:3000/medical/analyze-image \
  -H "Content-Type: application/json" \
  -d @demo-data/sample_patient_1.json
```

### Using UI
1. Open http://localhost:3001
2. Fill form with demo data
3. Upload any medical image
4. Complete workflow

## ⚙️ Configuration

### Motia Config
```typescript
// motia.config.ts
export default defineConfig({
  plugins: [observabilityPlugin, statesPlugin, endpointPlugin, logsPlugin, bullmqPlugin]
})
```

### Frontend Proxy
```javascript
// vite.config.js
proxy: {
  '/medical': {
    target: 'http://localhost:3000',
    changeOrigin: true,
  }
}
```

## 🐛 Common Issues

### "Module not found"
```bash
source python_modules/bin/activate
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Kill process on port 3000
sudo lsof -t -i:3000 | xargs kill -9

# Or change port in configs
```

### "Frontend can't connect"
```bash
# Check proxy in vite.config.js
# Ensure backend is running first
```

### "Step not found"
```bash
npm run generate-types
npm run dev
```

## 💾 State Keys

| Key Pattern | Stores |
|-------------|--------|
| `patient_info_{session_id}` | Patient demographics |
| `imaging_result_{session_id}` | Image analysis results |
| `lab_result_{session_id}` | Lab analysis results |
| `draft_report_{session_id}` | Generated draft report |
| `final_report_{session_id}` | Approved final report |
| `pdf_path_{session_id}` | PDF file location |

## 📝 Medical Language Guidelines

### ✅ Safe Language
- "Findings suggest..."
- "Clinical correlation recommended"
- "For radiologist review only"
- "Further evaluation advised"

### ❌ Avoid
- "Diagnosis: ..."
- "Treatment: ..."
- "Prescribe..."
- Definitive diagnostic statements

## 🔐 Security Checklist (Production)

- [ ] Add authentication
- [ ] Implement RBAC
- [ ] Enable HTTPS
- [ ] Encrypt patient data
- [ ] Add audit logging
- [ ] Input validation
- [ ] Rate limiting
- [ ] HIPAA compliance
- [ ] Regular backups
- [ ] Security monitoring

## 📞 Support

- **Motia Docs**: https://motia.dev/docs
- **Motia Discord**: https://discord.gg/motia
- **GitHub Issues**: [Create issue]
- **Setup Guide**: See SETUP_GUIDE.md
- **Architecture**: See ARCHITECTURE.md

## 🎯 Project Structure

```
reportgen/
├── src/medical/           # Motia workflow steps
├── services/              # Python analysis services
├── frontend/              # React UI
├── demo-data/             # Sample test data
├── start.sh               # Quick start script
├── README.md              # Main documentation
├── SETUP_GUIDE.md         # Detailed setup
├── ARCHITECTURE.md        # System architecture
└── QUICK_REFERENCE.md     # This file
```

## 🚨 Important Disclaimers

⚠️ **CRITICAL**: This system generates **DRAFT REPORTS ONLY**

- NOT a medical diagnosis
- NOT a treatment recommendation
- Requires human expert review
- For educational/demo purposes
- Consult medical professionals

## 📚 Resources

- **OpenCV**: https://docs.opencv.org/
- **ReportLab**: https://www.reportlab.com/docs/
- **React**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Vite**: https://vitejs.dev/

---

**Quick Start**: `./start.sh` → Open http://localhost:3001

**Version**: 1.0.0

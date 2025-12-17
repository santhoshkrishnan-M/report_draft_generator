# Quick Start Guide - PDF Download Feature

## 🚀 Getting Started

Your medical report system now includes a professional PDF download feature!

### Prerequisites

✅ Backend server running (port 3000)
✅ Frontend server running (port 5173)
✅ Python environment with reportlab installed

## 📋 Complete Workflow

### 1. Start the Servers

**Terminal 1 - Backend:**
```bash
cd reportgen
npm run dev
```
Server runs at: http://localhost:3000

**Terminal 2 - Frontend:**
```bash
cd reportgen/frontend
npm run dev
```
Frontend runs at: http://localhost:5173

### 2. Use the Application

1. **Open Browser**: Navigate to http://localhost:5173

2. **Dashboard (Step 1)**: 
   - Enter patient information
   - Upload medical image
   - Click "Analyze Image"

3. **Processing Status (Step 2)**:
   - Enter laboratory test results
   - Click "Submit Lab Results"
   - Wait for report generation

4. **Report Review (Step 3)**:
   - Review the AI-generated draft report
   - Enter reviewer name and comments
   - Click "Approve Report"

5. **Final Report (Step 4)**:
   - ✨ **Click "Download PDF Report"** ✨
   - PDF downloads automatically to your Downloads folder
   - File name: `RPT-XXXXXXXXX-XXXXXX.pdf`

## 📄 What's in the PDF?

Your downloaded PDF includes:

### Document Sections
- **Header**: Professional blue header with report metadata
- **Patient Information**: Complete demographics table
- **Examination Summary**: Detailed clinical context
- **Imaging Findings**: Numbered list with critical items highlighted in red
- **Laboratory Findings**: Test results with reference ranges
  - Abnormal values clearly marked
  - Critical values in bold red text
- **Interpretive Notes**: Clinical interpretation and analysis
- **Recommendations**: Actionable clinical recommendations
- **Reviewer Information**: Signature section with reviewer name and date
- **Disclaimer**: Medical disclaimer in highlighted box
- **Footer**: Page numbers and confidentiality notice

### Professional Features
- ✓ Hospital-grade formatting
- ✓ Clear section headings
- ✓ Professional typography
- ✓ Proper spacing and alignment
- ✓ Critical findings highlighted
- ✓ Page numbers on every page
- ✓ Confidential document watermark

## 🧪 Testing the Feature

### Test PDF Generation (Standalone)

Generate a sample PDF without running the full workflow:

```bash
cd reportgen
python_modules/bin/python test_pdf_generation.py
```

This creates: `outputs/pdfs/RPT-20251217-TEST-001.pdf`

### View Generated PDF

**Linux:**
```bash
xdg-open outputs/pdfs/RPT-20251217-TEST-001.pdf
```

**Or navigate to:**
```
reportgen/outputs/pdfs/
```

## 🔍 API Testing

Test the download endpoint directly:

```bash
# Start backend
cd reportgen && npm run dev

# In another terminal, download a report
curl -X GET http://localhost:3000/medical/report/<SESSION_ID>/download \
  --output test-report.pdf

# View the downloaded PDF
xdg-open test-report.pdf
```

Replace `<SESSION_ID>` with an actual session ID from an approved report.

## 🐛 Troubleshooting

### Issue: "PDF not found" error

**Cause**: Report not approved yet

**Solution**: 
1. Complete the workflow through Step 3
2. Click "Approve Report" in the Review page
3. Then try downloading

### Issue: Download button disabled

**Cause**: Report status is not "approved"

**Solution**: 
- Ensure you've clicked "Approve Report"
- Check that you're on the Final Report page
- Verify the green "APPROVED" badge is visible

### Issue: PDF downloads but doesn't open

**Cause**: PDF viewer not installed

**Solution**:
```bash
# Install PDF viewer
sudo apt-get install evince  # or xpdf, or okular
```

### Issue: Backend errors "PDF generation failed"

**Cause**: Missing Python dependencies

**Solution**:
```bash
cd reportgen
source python_modules/bin/activate
pip install reportlab
```

### Issue: Frontend shows "Failed to download PDF"

**Cause**: Backend not running or wrong port

**Solution**:
1. Check backend is running on port 3000
2. Check browser console for network errors
3. Verify vite.config.js has correct proxy settings

## 📊 File Locations

### Generated PDFs
```
reportgen/
└── outputs/
    └── pdfs/
        ├── RPT-20251217-143052.pdf
        ├── RPT-20251217-145123.pdf
        └── ...
```

### Source Code
```
reportgen/
├── services/pdf-service/
│   └── pdf_generator.py          # PDF generation logic
├── src/medical/
│   ├── download_pdf_step.py      # Download endpoint
│   └── report_approval_step.py   # Triggers PDF generation
└── frontend/src/components/
    └── FinalReport.jsx            # Download UI
```

## 💡 Tips

1. **Test First**: Run `test_pdf_generation.py` before using the full workflow
2. **Check Logs**: Monitor backend terminal for PDF generation messages
3. **Browser Console**: Check for JavaScript errors if download fails
4. **File Size**: PDFs are typically 10-20 KB for standard reports
5. **Cleanup**: Old PDFs in `outputs/pdfs/` can be manually deleted

## 🎯 Success Indicators

You know it's working when:
- ✓ Backend logs show "download_pdf_step.py registered"
- ✓ "Download PDF Report" button appears on Final Report page
- ✓ Button shows spinner while generating
- ✓ PDF file appears in your Downloads folder
- ✓ PDF opens and displays all sections properly

## 📖 Additional Resources

- **Full Documentation**: See `PDF_DOWNLOAD_GUIDE.md`
- **Architecture**: See `ARCHITECTURE.md`
- **API Reference**: See `PDF_DOWNLOAD_GUIDE.md` → API Reference section
- **Security**: See `PDF_DOWNLOAD_GUIDE.md` → Security section

## 🚨 Important Notes

### For Development
- PDFs are stored in `outputs/pdfs/` (excluded from git)
- Each report generates one PDF file
- Files persist until manually deleted

### For Production
Before deploying:
1. Implement file encryption at rest
2. Add audit logging for downloads
3. Set up automatic file cleanup
4. Configure proper access controls
5. Ensure HTTPS for all traffic
6. Add user authentication
7. Implement HIPAA compliance measures

## ✅ Quick Checklist

Before reporting issues:
- [ ] Backend running on port 3000
- [ ] Frontend running on port 5173
- [ ] Report has been approved
- [ ] Green "APPROVED" badge visible
- [ ] Browser allows downloads from localhost
- [ ] No JavaScript console errors
- [ ] Backend logs show no errors
- [ ] `outputs/pdfs/` directory exists

## 🎉 Success!

When everything works:
1. Report is approved ✓
2. Click "Download PDF Report" ✓
3. PDF downloads automatically ✓
4. Open PDF to view professional medical report ✓
5. Share with healthcare providers ✓

---

**Need Help?**
- Check backend logs: Look for PDF generation messages
- Check frontend console: Press F12 in browser
- Test standalone: Run `test_pdf_generation.py`
- Review documentation: See `PDF_DOWNLOAD_GUIDE.md`

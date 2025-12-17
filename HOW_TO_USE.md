🎯 HOW TO USE THE MEDICAL REPORT SYSTEM

⚠️ IMPORTANT: You MUST Complete Steps in Order!

The system has **3 tabs** that must be completed **sequentially**:

```
Dashboard → Processing Status → Report Review
   (Step 1)      (Step 2)           (Step 3)
```

---

📋 Step-by-Step Instructions

Step 1: Dashboard Tab (Upload Image)

1. **Open** http://localhost:5173 in your browser
2. **Click on "Dashboard" tab** (should be already selected)
3. **Fill in the patient form:**
   - Patient ID: `TEST001`
   - Patient Name: `John Doe`
   - Age: `45`
   - Gender: Select `Male`
   - Study Date: Pick today's date
   - Image Type: Select `X-Ray`
4. **Upload an image:**
   - Click "Choose File"
   - Select ANY image from your computer
5. **Click "Analyze Image" button**
6. **Wait** for success message
7. **The system will automatically move to "Processing Status" tab**

Step 2: Processing Status Tab (Add Lab Results)

After image analysis completes:

1. **You'll see the "Processing Status" tab**
2. **Enter lab values** (or use sample values):
   - Hemoglobin: `12.5`
   - WBC: `8.5`
   - Glucose: `95`
   - Creatinine: `1.0`
   - Sodium: `140`
   - Potassium: `4.2`
3. **Click "Add Lab Results" button**
4. **Wait** for success message
5. **Click "Generate Report" button**
6. **Wait** for report generation
7. **The system will move to "Report Review" tab**

Step 3: Report Review Tab (Approve & Download)

After report is generated:

1. **You'll see the draft report**
2. **Review the report content**
3. **Click "Approve Report" button**
4. **Wait** for PDF generation
5. **You'll see the "Download PDF Report" button** (big blue button)
6. **Click it to download your PDF!**

---

�� Common Mistakes

❌ **DON'T** click on "Report Review" tab first  
❌ **DON'T** skip the Dashboard step  
❌ **DON'T** skip the Lab Results step  
✅ **DO** complete each step in order  

---

🔍 Troubleshooting

"Report not found" Error
**Cause:** You didn't complete the Dashboard step  
**Fix:** Click on "Dashboard" tab and start from Step 1

"Image analysis failed"
**Cause:** Backend not responding  
**Fix:** Check if backend is running on port 3000

"Download button not appearing"
**Cause:** Report not approved yet  
**Fix:** Make sure you clicked "Approve Report" in Step 3

---

🧪 Quick Test

Open browser console (F12) and run:
```javascript
// This should show "success"
fetch('http://localhost:3000/medical/analyze-image', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    patient_id: 'TEST',
    patient_name: 'Test',
    age: '30',
    gender: 'Male',
    study_date: '2025-12-17',
    image_type: 'X-Ray',
    image_path: '/tmp/test.png'
  })
}).then(r => r.json()).then(console.log)
```

---

✅ Success Checklist

- [ ] Backend running on port 3000
- [ ] Frontend running on port 5173
- [ ] Browser at http://localhost:5173
- [ ] Started from Dashboard tab
- [ ] Filled patient info
- [ ] Uploaded image
- [ ] Clicked "Analyze Image"
- [ ] Waited for success
- [ ] Added lab results
- [ ] Clicked "Generate Report"
- [ ] Reviewed draft report
- [ ] Clicked "Approve Report"
- [ ] Saw blue "Download PDF Report" button
- [ ] Downloaded PDF successfully! 🎉

---

**Remember: Complete the workflow in order from Dashboard → Processing → Review!**

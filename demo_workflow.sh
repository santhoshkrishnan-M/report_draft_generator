#!/bin/bash

echo "=============================================="
echo "   🏥 MEDICAL REPORT SYSTEM - DEMO WORKFLOW   "
echo "=============================================="
echo ""
echo "This will create a complete medical report with PDF download."
echo ""

# Step 1: Image Analysis
echo "📸 Step 1: Analyzing diagnostic image..."
SESSION_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/analyze-image \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "DEMO001",
    "patient_name": "John Doe",
    "age": "45",
    "gender": "Male",
    "study_date": "2025-12-17",
    "image_type": "X-Ray",
    "image_path": "/tmp/demo_xray.png"
  }')

SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SESSION_ID" ]; then
  echo "❌ Failed to create session. Make sure backend is running on port 3000"
  exit 1
fi

echo "✅ Image analysis complete!"
echo "   Session ID: $SESSION_ID"
echo ""
sleep 2

# Step 2: Lab Analysis
echo "🧪 Step 2: Analyzing laboratory results..."
curl -s -X POST http://localhost:3000/medical/analyze-labs \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"lab_data\": {
      \"hemoglobin\": {\"value\": 13.5, \"unit\": \"g/dL\"},
      \"wbc\": {\"value\": 7.8, \"unit\": \"10^3/μL\"},
      \"glucose\": {\"value\": 95, \"unit\": \"mg/dL\"},
      \"creatinine\": {\"value\": 1.0, \"unit\": \"mg/dL\"},
      \"sodium\": {\"value\": 140, \"unit\": \"mEq/L\"}
    }
  }" > /dev/null

echo "✅ Lab analysis complete!"
echo ""
sleep 2

# Step 3: Generate Report
echo "📄 Step 3: Generating medical report..."
REPORT_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/generate-report \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\"}")

REPORT_ID=$(echo $REPORT_RESPONSE | grep -o '"report_id":"[^"]*"' | cut -d'"' -f4)

echo "✅ Report generated!"
echo "   Report ID: $REPORT_ID"
echo ""
sleep 2

# Step 4: Approve Report
echo "✅ Step 4: Approving report (simulating radiologist)..."
APPROVAL_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/approve-report \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"report_id\": \"$REPORT_ID\",
    \"approved\": true,
    \"reviewer_name\": \"Dr. Sarah Smith\",
    \"reviewer_comments\": \"Report reviewed and approved. All findings are accurate.\"
  }")

PDF_PATH=$(echo $APPROVAL_RESPONSE | grep -o '"pdf_path":"[^"]*"' | cut -d'"' -f4)

echo "✅ Report approved and PDF generated!"
echo "   PDF Path: $PDF_PATH"
echo ""

echo "=============================================="
echo "   ✅ COMPLETE WORKFLOW FINISHED!   "
echo "=============================================="
echo ""
echo "Now in your browser at http://localhost:5173:"
echo ""
echo "1. Go to 'Report Review' tab"
echo "2. You will see the approved report"
echo "3. Click the blue 'Download PDF Report' button"
echo ""
echo "Session ID for UI: $SESSION_ID"
echo ""

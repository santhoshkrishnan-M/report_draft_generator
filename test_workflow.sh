#!/bin/bash

echo "======================================"
echo "Testing Medical Report Workflow"
echo "======================================"
echo ""

SESSION_ID="SESSION-TEST123-2025-12-17"

# Step 1: Image Analysis
echo "Step 1: Analyzing image..."
IMAGE_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/analyze-image \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "TEST123",
    "patient_name": "John Doe",
    "age": "45",
    "gender": "Male",
    "study_date": "2025-12-17",
    "image_type": "X-Ray",
    "image_path": "/tmp/test.png"
  }')
echo "✓ Image Analysis: $IMAGE_RESPONSE"
echo ""

# Step 2: Lab Analysis
echo "Step 2: Analyzing lab results..."
LAB_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/analyze-labs \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"lab_data\": {
      \"hemoglobin\": {\"value\": 12.5, \"unit\": \"g/dL\", \"reference_range\": \"13.5-17.5\"},
      \"wbc\": {\"value\": 8.5, \"unit\": \"10^3/μL\", \"reference_range\": \"4.5-11.0\"}
    }
  }")
echo "✓ Lab Analysis: $LAB_RESPONSE"
echo ""

# Step 3: Generate Report
echo "Step 3: Generating report..."
REPORT_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/generate-report \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\"}")
echo "✓ Report Generation: $REPORT_RESPONSE"
echo ""

# Step 4: Approve Report
echo "Step 4: Approving report..."
APPROVAL_RESPONSE=$(curl -s -X POST http://localhost:3000/medical/approve-report \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"report_id\": \"RPT-20251217-TEST\",
    \"approved\": true,
    \"reviewer_name\": \"Dr. Smith\",
    \"reviewer_comments\": \"Report approved for final distribution\"
  }")
echo "✓ Report Approval: $APPROVAL_RESPONSE"
echo ""

# Step 5: Get Report Status
echo "Step 5: Getting final report..."
GET_RESPONSE=$(curl -s -X GET "http://localhost:3000/medical/get-report?session_id=$SESSION_ID")
echo "✓ Get Report: $GET_RESPONSE"
echo ""

echo "======================================"
echo "Workflow Test Complete!"
echo "======================================"
echo ""
echo "Now open http://localhost:5173 in your browser to use the UI"
echo "The download button will appear after completing all steps"

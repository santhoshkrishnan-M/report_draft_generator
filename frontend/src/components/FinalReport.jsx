import React from 'react'

function FinalReport({ reportData, onReset }) {
  const handleDownloadPDF = () => {
    // In production, this would trigger actual PDF download
    // For now, show message
    if (reportData.pdf_path) {
      alert(`PDF available at: ${reportData.pdf_path}\n\nIn production, this would download the file.`)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Success Banner */}
      <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-green-700">
              <strong>Report Approved!</strong> The medical report has been reviewed and approved by a radiologist.
            </p>
          </div>
        </div>
      </div>

      {/* Report Summary Card */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-6">
        <div className="flex items-center justify-between border-b pb-4 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Final Report Ready</h2>
            <p className="text-sm text-gray-600 mt-1">
              Report ID: {reportData.report_id}
            </p>
          </div>
          <div className="text-right">
            <span className="inline-block bg-green-100 text-green-800 text-sm font-semibold px-4 py-2 rounded-full">
              ✓ APPROVED
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-8">
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Session Information</h3>
            <div className="space-y-1 text-sm">
              <p><strong>Session ID:</strong> {reportData.session_id}</p>
              <p><strong>Status:</strong> Approved & Finalized</p>
            </div>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">Document Information</h3>
            <div className="space-y-1 text-sm">
              <p><strong>Format:</strong> PDF</p>
              <p><strong>Status:</strong> Ready for Download</p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <button
            onClick={handleDownloadPDF}
            className="w-full bg-medical-blue text-white px-6 py-4 rounded-md font-medium hover:bg-blue-700 transition flex items-center justify-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download PDF Report
          </button>

          <button
            onClick={onReset}
            className="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-md font-medium hover:bg-gray-300 transition"
          >
            Start New Report
          </button>
        </div>
      </div>

      {/* Workflow Summary */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Workflow Summary</h3>
        <div className="space-y-3">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4 flex-shrink-0">
              ✓
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-800">Image Analysis</p>
              <p className="text-sm text-gray-600">Diagnostic image processed and analyzed</p>
            </div>
          </div>

          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4 flex-shrink-0">
              ✓
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-800">Laboratory Analysis</p>
              <p className="text-sm text-gray-600">Lab results analyzed against reference ranges</p>
            </div>
          </div>

          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4 flex-shrink-0">
              ✓
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-800">Report Generation</p>
              <p className="text-sm text-gray-600">AI-generated draft report created</p>
            </div>
          </div>

          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4 flex-shrink-0">
              ✓
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-800">Human Review & Approval</p>
              <p className="text-sm text-gray-600">Radiologist reviewed and approved report</p>
            </div>
          </div>

          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4 flex-shrink-0">
              ✓
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-800">PDF Generation</p>
              <p className="text-sm text-gray-600">Final report exported as PDF</p>
            </div>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="mt-6 bg-gray-100 rounded-lg p-6 text-center">
        <p className="text-xs text-gray-600">
          This report was generated using the Medical Report Drafting System.<br/>
          All AI-generated content has been reviewed and approved by a licensed medical professional.
        </p>
      </div>
    </div>
  )
}

export default FinalReport

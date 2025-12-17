import React, { useState } from 'react'
import api from '../api'

function FinalReport({ reportData, onReset }) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState(null)

  const handleDownloadPDF = async () => {
    if (!reportData.session_id) {
      alert('Session ID not found. Cannot download report.')
      return
    }

    setDownloading(true)
    setDownloadError(null)

    try {
      // Call the download endpoint
      const response = await api.get(
        `/medical/report/${reportData.session_id}/download`,
        {
          responseType: 'blob', // Important for binary data
          timeout: 30000, // 30 second timeout
        }
      )

      // Create a blob from the PDF data
      const blob = new Blob([response.data], { type: 'application/pdf' })
      
      // Create a download link and trigger it
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${reportData.report_id || 'medical-report'}.pdf`
      
      // Append to body, click, and remove
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      // Clean up the URL object
      window.URL.revokeObjectURL(url)
      
      console.log('PDF downloaded successfully')
    } catch (error) {
      console.error('PDF download failed:', error)
      
      if (error.response?.status === 404) {
        setDownloadError('PDF not found. Please ensure the report has been approved.')
      } else if (error.code === 'ECONNABORTED') {
        setDownloadError('Download timeout. Please try again.')
      } else {
        setDownloadError('Failed to download PDF. Please try again or contact support.')
      }
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
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

      {/* Error Banner */}
      {downloadError && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{downloadError}</p>
            </div>
            <div className="ml-auto pl-3">
              <button
                onClick={() => setDownloadError(null)}
                className="text-red-500 hover:text-red-700"
              >
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

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
        <div className="space-y-4">
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className={`w-full px-8 py-5 rounded-xl font-bold text-lg shadow-lg transition-all duration-300 flex items-center justify-center ${
              downloading 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-900 to-blue-800 text-white hover:from-blue-800 hover:to-blue-700 hover:shadow-xl transform hover:-translate-y-0.5'
            }`}
          >
            {downloading ? (
              <>
                <svg className="animate-spin h-6 w-6 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating PDF...
              </>
            ) : (
              <>
                <svg className="w-7 h-7 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download PDF Report
              </>
            )}
          </button>

          <button
            onClick={onReset}
            disabled={downloading}
            className={`w-full px-8 py-4 rounded-xl font-semibold text-base shadow-md transition-all duration-300 ${
              downloading
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-gray-200 to-gray-100 text-gray-700 hover:from-gray-300 hover:to-gray-200 hover:shadow-lg transform hover:-translate-y-0.5'
            }`}
          >
            <svg className="w-5 h-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
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

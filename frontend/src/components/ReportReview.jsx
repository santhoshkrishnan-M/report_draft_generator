import React, { useState, useEffect } from 'react'
import axios from 'axios'

function ReportReview({ sessionId, onReportApproved }) {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [reviewerName, setReviewerName] = useState('')
  const [comments, setComments] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchReport()
  }, [sessionId])

  const fetchReport = async () => {
    try {
      const response = await axios.get(`/medical/report/${sessionId}`)
      if (response.data.report) {
        setReport(response.data.report)
      }
    } catch (error) {
      console.error('Error fetching report:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    if (!reviewerName) {
      alert('Please enter your name')
      return
    }

    setSubmitting(true)

    try {
      const response = await axios.post('/medical/approve-report', {
        session_id: sessionId,
        report_id: report.report_id,
        approved: true,
        reviewer_name: reviewerName,
        reviewer_comments: comments
      })

      if (response.data.status === 'approved') {
        onReportApproved(response.data)
      }
    } catch (error) {
      alert(`Error: ${error.message}`)
    } finally {
      setSubmitting(false)
    }
  }

  const handleReject = async () => {
    if (!reviewerName) {
      alert('Please enter your name')
      return
    }

    setSubmitting(true)

    try {
      await axios.post('/medical/approve-report', {
        session_id: sessionId,
        report_id: report.report_id,
        approved: false,
        reviewer_name: reviewerName,
        reviewer_comments: comments
      })

      alert('Report rejected. Workflow can be restarted.')
    } catch (error) {
      alert(`Error: ${error.message}`)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-medical-blue"></div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <p className="text-yellow-800">Report not found. Please complete the workflow first.</p>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Alert Banner */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-yellow-700">
              <strong>Human Review Required:</strong> This is an AI-generated draft report. 
              Please review carefully before approval.
            </p>
          </div>
        </div>
      </div>

      {/* Report Content */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="border-b pb-4 mb-6">
          <h2 className="text-2xl font-bold text-gray-800">MEDICAL DIAGNOSTIC REPORT</h2>
          <p className="text-sm text-gray-600 mt-2">
            Report ID: {report.report_id} | Status: <span className="font-semibold text-yellow-600">DRAFT</span>
          </p>
        </div>

        {/* Patient Information */}
        <section className="mb-6">
          <h3 className="text-lg font-semibold text-medical-blue mb-3">PATIENT INFORMATION</h3>
          <div className="bg-gray-50 rounded p-4 grid grid-cols-2 gap-3 text-sm">
            <div><strong>Patient ID:</strong> {report.patient_information.patient_id}</div>
            <div><strong>Patient Name:</strong> {report.patient_information.patient_name}</div>
            <div><strong>Age:</strong> {report.patient_information.age}</div>
            <div><strong>Gender:</strong> {report.patient_information.gender}</div>
            <div><strong>Study Date:</strong> {report.patient_information.study_date}</div>
          </div>
        </section>

        {/* Examination Summary */}
        <section className="mb-6">
          <h3 className="text-lg font-semibold text-medical-blue mb-3">EXAMINATION SUMMARY</h3>
          <p className="text-gray-700 bg-medical-lightblue p-4 rounded">{report.examination_summary}</p>
        </section>

        {/* Imaging Findings */}
        {report.imaging_findings?.status === 'completed' && (
          <section className="mb-6">
            <h3 className="text-lg font-semibold text-medical-blue mb-3">IMAGING FINDINGS</h3>
            <div className="bg-gray-50 p-4 rounded space-y-2">
              {report.imaging_findings.findings.map((finding, idx) => (
                <p key={idx} className="text-gray-700 text-sm">{finding}</p>
              ))}
            </div>
          </section>
        )}

        {/* Laboratory Findings */}
        {report.laboratory_findings?.status === 'completed' && (
          <section className="mb-6">
            <h3 className="text-lg font-semibold text-medical-blue mb-3">LABORATORY FINDINGS</h3>
            <div className="bg-gray-50 p-4 rounded space-y-2">
              {report.laboratory_findings.findings.map((finding, idx) => (
                <p key={idx} className={`text-sm ${finding.includes('⚠️') || finding.includes('CRITICAL') ? 'text-red-600 font-semibold' : 'text-gray-700'}`}>
                  {finding}
                </p>
              ))}
            </div>
          </section>
        )}

        {/* Interpretive Notes */}
        <section className="mb-6">
          <h3 className="text-lg font-semibold text-medical-blue mb-3">INTERPRETIVE NOTES</h3>
          <div className="bg-medical-lightblue p-4 rounded space-y-2">
            {report.interpretive_notes.map((note, idx) => (
              <p key={idx} className="text-gray-700 text-sm">{note}</p>
            ))}
          </div>
        </section>

        {/* Recommendations */}
        <section className="mb-6">
          <h3 className="text-lg font-semibold text-medical-blue mb-3">RECOMMENDATIONS</h3>
          <div className="bg-gray-50 p-4 rounded space-y-2">
            {report.recommendations.map((rec, idx) => (
              <p key={idx} className="text-gray-700 text-sm">{rec}</p>
            ))}
          </div>
        </section>

        {/* Disclaimer */}
        <section className="border-t pt-4">
          <div className="bg-red-50 border border-red-200 p-4 rounded">
            <p className="text-xs text-red-800 text-center font-semibold">
              ⚠️ AI-GENERATED DRAFT - FOR REVIEW ONLY - NOT A MEDICAL DIAGNOSIS
            </p>
          </div>
        </section>
      </div>

      {/* Review Form */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h3 className="text-xl font-bold text-gray-800 mb-6">Radiologist Review & Approval</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Reviewer Name *
            </label>
            <input
              type="text"
              value={reviewerName}
              onChange={(e) => setReviewerName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
              placeholder="Dr. Smith"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Comments (optional)
            </label>
            <textarea
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
              placeholder="Additional clinical notes or corrections..."
            />
          </div>

          <div className="flex space-x-4 pt-4">
            <button
              onClick={handleApprove}
              disabled={submitting}
              className="flex-1 bg-green-600 text-white px-6 py-3 rounded-md font-medium hover:bg-green-700 transition disabled:bg-gray-400"
            >
              ✓ Approve Report
            </button>
            <button
              onClick={handleReject}
              disabled={submitting}
              className="flex-1 bg-red-600 text-white px-6 py-3 rounded-md font-medium hover:bg-red-700 transition disabled:bg-gray-400"
            >
              ✗ Reject Report
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ReportReview

import React, { useState } from 'react'
import Dashboard from './components/Dashboard'
import ProcessingStatus from './components/ProcessingStatus'
import ReportReview from './components/ReportReview'
import FinalReport from './components/FinalReport'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('dashboard')
  const [sessionId, setSessionId] = useState(null)
  const [reportData, setReportData] = useState(null)

  const handleImageAnalyzed = (session) => {
    setSessionId(session)
    setCurrentView('processing')
  }

  const handleLabsAnalyzed = () => {
    // Auto-generate report after labs
    setTimeout(() => {
      setCurrentView('review')
    }, 1000)
  }

  const handleReportApproved = (report) => {
    setReportData(report)
    setCurrentView('final')
  }

  const resetWorkflow = () => {
    setCurrentView('dashboard')
    setSessionId(null)
    setReportData(null)
  }

  const loadDemoSession = () => {
    // Load the demo session that was created
    setSessionId('SESSION-DEMO001-2025-12-17')
    setCurrentView('final')
    setReportData({
      session_id: 'SESSION-DEMO001-2025-12-17',
      report_id: 'RPT-20251217-125811',
      patient_id: 'DEMO001'
    })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-medical-blue text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Medical Report Drafting System</h1>
              <p className="text-blue-100 mt-2">AI-Assisted Diagnostic Report Generation</p>
            </div>
            <button
              onClick={loadDemoSession}
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg transition transform hover:scale-105 flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
              </svg>
              View Demo Report & Download PDF
            </button>
          </div>
        </div>
      </header>

      {/* Workflow Progress Bar */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-200">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between max-w-4xl mx-auto">
            <div className="flex items-center">
              <div className={`flex items-center justify-center w-10 h-10 rounded-full ${currentView === 'dashboard' ? 'bg-blue-600 text-white' : 'bg-green-500 text-white'} font-bold`}>
                {currentView === 'dashboard' ? '1' : '✓'}
              </div>
              <span className="ml-2 font-semibold">Upload Image</span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-300 relative">
              <div className={`h-full bg-blue-600 transition-all ${currentView !== 'dashboard' ? 'w-full' : 'w-0'}`}></div>
            </div>
            <div className="flex items-center">
              <div className={`flex items-center justify-center w-10 h-10 rounded-full ${currentView === 'processing' ? 'bg-blue-600 text-white' : currentView === 'review' || currentView === 'final' ? 'bg-green-500 text-white' : 'bg-gray-300 text-gray-600'} font-bold`}>
                {currentView === 'dashboard' ? '2' : currentView === 'processing' ? '2' : '✓'}
              </div>
              <span className="ml-2 font-semibold">Add Lab Data</span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-300 relative">
              <div className={`h-full bg-blue-600 transition-all ${currentView === 'review' || currentView === 'final' ? 'w-full' : 'w-0'}`}></div>
            </div>
            <div className="flex items-center">
              <div className={`flex items-center justify-center w-10 h-10 rounded-full ${currentView === 'review' ? 'bg-blue-600 text-white' : currentView === 'final' ? 'bg-green-500 text-white' : 'bg-gray-300 text-gray-600'} font-bold`}>
                {currentView === 'final' ? '✓' : '3'}
              </div>
              <span className="ml-2 font-semibold">Review & Download</span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8 py-4">
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`px-4 py-2 rounded-md font-medium transition ${
                currentView === 'dashboard'
                  ? 'bg-medical-blue text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              Dashboard
            </button>
            {sessionId && (
              <>
                <button
                  onClick={() => setCurrentView('processing')}
                  className={`px-4 py-2 rounded-md font-medium transition ${
                    currentView === 'processing'
                      ? 'bg-medical-blue text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  Processing Status
                </button>
                <button
                  onClick={() => setCurrentView('review')}
                  className={`px-4 py-2 rounded-md font-medium transition ${
                    currentView === 'review'
                      ? 'bg-medical-blue text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  Report Review
                </button>
                {reportData && (
                  <button
                    onClick={() => setCurrentView('final')}
                    className={`px-4 py-2 rounded-md font-medium transition ${
                      currentView === 'final'
                        ? 'bg-medical-blue text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Final Report
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {currentView === 'dashboard' && (
          <Dashboard onImageAnalyzed={handleImageAnalyzed} />
        )}
        {currentView === 'processing' && (
          <ProcessingStatus
            sessionId={sessionId}
            onLabsAnalyzed={handleLabsAnalyzed}
          />
        )}
        {currentView === 'review' && (
          <ReportReview
            sessionId={sessionId}
            onReportApproved={handleReportApproved}
          />
        )}
        {currentView === 'final' && (
          <FinalReport reportData={reportData} onReset={resetWorkflow} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-gray-600">
          <p className="text-sm">
            ⚠️ AI-Generated Reports - For Review Purposes Only - Not a Medical Diagnosis
          </p>
          <p className="text-xs mt-2">
            Medical Report Drafting System v1.0.0 | Built with Motia Framework
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App

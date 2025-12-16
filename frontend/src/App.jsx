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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-medical-blue text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold">Medical Report Drafting System</h1>
          <p className="text-blue-100 mt-2">AI-Assisted Diagnostic Report Generation</p>
        </div>
      </header>

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

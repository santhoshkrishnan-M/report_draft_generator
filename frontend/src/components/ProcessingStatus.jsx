import React, { useState } from 'react'
import api from '../api'

function ProcessingStatus({ sessionId, onLabsAnalyzed }) {
  const [labData, setLabData] = useState({
    hemoglobin: '',
    wbc: '',
    glucose: '',
    creatinine: '',
    sodium: '',
    potassium: ''
  })
  
  const [analyzing, setAnalyzing] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [message, setMessage] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setLabData(prev => ({ ...prev, [name]: value }))
  }

  const handleLabSubmit = async (e) => {
    e.preventDefault()
    setAnalyzing(true)
    setMessage('Analyzing laboratory results...')

    try {
      // Convert to numbers
      const numericLabData = {}
      Object.keys(labData).forEach(key => {
        if (labData[key]) {
          numericLabData[key] = parseFloat(labData[key])
        }
      })

      const response = await api.post('/medical/analyze-labs', {
        session_id: sessionId,
        lab_data: numericLabData
      })

      if (response.data.status === 'success') {
        setMessage('Lab analysis completed!')
        
        // Auto-generate report
        setTimeout(() => {
          generateReport()
        }, 1000)
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`)
      setAnalyzing(false)
    }
  }

  const generateReport = async () => {
    setGenerating(true)
    setMessage('Generating medical report...')

    try {
      const response = await api.post('/medical/generate-report', {
        session_id: sessionId
      })

      if (response.data.status === 'success') {
        setMessage('Report generated! Moving to review...')
        setTimeout(() => {
          onLabsAnalyzed()
        }, 1000)
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`)
    } finally {
      setGenerating(false)
      setAnalyzing(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* AI Disclaimer Banner */}
      <div className="bg-amber-50 border-l-4 border-amber-500 rounded-r-lg shadow-sm p-4 mb-6">
        <div className="flex items-center">
          <svg className="w-5 h-5 text-amber-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="text-sm font-medium text-amber-800">
            Step 2 of 3 - Enter Laboratory Test Results
          </span>
        </div>
      </div>

      {/* Success/Error Messages */}
      {message && (
        <div className={`rounded-lg shadow-sm p-4 mb-6 ${
          analyzing || generating ? 'bg-blue-50 border border-blue-200' : 
          message.includes('Error') ? 'bg-red-50 border border-red-200' : 
          'bg-green-50 border border-green-200'
        }`}>
          <div className="flex items-center">
            {(analyzing || generating) ? (
              <svg className="animate-spin h-5 w-5 text-blue-600 mr-3" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : null}
            <span className={`text-sm font-medium ${
              analyzing || generating ? 'text-blue-800' :
              message.includes('Error') ? 'text-red-800' :
              'text-green-800'
            }`}>
              {message}
            </span>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
        {/* Card Header */}
        <div className="bg-gradient-to-r from-green-700 to-green-600 px-6 py-4">
          <h2 className="text-xl font-bold text-white flex items-center">
            <svg className="w-6 h-6 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            Laboratory Test Results
          </h2>
          <p className="text-green-100 text-sm mt-1">Enter available lab values (all fields optional)</p>
        </div>

        {/* Success Status */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 px-6 py-4 border-b">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4">
              ✓
            </div>
            <div>
              <h3 className="font-semibold text-gray-800">Image Analysis Complete</h3>
              <p className="text-sm text-gray-600">Session ID: {sessionId}</p>
            </div>
          </div>
        </div>

        <form onSubmit={handleLabSubmit} className="space-y-6">
          {/* Card Body */}
          <div className="px-6 py-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Hemoglobin (g/dL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 12.0-16.0</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="hemoglobin"
                  value={labData.hemoglobin}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-green-600 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="13.5"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  WBC (×10³/μL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 4.0-11.0</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="wbc"
                  value={labData.wbc}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-green-600 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="7.5"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Glucose (mg/dL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 70-100</span>
                </label>
                <input
                  type="number"
                  step="1"
                  name="glucose"
                  value={labData.glucose}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-green-600 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="90"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Creatinine (mg/dL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 0.6-1.2</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="creatinine"
                  value={labData.creatinine}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-green-600 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="0.9"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Sodium (mEq/L)
                  <span className="text-xs text-gray-500 ml-2">Normal: 136-145</span>
                </label>
                <input
                  type="number"
                  step="1"
                  name="sodium"
                  value={labData.sodium}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-green-600 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="140"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Potassium (mEq/L)
                  <span className="text-xs text-gray-500 ml-2">Normal: 3.5-5.0</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="potassium"
                  value={labData.potassium}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-green-600 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="4.2"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="px-6 pb-6 flex justify-end">
            <button
              type="submit"
              disabled={analyzing || generating}
              className={`px-8 py-4 rounded-xl font-bold text-lg shadow-lg transition-all duration-300 flex items-center ${
                analyzing || generating
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-green-700 to-green-600 text-white hover:from-green-600 hover:to-green-500 hover:shadow-xl transform hover:-translate-y-0.5'
              }`}
            >
              {analyzing || generating ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </>
              ) : (
                <>
                  <svg className="w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Analyze Labs & Generate Report
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ProcessingStatus

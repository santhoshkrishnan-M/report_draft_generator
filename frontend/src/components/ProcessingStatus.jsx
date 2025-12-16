import React, { useState } from 'react'
import axios from 'axios'

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

      const response = await axios.post('/medical/analyze-labs', {
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
      const response = await axios.post('/medical/generate-report', {
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
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Processing Status</h2>
        
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-4">
              ✓
            </div>
            <div>
              <h3 className="font-semibold">Image Analysis Complete</h3>
              <p className="text-sm text-gray-600">Session ID: {sessionId}</p>
            </div>
          </div>
        </div>

        <form onSubmit={handleLabSubmit} className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Laboratory Results</h3>
            <p className="text-sm text-gray-600 mb-4">Enter available laboratory test values (optional fields)</p>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Hemoglobin (g/dL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 12.0-16.0</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="hemoglobin"
                  value={labData.hemoglobin}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="13.5"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  WBC (×10³/μL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 4.0-11.0</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="wbc"
                  value={labData.wbc}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="7.5"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Glucose (mg/dL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 70-100</span>
                </label>
                <input
                  type="number"
                  step="1"
                  name="glucose"
                  value={labData.glucose}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="90"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Creatinine (mg/dL)
                  <span className="text-xs text-gray-500 ml-2">Normal: 0.6-1.2</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="creatinine"
                  value={labData.creatinine}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="0.9"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sodium (mEq/L)
                  <span className="text-xs text-gray-500 ml-2">Normal: 136-145</span>
                </label>
                <input
                  type="number"
                  step="1"
                  name="sodium"
                  value={labData.sodium}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="140"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Potassium (mEq/L)
                  <span className="text-xs text-gray-500 ml-2">Normal: 3.5-5.0</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="potassium"
                  value={labData.potassium}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="4.2"
                />
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between pt-6 border-t">
            <button
              type="submit"
              disabled={analyzing || generating}
              className="bg-medical-blue text-white px-8 py-3 rounded-md font-medium hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {analyzing || generating ? 'Processing...' : 'Analyze Labs & Generate Report'}
            </button>
            
            {message && (
              <p className={`text-sm ${message.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
                {message}
              </p>
            )}
          </div>
        </form>
      </div>

      {(analyzing || generating) && (
        <div className="mt-6 bg-medical-lightblue rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-medical-blue mr-4"></div>
            <div>
              <p className="font-semibold text-gray-800">
                {analyzing && !generating && 'Analyzing laboratory results...'}
                {generating && 'Generating medical report...'}
              </p>
              <p className="text-sm text-gray-600">Please wait while we process your data</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProcessingStatus

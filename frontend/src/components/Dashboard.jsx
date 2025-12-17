import React, { useState } from 'react'
import api from '../api'

function Dashboard({ onImageAnalyzed }) {
  const [patientInfo, setPatientInfo] = useState({
    patient_id: '',
    patient_name: '',
    age: '',
    gender: 'Male',
    study_date: new Date().toISOString().split('T')[0],
    image_type: 'X-Ray'
  })

  const [selectedImage, setSelectedImage] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [dragActive, setDragActive] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setPatientInfo(prev => ({ ...prev, [name]: value }))
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedImage(e.dataTransfer.files[0])
    }
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
      setMessage('')
    }
  }

  const isFormValid = () => {
    return patientInfo.patient_id && 
           patientInfo.patient_name && 
           patientInfo.age && 
           selectedImage
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!selectedImage) {
      setMessage('Please select a diagnostic image')
      return
    }

    setUploading(true)
    setMessage('')

    try {
      const imagePath = `/tmp/medical_images/${selectedImage.name}`
      
      const response = await api.post('/medical/analyze-image', {
        ...patientInfo,
        image_path: imagePath
      })

      if (response.data.status === 'success') {
        setMessage('Image analysis completed!')
        onImageAnalyzed(response.data.session_id)
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`)
    } finally {
      setUploading(false)
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
            AI-Generated Reports – For Review Purposes Only – Not a Medical Diagnosis
          </span>
        </div>
      </div>

      {/* Success/Error Messages */}
      {message && (
        <div className={`rounded-lg shadow-sm p-4 mb-6 ${
          uploading ? 'bg-blue-50 border border-blue-200' : 
          message.includes('Error') || message.includes('select') ? 'bg-red-50 border border-red-200' : 
          'bg-green-50 border border-green-200'
        }`}>
          <div className="flex items-center">
            {uploading ? (
              <svg className="animate-spin h-5 w-5 text-blue-600 mr-3" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : null}
            <span className={`text-sm font-medium ${
              uploading ? 'text-blue-800' :
              message.includes('Error') || message.includes('select') ? 'text-red-800' :
              'text-green-800'
            }`}>
              {message}
            </span>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Patient Information Card */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
          {/* Card Header */}
          <div className="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-4">
            <h2 className="text-xl font-bold text-white flex items-center">
              <svg className="w-6 h-6 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Patient Information
            </h2>
            <p className="text-blue-200 text-sm mt-1">Enter patient demographics and clinical details</p>
          </div>

          {/* Card Body */}
          <div className="px-6 py-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Patient ID */}
              <div className="md:col-span-2">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Patient ID <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="patient_id"
                  value={patientInfo.patient_id}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-blue-900 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="e.g., PAT-2024-001"
                  required
                />
              </div>

              {/* Patient Name */}
              <div className="md:col-span-2">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Patient Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="patient_name"
                  value={patientInfo.patient_name}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-blue-900 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="Enter full name"
                  required
                />
              </div>

              {/* Age */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Age <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="age"
                  value={patientInfo.age}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-blue-900 transition-all duration-200 text-gray-800 placeholder-gray-400"
                  placeholder="Enter age"
                  min="0"
                  max="150"
                  required
                />
              </div>

              {/* Gender */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Gender <span className="text-red-500">*</span>
                </label>
                <select
                  name="gender"
                  value={patientInfo.gender}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-blue-900 transition-all duration-200 text-gray-800 bg-white"
                  required
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              {/* Image Type */}
              <div className="md:col-span-2">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Imaging Modality <span className="text-red-500">*</span>
                </label>
                <select
                  name="image_type"
                  value={patientInfo.image_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-900 focus:border-blue-900 transition-all duration-200 text-gray-800 bg-white"
                  required
                >
                  <option value="X-Ray">X-Ray (Radiography)</option>
                  <option value="CT">CT Scan (Computed Tomography)</option>
                  <option value="MRI">MRI (Magnetic Resonance Imaging)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Diagnostic Image Upload Card */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
          {/* Card Header */}
          <div className="bg-gradient-to-r from-teal-700 to-teal-600 px-6 py-4">
            <h2 className="text-xl font-bold text-white flex items-center">
              <svg className="w-6 h-6 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Diagnostic Image Upload
            </h2>
            <p className="text-teal-100 text-sm mt-1">Upload medical imaging file for analysis</p>
          </div>

          {/* Card Body */}
          <div className="px-6 py-6">
            {/* Drag and Drop Zone */}
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`relative border-3 border-dashed rounded-xl p-10 text-center transition-all duration-300 ${
                dragActive
                  ? 'border-teal-600 bg-teal-50'
                  : 'border-gray-300 bg-gray-50 hover:border-teal-500 hover:bg-teal-25'
              }`}
            >
              <input
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                id="file-upload"
                required
              />
              
              <div className="flex flex-col items-center">
                {selectedImage ? (
                  <>
                    <svg className="w-16 h-16 text-green-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p className="text-lg font-semibold text-gray-800 mb-2">{selectedImage.name}</p>
                    <p className="text-sm text-gray-500 mb-4">
                      {(selectedImage.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    <label 
                      htmlFor="file-upload"
                      className="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors cursor-pointer font-medium"
                    >
                      Change File
                    </label>
                  </>
                ) : (
                  <>
                    <svg className="w-16 h-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-lg font-semibold text-gray-800 mb-2">
                      Drag & Drop your image here
                    </p>
                    <p className="text-sm text-gray-500 mb-4">
                      or click to browse files
                    </p>
                    <label 
                      htmlFor="file-upload"
                      className="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors cursor-pointer font-medium"
                    >
                      Select File
                    </label>
                    <p className="text-xs text-gray-400 mt-4">
                      Supported formats: JPG, PNG, DICOM • Max size: 10MB
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={uploading || !isFormValid()}
            className={`px-8 py-4 rounded-xl font-bold text-lg shadow-lg transition-all duration-300 flex items-center ${
              uploading || !isFormValid()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-900 to-blue-800 text-white hover:from-blue-800 hover:to-blue-700 hover:shadow-xl transform hover:-translate-y-0.5'
            }`}
          >
            {uploading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing Image...
              </>
            ) : (
              <>
                <svg className="w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Analyze Image & Proceed
              </>
            )}
          </button>
        </div>
      </form>

      {/* Info Footer */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start">
          <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div>
            <h4 className="text-sm font-semibold text-blue-900 mb-1">What happens next?</h4>
            <p className="text-sm text-blue-800">
              After clicking "Analyze Image & Proceed", our AI will process the diagnostic image and extract relevant findings. 
              You'll then proceed to Step 2 to add laboratory results, followed by report generation and review.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

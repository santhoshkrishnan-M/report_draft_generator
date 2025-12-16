import React, { useState } from 'react'
import axios from 'axios'

function Dashboard({ onImageAnalyzed }) {
  const [patientInfo, setPatientInfo] = useState({
    patient_id: '',
    patient_name: '',
    age: '',
    gender: 'M',
    study_date: new Date().toISOString().split('T')[0],
    image_type: 'xray'
  })

  const [selectedImage, setSelectedImage] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setPatientInfo(prev => ({ ...prev, [name]: value }))
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!selectedImage) {
      setMessage('Please select an image')
      return
    }

    setUploading(true)
    setMessage('Analyzing image...')

    try {
      // For demo, we'll use a mock image path
      // In production, you'd upload the file first
      const imagePath = `/tmp/medical_images/${selectedImage.name}`
      
      const response = await axios.post('/medical/analyze-image', {
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
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Diagnostic Data</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Patient Information */}
          <div className="border-b pb-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Patient Information</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Patient ID *
                </label>
                <input
                  type="text"
                  name="patient_id"
                  value={patientInfo.patient_id}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="P12345"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Patient Name *
                </label>
                <input
                  type="text"
                  name="patient_name"
                  value={patientInfo.patient_name}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Age *
                </label>
                <input
                  type="text"
                  name="age"
                  value={patientInfo.age}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                  placeholder="45"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Gender *
                </label>
                <select
                  name="gender"
                  value={patientInfo.gender}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                >
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Study Date *
                </label>
                <input
                  type="date"
                  name="study_date"
                  value={patientInfo.study_date}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Image Type *
                </label>
                <select
                  name="image_type"
                  value={patientInfo.image_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                >
                  <option value="xray">X-Ray</option>
                  <option value="mri">MRI</option>
                  <option value="ct">CT Scan</option>
                </select>
              </div>
            </div>
          </div>

          {/* Image Upload */}
          <div>
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Diagnostic Image</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-medical-blue transition">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                className="hidden"
                id="image-upload"
              />
              <label htmlFor="image-upload" className="cursor-pointer">
                {selectedImage ? (
                  <div>
                    <p className="text-green-600 font-medium">✓ {selectedImage.name}</p>
                    <p className="text-sm text-gray-500 mt-2">Click to change</p>
                  </div>
                ) : (
                  <div>
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="mt-2 text-sm text-gray-600">
                      <span className="font-medium text-medical-blue">Click to upload</span> diagnostic image
                    </p>
                    <p className="text-xs text-gray-500 mt-1">PNG, JPG, BMP up to 10MB</p>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-between pt-6">
            <button
              type="submit"
              disabled={uploading}
              className="bg-medical-blue text-white px-8 py-3 rounded-md font-medium hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {uploading ? 'Analyzing...' : 'Analyze Image'}
            </button>
            
            {message && (
              <p className={`text-sm ${message.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
                {message}
              </p>
            )}
          </div>
        </form>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-3 gap-4 mt-8">
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <div className="text-3xl font-bold text-medical-blue mb-2">01</div>
          <p className="text-sm text-gray-600">Upload Image</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <div className="text-3xl font-bold text-medical-blue mb-2">02</div>
          <p className="text-sm text-gray-600">Enter Lab Results</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <div className="text-3xl font-bold text-medical-blue mb-2">03</div>
          <p className="text-sm text-gray-600">Review & Approve</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

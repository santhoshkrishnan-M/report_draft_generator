#!/bin/bash

# Medical Report Drafting System - Quick Start Script

echo "================================"
echo "Medical Report Drafting System"
echo "================================"
echo ""

# Check if Python virtual environment exists
if [ ! -d "python_modules" ]; then
    echo "❌ Python virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv python_modules
fi

# Activate virtual environment
echo "📦 Activating Python environment..."
source python_modules/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Python dependencies installed"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo ""
echo "✅ Node.js dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p /tmp/medical_images
mkdir -p /tmp/medical_reports

echo ""
echo "================================"
echo "🚀 Starting Medical Report System"
echo "================================"
echo ""
echo "Services:"
echo "  • Motia Backend & Workbench: http://localhost:3000"
echo "  • Frontend UI: http://localhost:3001"
echo ""
echo "To start the frontend (in another terminal):"
echo "  cd frontend && npm run dev"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start Motia development server
npm run dev

# Medical Report Drafting System - Setup Guide

## Quick Start (Recommended)

```bash
# Run the automated setup script
./start.sh
```

This will:
1. Set up Python virtual environment
2. Install all dependencies
3. Create necessary directories
4. Start the Motia development server

## Manual Setup

### Step 1: Install Python Dependencies

```bash
# Activate virtual environment (if exists)
source python_modules/bin/activate

# Or create new virtual environment
python3 -m venv python_modules
source python_modules/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Node.js Dependencies

```bash
npm install
```

### Step 3: Create Required Directories

```bash
mkdir -p /tmp/medical_images
mkdir -p /tmp/medical_reports
```

### Step 4: Start Backend Server

```bash
npm run dev
```

This starts:
- Motia runtime (API endpoints)
- Motia Workbench (http://localhost:3000)
- All medical workflow steps

### Step 5: Start Frontend (In New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:3001

## Verify Installation

### Test Backend

```bash
# Check Motia Workbench
curl http://localhost:3000

# Check medical endpoints (after Motia starts)
curl http://localhost:3000/medical/report/test-session
```

### Test Frontend

Open browser to: http://localhost:3001

## Configuration

### Python Services

Edit service configurations in:
- `services/image-agent/image_processor.py`
- `services/lab-agent/lab_analyzer.py`
- `services/report-agent/report_generator.py`
- `services/pdf-service/pdf_generator.py`

### Motia Steps

Medical workflow steps are in:
- `src/medical/image_analysis_step.py`
- `src/medical/lab_analysis_step.py`
- `src/medical/report_generation_step.py`
- `src/medical/report_approval_step.py`
- `src/medical/get_report_step.py`

### Frontend Configuration

Edit frontend configuration in:
- `frontend/src/App.jsx` - Main app logic
- `frontend/src/components/` - UI components
- `tailwind.config.js` - Styling
- `vite.config.js` - Dev server & proxy

## Troubleshooting

### Python Import Errors

```bash
# Make sure virtual environment is activated
source python_modules/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### OpenCV Installation Issues

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-opencv libopencv-dev

# Or install via pip
pip install opencv-python opencv-python-headless
```

### Motia Step Not Found

```bash
# Regenerate types
npm run generate-types

# Clean and restart
npm run clean
npm install
npm run dev
```

### Frontend Not Connecting to Backend

Check `vite.config.js` proxy configuration:

```javascript
proxy: {
  '/medical': {
    target: 'http://localhost:3000',
    changeOrigin: true,
  }
}
```

### Port Already in Use

```bash
# Change Motia port (in motia.config.ts if needed)
# Change frontend port (in vite.config.js)

server: {
  port: 3001, // Change this
}
```

## Development Workflow

### Adding New Medical Tests

Edit `services/lab-agent/lab_analyzer.py` and add to `REFERENCE_RANGES`:

```python
'test_name': ReferenceRange('Display Name', min_val, max_val, crit_low, crit_high, 'unit')
```

### Modifying Report Template

Edit `services/report-agent/report_generator.py` methods:
- `generate_imaging_findings()`
- `generate_laboratory_findings()`
- `generate_interpretive_notes()`
- `generate_recommendations()`

### Customizing PDF Layout

Edit `services/pdf-service/pdf_generator.py`:
- `_setup_custom_styles()` - Text styles
- `_create_header()` - Page header
- `_create_footer()` - Page footer
- `generate_pdf()` - Document structure

### Adding UI Components

Create new components in `frontend/src/components/`

### Modifying Workflow Steps

Edit Motia steps in `src/medical/`:
- Update `config` object for API changes
- Modify `handler` function for logic changes

## Testing

### Unit Tests (Example)

```python
# Test lab analyzer
cd services/lab-agent
python3 lab_analyzer.py

# Test image processor
cd services/image-agent
python3 image_processor.py

# Test report generator
cd services/report-agent
python3 report_generator.py
```

### API Tests

Use demo data in `demo-data/` directory:

```bash
# See demo-data/README.md for API examples
cat demo-data/README.md
```

### End-to-End Test

1. Open UI: http://localhost:3001
2. Fill patient info
3. Upload test image
4. Enter lab results
5. Generate report
6. Review and approve
7. Download PDF

## Production Deployment

### Environment Variables

Create `.env` file:

```bash
NODE_ENV=production
MOTIA_PORT=3000
FRONTEND_PORT=3001
PYTHON_ENV_PATH=/path/to/python_modules
```

### Build for Production

```bash
# Build Motia backend
npm run build

# Build frontend
cd frontend
npm run build

# Start production server
npm run start
```

### Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM node:18
FROM python:3.9

# Copy project files
COPY . /app
WORKDIR /app

# Install dependencies
RUN npm install
RUN pip install -r requirements.txt

# Build
RUN npm run build

# Expose ports
EXPOSE 3000 3001

# Start services
CMD ["npm", "run", "start"]
```

## Security Considerations

### For Production Use

1. **Authentication**: Add user authentication
2. **Authorization**: Implement role-based access
3. **HTTPS**: Use SSL/TLS certificates
4. **Data Encryption**: Encrypt patient data at rest
5. **Audit Logging**: Log all report access/modifications
6. **HIPAA Compliance**: Ensure healthcare data compliance
7. **Input Validation**: Validate all user inputs
8. **Rate Limiting**: Add API rate limiting
9. **Backup**: Regular data backups
10. **Monitoring**: Set up health checks and monitoring

## Performance Optimization

### Backend

- Use Redis for state caching
- Implement database instead of in-memory state
- Add request queuing for heavy processing

### Frontend

- Lazy load components
- Implement pagination for large datasets
- Add loading states and skeletons
- Use React.memo for expensive components

### Image Processing

- Implement image compression
- Use worker threads for parallel processing
- Cache processed images

## Support & Resources

- **Motia Documentation**: https://motia.dev/docs
- **OpenCV Documentation**: https://docs.opencv.org/
- **ReportLab Documentation**: https://www.reportlab.com/docs/
- **React Documentation**: https://react.dev/

## License & Compliance

⚠️ **IMPORTANT**: This system is for demonstration/educational purposes.

For production medical use:
- Obtain necessary medical software certifications
- Ensure HIPAA/GDPR compliance
- Implement proper security measures
- Get medical professional review
- Follow local healthcare regulations

---

**Version**: 1.0.0  
**Last Updated**: December 16, 2025

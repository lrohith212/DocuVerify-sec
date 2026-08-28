# 🚀 DocuVerify-Sec Quick Start Guide

Get DocuVerify-Sec running in 5 minutes.

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation & Launch

### Option 1: Automatic Setup (Recommended)

**On Linux/macOS:**
```bash
# Clone/create project directory
mkdir docuverify-sec && cd docuverify-sec

# Copy all project files into this directory
# (requirements.txt, app.py, forensics/, static/)

# Make script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

**On Windows:**
```bash
# Create project directory
mkdir docuverify-sec
cd docuverify-sec

# Copy all project files into this directory
# Run setup script
python setup.py
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create uploads directory
mkdir uploads

# 4. Run server
python app.py
```

## Access the Application

Once running, open your browser:

```
http://localhost:5000
```

You should see:
- ✓ Navigation bar with "DocuVerify-Sec" branding
- ✓ System status indicators (green/pulsing)
- ✓ Upload zone with drag-and-drop
- ✓ Demo buttons

## First Analysis

### Test with a Sample Document

1. **Prepare a test file**: PDF, PNG, or JPG (under 50MB)
2. **Upload it**:
   - Drag and drop onto the upload zone, OR
   - Click to select from file browser
3. **Wait for analysis**: Progress bar shows 4 stages
4. **View results**: 
   - Trust score gauge (0-100%)
   - Cyber threat status
   - Visual forensics
   - Metadata inspection
   - Mathematical audit

### Example: Check If PDF Has Malicious Code

1. Upload any PDF file
2. Navigate to **"Cyber Threats"** tab
3. Results will show:
   - ✓ Clean (no threats found) OR
   - ⚠ Medium (editing history detected) OR
   - ✗ Critical (malicious code detected)

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the Flask server.

## Common Commands

```bash
# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Run server
python app.py

# Run with production settings
FLASK_ENV=production python app.py

# Test API endpoint
curl http://localhost:5000/health

# Deactivate environment
deactivate
```

## Verify Installation

Check that all components are working:

```bash
# Health check
curl http://localhost:5000/health

# Expected response:
# {
#   "status": "operational",
#   "services": {
#     "cyber_scanner": "active",
#     "visual_forensics": "active",
#     "metadata_inspector": "active",
#     "semantic_audit": "active"
#   }
# }
```

## Troubleshooting

### Port 5000 Already in Use
```bash
# Use different port
python -c "from app import app; app.run(port=8000)"
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify Flask is installed
python -c "import flask; print(flask.__version__)"
```

### Import Errors (forensics module)
```bash
# Ensure forensics/__init__.py exists
ls -la forensics/

# If missing, create it:
touch forensics/__init__.py
```

### Tesseract Not Found
The app will automatically fall back to EasyOCR - no action needed!

If you want Tesseract:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

## Next Steps

1. **Read Full Documentation**: See `README.md` for complete feature guide
2. **Explore API**: Check API endpoints section in README
3. **Customize Scoring**: Edit `calculate_trust_score()` in `app.py`
4. **Deploy**: See deployment guide in README for production setup

## File Structure Checklist

Verify you have all files:

```
docuverify-sec/
├── app.py                    ✓
├── requirements.txt          ✓
├── QUICKSTART.md            ✓
├── README.md                ✓
├── forensics/
│   ├── __init__.py          ✓
│   ├── cyber_scanner.py     ✓
│   ├── visual_ela.py        ✓
│   ├── metadata_inspector.py ✓
│   └── semantic_audit.py    ✓
├── static/
│   └── index.html           ✓
└── uploads/                 ✓ (create with `mkdir uploads`)
```

## Getting Help

**Issue**: 404 on http://localhost:5000
- Solution: Ensure Flask is running and showing "Running on http://127.0.0.1:5000"

**Issue**: File upload fails
- Check file format (PDF, PNG, JPG only)
- Check file size (max 50MB)
- Check uploads/ directory exists and is writable

**Issue**: Analysis doesn't complete
- Check browser console for JavaScript errors
- Check Flask terminal for error messages
- Try with a smaller file first

## Advanced: Run with Production Server

For production deployment, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Environment Variables

Create `.env` file for custom configuration:

```
FLASK_ENV=production
DEBUG=False
MAX_FILE_SIZE=52428800
UPLOAD_FOLDER=uploads
```

## What's Next?

✨ Your DocuVerify-Sec instance is ready!

- Upload documents to verify authenticity
- Export analysis results as JSON
- Integrate with your security workflow
- Check README.md for advanced features

---

**Need help?** Check the troubleshooting section or review README.md for detailed documentation.

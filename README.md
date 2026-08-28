# DocuVerify-Sec: Intelligent Document Authenticity & Cyber-Forensic Engine

A production-ready, full-stack web application for comprehensive document forensic analysis, combining cyber threat detection, visual tampering analysis, metadata inspection, and mathematical auditing.

## 🎯 Features

### 1. **Cyber Threat Detection**
- Scans PDFs for embedded malicious JavaScript, launch actions, and suspicious payloads
- Detects macro execution, embedded files, URI handlers, and auto-action triggers
- Analyzes PDF stream objects for shell execution patterns
- Identifies incremental update tampering
- Returns detailed threat reports with severity levels (LOW/MEDIUM/CRITICAL)

### 2. **Visual & Pixel Forensics**
- **Error Level Analysis (ELA)**: Re-compresses images at quality 90 and calculates pixel-level differences
- **Contour Detection**: Automatically identifies high-variance regions indicating splicing or editing
- **Tampering Confidence Scoring**: Quantifies likelihood of visual manipulation
- Generates heat maps showing suspicious areas with red bounding boxes
- Supports PDF-to-image rendering at 300 DPI for high-resolution analysis

### 3. **Metadata & Editing History**
- Extracts EXIF data from images and XMP metadata from PDFs
- Detects editing software signatures (Photoshop, GIMP, Canva, PDFescape, Illustrator, etc.)
- Flags suspicious metadata patterns and date mismatches
- Provides editing history timeline

### 4. **Semantic & Mathematical Auditing**
- Extracts text via OCR (Tesseract with EasyOCR fallback)
- Identifies monetary values (Subtotal, Tax, Total, Discounts)
- Validates academic scores and marks
- Detects mathematical inconsistencies (e.g., Subtotal + Tax ≠ Total)
- Percentage validation and cross-checks

### 5. **Composite Trust Score (0-100%)**
- **85-100%**: ✓ VERIFIED AUTHENTIC (Green) - Document appears legitimate
- **50-84%**: ⚠ SUSPICIOUS / REQUIRES REVIEW (Yellow) - Manual inspection recommended
- **0-49%**: ✗ TAMPERED / MALICIOUS (Red) - Critical issues detected

**Scoring Logic:**
- Start: 100 points
- Deduct 40 for critical cyber payloads
- Deduct 30 for high-confidence visual tampering
- Deduct 15 for editing software detected
- Deduct 15 for mathematical inconsistencies

### 6. **Executive Summary**
- Plain-language explanations of all findings
- Risk assessments tailored for non-technical audiences
- Actionable recommendations

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0 with CORS enabled
- **Computer Vision**: OpenCV, PIL/Pillow
- **PDF Processing**: PyMuPDF, PyPDF2, pdfplumber
- **OCR**: Tesseract (pytesseract) with EasyOCR fallback
- **Processing**: NumPy, SciPy

### Frontend
- **HTML5** with semantic markup
- **CSS3** with custom dark cybersecurity theme (slate/zinc + neon cyan/green/red)
- **Vanilla JavaScript** with modern ES6+ features
- **Icons**: Font Awesome 6
- **Charts**: Custom SVG-based gauge visualization

### Infrastructure
- **File Storage**: Local uploads directory
- **Max File Size**: 50 MB
- **CORS**: Fully enabled for cross-origin requests

---

## 📝 Future Enhancements

- [ ] PDF report generation with charts
- [ ] Blockchain-based document validation
- [ ] Machine learning model for tampering detection
- [ ] Multi-language OCR support
- [ ] Real-time collaborative analysis
- [ ] Integration with threat intelligence feeds
- [ ] WebRTC for secure document transmission
- [ ] Custom threat rules engine
- [ ] Historical comparison database
- [ ] Mobile app (React Native)

---
## 📁 Project Structure

```
docuverify-sec/
├── app.py                          # Main Flask backend
├── requirements.txt                # Python dependencies
├── forensics/
│   ├── __init__.py
│   ├── cyber_scanner.py           # Malicious PDF detection
│   ├── visual_ela.py              # Error Level Analysis & contours
│   ├── metadata_inspector.py      # EXIF/XMP extraction
│   └── semantic_audit.py          # OCR & math validation
├── static/
│   └── index.html                 # Complete frontend (HTML+CSS+JS)
├── uploads/                       # Directory for uploaded files
└── README.md                      # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Tesseract OCR (optional, with automatic fallback to EasyOCR)

### Step 1: Clone/Create Project Directory
```bash
mkdir docuverify-sec
cd docuverify-sec
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Tesseract OCR (Optional)
**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS (Homebrew):**
```bash
brew install tesseract
```

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki

*Note: If Tesseract is not installed, the application will automatically fall back to EasyOCR.*

### Step 5: Create Uploads Directory
```bash
mkdir -p uploads
```

### Step 6: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

---

## 🔌 API Endpoints

### `POST /api/analyze`
**Comprehensive document forensic analysis**

**Request:**
```bash
curl -X POST -F "file=@document.pdf" http://localhost:5000/api/analyze
```

**Response:**
```json
{
  "file_name": "document.pdf",
  "file_size": 125000,
  "analysis_timestamp": "2024-01-15T10:30:00.000000",
  "trust_score": {
    "score": 85,
    "category": "VERIFIED AUTHENTIC",
    "color": "green",
    "deductions": [
      {"reason": "Edited with Photoshop", "deduction": 8}
    ]
  },
  "analyses": {
    "cyber_threats": {...},
    "visual_forensics": {...},
    "metadata": {...},
    "semantic_audit": {...}
  },
  "executive_summary": [...],
  "file_paths": {...}
}
```

### `GET /health`
**System status check**

```bash
curl http://localhost:5000/health
```

### `GET /api/demo-samples`
**List available demo documents**

```bash
curl http://localhost:5000/api/demo-samples
```

### `GET /uploads/<filename>`
**Retrieve uploaded or generated files**

```bash
curl http://localhost:5000/uploads/original_rendered.png
```

---

## 🖥️ Frontend Usage

### Upload & Analyze
1. Navigate to `http://localhost:5000` (or static file server)
2. Drag-and-drop a PDF, PNG, or JPG file
3. Wait for analysis to complete (~5-15 seconds depending on file size)
4. View comprehensive forensic results

### Results Dashboard

#### **Trust Score Gauge**
- Large animated SVG gauge showing 0-100% authenticity
- Color-coded category badge
- Status indicators for cyber and visual threats

#### **Executive Summary**
- Plain-language findings
- Risk flags with icons
- Actionable recommendations

#### **Tabbed Results**

1. **Visual Comparison Tab**
   - Side-by-side original vs. ELA heatmap
   - Bounding boxes highlighting suspicious regions
   - Tampering confidence percentages

2. **Cyber Threats Tab**
   - List of detected malicious payloads
   - Severity levels and descriptions
   - Technical details and byte offsets

3. **Metadata Tab**
   - Software used for editing
   - Creation and modification dates
   - Suspicious keyword flags

4. **Mathematical Audit Tab**
   - Extracted numerical values
   - Inconsistency reports
   - Calculation validation results

### Export Options
- **PDF Report**: Download complete forensic analysis as PDF (future enhancement)
- **JSON Report**: Full structured data export for integration

---

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the project root:

```bash
FLASK_ENV=development
DEBUG=True
MAX_FILE_SIZE=52428800  # 50MB in bytes
UPLOAD_FOLDER=uploads
```

### Tesseract Configuration
If Tesseract is installed at a non-standard location, configure in `semantic_audit.py`:

```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = '/path/to/tesseract'
```

---

## 📊 Understanding Results

### Trust Score Components

| Factor | Max Deduction | Triggers |
|--------|---------------|----------|
| Cyber Threats | 40 pts | JS, Launch, Exploit Detected |
| Visual Tampering | 30 pts | High ELA variance, splicing |
| Editing Software | 15 pts | Photoshop, GIMP, etc. |
| Math Inconsistencies | 15 pts | Subtotal ≠ Total, invalid scores |

### ELA Heatmap Interpretation
- **Blue/Cool colors**: Normal compression artifacts (legitimate)
- **Red/Hot colors**: High compression differences (potential tampering)
- **Bounding boxes**: Flagged regions of interest

### Threat Severity Levels
- **CRITICAL**: Immediate action required (malicious code, exploit payload)
- **MEDIUM**: Manual review recommended (editing history, date anomalies)
- **LOW**: Informational (document properties, metadata)

---

## ⚙️ Advanced Usage

### Batch Processing
To analyze multiple documents:

```python
import os
import requests

upload_dir = 'documents/'
for filename in os.listdir(upload_dir):
    with open(os.path.join(upload_dir, filename), 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/api/analyze', files=files)
        results = response.json()
        print(f"{filename}: Score {results['trust_score']['score']}")
```

### Integration with External Systems
The JSON response from `/api/analyze` can be integrated with:
- SIEM systems for threat monitoring
- Document management systems for automated flagging
- Compliance auditing platforms
- Risk assessment workflows

### Custom Scoring
Modify scoring logic in `app.py`, function `calculate_trust_score()`:

```python
def calculate_trust_score(cyber_result, visual_result, metadata_result, semantic_result):
    score = 100
    # Customize deduction logic here
    return score
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Tesseract Not Found**
- Install Tesseract or let EasyOCR handle OCR automatically
- Add to system PATH if installed manually

**2. File Too Large**
- Default limit is 50MB
- Increase `MAX_FILE_SIZE` in `app.py` config

**3. PDF Rendering Fails**
- Ensure PyMuPDF is properly installed: `pip install --upgrade PyMuPDF`
- Some encrypted PDFs may not render

**4. CORS Errors**
- CORS is enabled for all origins by default
- Modify in `app.py` if needed:
  ```python
  CORS(app, resources={r"/api/*": {"origins": ["https://example.com"]}})
  ```

**5. OCR Not Extracting Text**
- Some scanned PDFs may require preprocessing
- Ensure image contrast is adequate
- Try EasyOCR if Tesseract fails

---

## 🔒 Security Considerations

- **File Upload Validation**: Only PDF, PNG, JPG allowed
- **Filename Sanitization**: Uses `secure_filename()` to prevent path traversal
- **File Size Limits**: Max 50MB to prevent DoS
- **No Code Execution**: Forensic analysis only, no file execution
- **Sandboxed Analysis**: Each file analyzed in isolated process
- **CORS Configuration**: Customizable for your domain

### Deployment Security
- Run behind HTTPS in production
- Use environment variables for sensitive config
- Implement rate limiting on `/api/analyze`
- Add authentication layer for sensitive documents
- Regular security audits of dependencies

---

## 📈 Performance Optimization

### Processing Times (Approximate)
- Small PDFs (<1MB): 3-5 seconds
- Large PDFs (10-50MB): 10-30 seconds
- High-resolution images: 5-10 seconds

### Optimization Tips
1. **Async Processing**: For high volume, implement Celery/Redis for background jobs
2. **Caching**: Cache OCR results if analyzing identical files
3. **GPU Acceleration**: Enable CUDA for EasyOCR if available
4. **Lazy Loading**: Load images on-demand in frontend



## 📄 License

This project is provided as-is for educational and forensic analysis purposes.

---




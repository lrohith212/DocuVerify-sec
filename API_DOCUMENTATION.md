# DocuVerify-Sec API Documentation

Complete API reference with examples, authentication, error handling, and integration guides.

---

## Base URL

```
http://localhost:5000
```

For production, replace with your domain:
```
https://docuverify-sec.example.com
```

---

## Authentication

Currently, the API is open (no authentication required). For production deployment, implement:

```python
# In app.py, add authentication middleware
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.environ.get('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/analyze', methods=['POST'])
@require_api_key
def analyze_document():
    # ... implementation
```

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check system status and service availability

**Request**:
```bash
curl -X GET http://localhost:5000/health
```

**Response** (200 OK):
```json
{
  "status": "operational",
  "timestamp": "2024-01-15T10:30:45.123456",
  "services": {
    "cyber_scanner": "active",
    "visual_forensics": "active",
    "metadata_inspector": "active",
    "semantic_audit": "active"
  }
}
```

**Use Case**: Monitor system health before bulk operations

---

### 2. Analyze Document (Main Endpoint)

**Endpoint**: `POST /api/analyze`

**Description**: Comprehensive forensic analysis of uploaded document

**Request Headers**:
```
Content-Type: multipart/form-data
```

**Request Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | file | Yes | Document file (PDF, PNG, JPG) |

**Supported Formats**:
- `.pdf` - PDF documents
- `.png` - PNG images
- `.jpg`, `.jpeg` - JPEG images

**File Size Limits**:
- Maximum: 50 MB
- Recommended: < 10 MB for faster processing

**Request Examples**:

**Python (requests library)**:
```python
import requests

with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:5000/api/analyze',
        files=files,
        timeout=60
    )

result = response.json()
print(f"Trust Score: {result['trust_score']['score']}%")
print(f"Category: {result['trust_score']['category']}")
```

**cURL**:
```bash
curl -X POST -F "file=@document.pdf" \
  http://localhost:5000/api/analyze
```

**JavaScript (Fetch API)**:
```javascript
const formData = new FormData();
const fileInput = document.getElementById('fileInput');
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5000/api/analyze', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Trust Score: ${result.trust_score.score}%`);
```

**Response** (200 OK):
```json
{
  "file_name": "document.pdf",
  "file_size": 125480,
  "analysis_timestamp": "2024-01-15T10:35:20.456789",
  "trust_score": {
    "score": 78,
    "category": {
      "category": "SUSPICIOUS / REQUIRES REVIEW",
      "color": "yellow",
      "risk_level": "MEDIUM"
    },
    "deductions": [
      {
        "reason": "Edited with Photoshop",
        "deduction": 8
      },
      {
        "reason": "Date anomaly detected",
        "deduction": 7
      },
      {
        "reason": "Potential tampering regions detected",
        "deduction": 7
      }
    ]
  },
  "analyses": {
    "cyber_threats": {
      "is_clean": true,
      "threat_level": "LOW",
      "threats_detected": [],
      "file_hash": "a1b2c3d4e5f6...",
      "scan_timestamp": "2024-01-15T10:35:20.456789"
    },
    "visual_forensics": {
      "success": true,
      "original_image_path": "uploads/original_rendered.png",
      "ela_heatmap_path": "uploads/ela_heatmap.png",
      "bounding_boxes": [
        {
          "x": 150,
          "y": 200,
          "w": 100,
          "h": 80,
          "confidence": 65.2,
          "area_percentage": 2.5
        }
      ],
      "tampering_detected": true,
      "tampering_confidence": 65.2,
      "high_variance_regions": 3
    },
    "metadata": {
      "metadata": {
        "Creator": "Adobe Photoshop 2024",
        "Producer": "Adobe PDF Library 16.0",
        "CreationDate": "2024-01-10T08:00:00Z",
        "ModDate": "2024-01-15T09:30:00Z"
      },
      "software_detected": ["Photoshop"],
      "creation_date": "2024-01-10T08:00:00Z",
      "modification_date": "2024-01-15T09:30:00Z",
      "suspicious_patterns": [
        {
          "type": "Date Anomaly",
          "severity": "MEDIUM",
          "description": "Creation and modification dates differ by 5 days",
          "details": "Created: 2024-01-10T08:00:00Z, Modified: 2024-01-15T09:30:00Z"
        }
      ],
      "metadata_risk_level": "MEDIUM",
      "editing_history": "Edited by: Photoshop"
    },
    "semantic_audit": {
      "success": true,
      "extracted_text": "Invoice #12345\nDate: 2024-01-10\n...",
      "text_length": 2341,
      "numerical_values": {
        "monetary_values": [100.50, 15.75, 116.25],
        "academic_values": [],
        "general_values": [12345, 2024, 1, 10]
      },
      "inconsistencies": [],
      "inconsistency_count": 0,
      "confidence_score": 92.3,
      "audit_status": "PASSED"
    }
  },
  "executive_summary": [
    "✓ Cyber Security: No malicious payloads detected.",
    "⚠️ Visual Forensics: 3 high-variance regions detected with 65.2% confidence. Document shows signs of pixel manipulation or splicing.",
    "ℹ️ Metadata: Document edited with Photoshop. Check creation vs. modification dates for authenticity.",
    "✓ Mathematical Audit: All numerical calculations appear consistent."
  ],
  "file_paths": {
    "uploaded_file": "/uploads/a1b2c3d4-e5f6-7890-abcd-ef1234567890_document.pdf",
    "original_image": "/uploads/original_rendered.png",
    "ela_heatmap": "/uploads/ela_heatmap.png"
  }
}
```

**Error Responses**:

**400 Bad Request** - Invalid file or missing parameter:
```json
{
  "error": "File type not allowed. Use PDF, PNG, or JPG"
}
```

**413 Payload Too Large** - File exceeds size limit:
```json
{
  "error": "File too large. Maximum size is 50MB"
}
```

**500 Internal Server Error** - Server error:
```json
{
  "error": "Server error: [error description]"
}
```

---

### 3. Get Demo Samples

**Endpoint**: `GET /api/demo-samples`

**Description**: List available demo documents for testing

**Request**:
```bash
curl -X GET http://localhost:5000/api/demo-samples
```

**Response** (200 OK):
```json
{
  "samples": [
    {
      "id": "clean_certificate",
      "name": "Clean Certificate",
      "description": "Authentic document with no tampering",
      "type": "pdf",
      "expected_score": 95
    },
    {
      "id": "forged_invoice",
      "name": "Forged Invoice",
      "description": "Doctored invoice with spliced amount",
      "type": "pdf",
      "expected_score": 35
    },
    {
      "id": "weaponized_pdf",
      "name": "Weaponized PDF",
      "description": "PDF with embedded JavaScript payload",
      "type": "pdf",
      "expected_score": 15
    }
  ]
}
```

---

### 4. Download File

**Endpoint**: `GET /uploads/<filename>`

**Description**: Retrieve uploaded or generated forensic files

**Request**:
```bash
curl -o output.png http://localhost:5000/uploads/original_rendered.png
curl -o heatmap.png http://localhost:5000/uploads/ela_heatmap.png
```

**Response**: File content (binary or image data)

**Error** (404):
```json
{
  "error": "File not found"
}
```

---

## Response Data Structure

### Trust Score Object

```json
{
  "score": 85,
  "deductions": [
    {
      "reason": "Reason for deduction",
      "deduction": 15
    }
  ],
  "category": {
    "category": "VERIFIED AUTHENTIC",
    "color": "green",
    "risk_level": "LOW"
  }
}
```

**Score Interpretation**:
- **85-100 (Green)**: VERIFIED AUTHENTIC - Safe to proceed
- **50-84 (Yellow)**: SUSPICIOUS - Manual review recommended
- **0-49 (Red)**: TAMPERED - Critical issues detected

### Cyber Threats Object

```json
{
  "is_clean": boolean,
  "threat_level": "LOW" | "MEDIUM" | "CRITICAL",
  "threats_detected": [
    {
      "type": "Threat Type",
      "severity": "LOW" | "MEDIUM" | "CRITICAL",
      "description": "Human-readable description",
      "location": "Where in file",
      "context": "Surrounding code/data"
    }
  ],
  "file_hash": "SHA-256 hash"
}
```

### Visual Forensics Object

```json
{
  "success": boolean,
  "original_image_path": "/uploads/...",
  "ela_heatmap_path": "/uploads/...",
  "tampering_detected": boolean,
  "tampering_confidence": 0-100,
  "high_variance_regions": number,
  "bounding_boxes": [
    {
      "x": pixel_x,
      "y": pixel_y,
      "w": width,
      "h": height,
      "confidence": 0-100,
      "area_percentage": 0-100
    }
  ]
}
```

### Metadata Object

```json
{
  "metadata": { /* key-value pairs */ },
  "software_detected": ["software1", "software2"],
  "creation_date": "ISO8601 timestamp",
  "modification_date": "ISO8601 timestamp",
  "suspicious_patterns": [
    {
      "type": "Pattern Type",
      "severity": "LOW" | "MEDIUM" | "CRITICAL",
      "description": "Description",
      "details": "Additional details"
    }
  ],
  "metadata_risk_level": "LOW" | "MEDIUM" | "HIGH"
}
```

### Semantic Audit Object

```json
{
  "success": boolean,
  "extracted_text": "Full extracted text",
  "text_length": number,
  "numerical_values": {
    "monetary_values": [100.50, 15.75],
    "academic_values": [80, 95],
    "general_values": [12345, 2024]
  },
  "inconsistencies": [
    {
      "type": "Inconsistency Type",
      "severity": "HIGH",
      "description": "What doesn't match",
      "expected": "Expected value",
      "actual": "Actual value"
    }
  ],
  "inconsistency_count": number,
  "confidence_score": 0-100,
  "audit_status": "PASSED" | "FLAGGED"
}
```

---

## Error Handling

### Common Error Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid file type or missing parameter |
| 404 | Not Found | Requested file doesn't exist |
| 413 | Payload Too Large | File exceeds 50MB limit |
| 500 | Server Error | Unexpected server error |
| 503 | Service Unavailable | Server temporarily down |

### Error Response Format

```json
{
  "error": "Human-readable error message"
}
```

### Retry Strategy

```python
import time
import requests

def call_api_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                'http://localhost:5000/api/analyze',
                files={'file': open('document.pdf', 'rb')},
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                print(f"Service temporarily unavailable, retrying...")
                time.sleep(5)
                continue
            else:
                raise Exception(f"API error: {response.status_code}")
                
        except requests.Timeout:
            print(f"Request timeout, retrying...")
            time.sleep(5)
    
    raise Exception("Max retries exceeded")
```

---

## Integration Examples

### 1. Batch Processing Multiple Documents

```python
import os
import json
import requests
from pathlib import Path

def batch_analyze_documents(directory):
    """Analyze all documents in a directory"""
    
    results = []
    
    for filepath in Path(directory).glob('*.pdf'):
        print(f"Analyzing {filepath.name}...")
        
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                'http://localhost:5000/api/analyze',
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            analysis = response.json()
            results.append({
                'filename': filepath.name,
                'trust_score': analysis['trust_score']['score'],
                'category': analysis['trust_score']['category']['category'],
                'threats': len(analysis['analyses']['cyber_threats']['threats_detected'])
            })
            
            print(f"  Score: {analysis['trust_score']['score']}%")
        else:
            print(f"  Error: {response.status_code}")
    
    return results

# Usage
results = batch_analyze_documents('./documents')
print(json.dumps(results, indent=2))
```

### 2. Conditional Workflow Based on Score

```python
def process_document_based_on_score(filepath):
    """Different handling based on authenticity score"""
    
    with open(filepath, 'rb') as f:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            files={'file': f}
        )
    
    result = response.json()
    score = result['trust_score']['score']
    
    if score >= 85:
        # Automatically approve high-confidence authentic documents
        approve_document(filepath)
        send_email("Document approved", filepath)
        
    elif score >= 50:
        # Flag for manual review
        flag_for_review(filepath, result)
        send_email("Manual review required", filepath, result)
        
    else:
        # Reject potentially malicious documents
        reject_document(filepath)
        send_email("Document rejected", filepath, result)
        quarantine_file(filepath)
```

### 3. Integration with Document Management System

```python
class DocumentSecurityProcessor:
    """Integrate DocuVerify with your DMS"""
    
    def __init__(self, api_endpoint='http://localhost:5000'):
        self.api_endpoint = api_endpoint
    
    def analyze_and_store(self, document_id, filepath):
        """Analyze document and store results in DB"""
        
        # Analyze
        with open(filepath, 'rb') as f:
            response = requests.post(
                f'{self.api_endpoint}/api/analyze',
                files={'file': f}
            )
        
        analysis = response.json()
        
        # Store in database
        db.documents.update_one(
            {'_id': document_id},
            {
                '$set': {
                    'forensics': analysis,
                    'trust_score': analysis['trust_score']['score'],
                    'analyzed_at': datetime.now(),
                    'status': self.determine_status(analysis)
                }
            }
        )
        
        return analysis
    
    def determine_status(self, analysis):
        score = analysis['trust_score']['score']
        if score >= 85:
            return 'verified'
        elif score >= 50:
            return 'review_needed'
        else:
            return 'suspicious'
```

### 4. Real-time Monitoring Dashboard

```javascript
// WebSocket-based dashboard updates
class ForensicMonitor {
    constructor(apiEndpoint = 'http://localhost:5000') {
        this.apiEndpoint = apiEndpoint;
    }
    
    async analyzeAndUpdateDashboard(file, dashboardElement) {
        // Show loading state
        this.showLoading(dashboardElement);
        
        // Analyze
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(
            `${this.apiEndpoint}/api/analyze`,
            { method: 'POST', body: formData }
        );
        
        const result = await response.json();
        
        // Update dashboard
        this.updateScoreGauge(result.trust_score.score, dashboardElement);
        this.updateThreatsList(result.analyses.cyber_threats, dashboardElement);
        this.updateMetadataPanel(result.analyses.metadata, dashboardElement);
        
        // Show notifications
        this.showNotifications(result.executive_summary, dashboardElement);
    }
    
    updateScoreGauge(score, element) {
        const gauge = element.querySelector('.trust-score-gauge');
        gauge.textContent = `${score}%`;
        
        if (score >= 85) {
            gauge.className = 'gauge verified';
        } else if (score >= 50) {
            gauge.className = 'gauge suspicious';
        } else {
            gauge.className = 'gauge malicious';
        }
    }
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, add:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_document():
    # ... implementation
```

---

## Performance Tips

1. **Timeout Settings**: Set appropriate timeouts for large files
   ```python
   timeout = 60  # seconds for large PDFs
   ```

2. **Async Processing**: For high volume, use task queues
   ```python
   from celery import Celery
   ```

3. **Caching**: Cache analysis results
   ```python
   from flask_caching import Cache
   ```

4. **Compression**: Compress API responses
   ```python
   from flask_compress import Compress
   ```

---

## Webhook Notifications

Add webhook support for asynchronous result delivery:

```python
import requests

def notify_webhook(webhook_url, analysis_result):
    """Send analysis results to webhook"""
    try:
        requests.post(webhook_url, json=analysis_result, timeout=10)
    except Exception as e:
        print(f"Webhook notification failed: {e}")
```

---

## Support & Debugging

For API issues:

1. **Check Health Endpoint**: `GET /health`
2. **Enable Debug Mode**: Set `DEBUG=True` in Flask
3. **Check Logs**: Review Flask console output
4. **Verify File Format**: Ensure correct file type
5. **Test with cURL**: Use simple curl commands first

---

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- All core forensic features implemented
- Full API with comprehensive documentation

---

## License & Support

Refer to README.md for licensing information and support guidelines.

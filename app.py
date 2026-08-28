import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from forensics import CyberScanner, VisualELA, MetadataInspector, SemanticAudit, AIDetector
import traceback

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_trust_score(cyber_result, visual_result, metadata_result, semantic_result, ai_result):
    score = 100
    deductions = []
    
    # Cyber
    if cyber_result.get('threat_level') == 'CRITICAL':
        score -= 40
        deductions.append({'reason': 'Critical cyber threats detected', 'deduction': 40})
    elif cyber_result.get('threat_level') == 'MEDIUM':
        score -= 15
        deductions.append({'reason': 'Medium cyber threats detected', 'deduction': 15})
        
    # Visual
    if visual_result.get('success'):
        if visual_result.get('tampering_detected'):
            if visual_result.get('tampering_confidence', 0) > 70:
                score -= 30
                deductions.append({'reason': 'High-confidence tampering detected', 'deduction': 30})
            else:
                score -= 15
                deductions.append({'reason': 'Potential tampering regions detected', 'deduction': 15})
                
    # Metadata
    if metadata_result.get('software_detected'):
        if len(metadata_result['software_detected']) > 1:
            score -= 15
            deductions.append({'reason': f'Multiple editors detected: {", ".join(metadata_result["software_detected"])}', 'deduction': 15})
        else:
            score -= 8
            deductions.append({'reason': f'Edited with {metadata_result["software_detected"][0]}', 'deduction': 8})
            
    if metadata_result.get('suspicious_patterns'):
        for pattern in metadata_result['suspicious_patterns']:
            if pattern['severity'] == 'MEDIUM':
                score -= 5
                deductions.append({'reason': pattern['description'], 'deduction': 5})
                
    # Semantic
    if semantic_result.get('success'):
        if semantic_result.get('inconsistency_count', 0) > 0:
            inconsistency_count = semantic_result.get('inconsistency_count', 0)
            deduction = min(15, inconsistency_count * 5)
            score -= deduction
            deductions.append({'reason': f'{inconsistency_count} mathematical inconsistencies found', 'deduction': deduction})

    # AI
    if ai_result and ai_result.get('success') and ai_result.get('is_ai_generated'):
        prob = ai_result.get('overall_ai_probability', 0)
        score -= 25
        deductions.append({'reason': f'AI-generated content detected ({prob:.1f}% confidence)', 'deduction': 25})
        
    score = max(0, score)
    return {
        'score': int(score),
        'deductions': deductions,
        'category': categorize_score(int(score))
    }

def categorize_score(score):
    if score >= 85:
        return {'category': 'VERIFIED AUTHENTIC', 'color': 'green', 'risk_level': 'LOW'}
    elif score >= 50:
        return {'category': 'SUSPICIOUS / REQUIRES REVIEW', 'color': 'yellow', 'risk_level': 'MEDIUM'}
    else:
        return {'category': 'TAMPERED / MALICIOUS', 'color': 'red', 'risk_level': 'HIGH'}

def generate_executive_summary(cyber_result, visual_result, metadata_result, semantic_result, ai_result, trust_score_result):
    summary_points = []
    if cyber_result.get('threats_detected'):
        threat_count = len(cyber_result['threats_detected'])
        threat_types = set([t['type'] for t in cyber_result['threats_detected']])
        summary_points.append(f"⚠️ Cyber Security: {threat_count} threat(s) detected - {', '.join(threat_types)}. Document may contain malicious payloads.")
    else:
        summary_points.append("✓ Cyber Security: No malicious payloads detected.")
        
    if visual_result.get('success'):
        if visual_result.get('tampering_detected'):
            confidence = visual_result.get('tampering_confidence', 0)
            regions = visual_result.get('high_variance_regions', 0)
            summary_points.append(f"⚠️ Visual Forensics: {regions} high-variance regions detected with {confidence:.1f}% confidence. Document shows signs of pixel manipulation or splicing.")
        else:
            summary_points.append("✓ Visual Forensics: No significant tampering evidence detected in pixel analysis.")
            
    if metadata_result.get('software_detected'):
        software = ', '.join(metadata_result['software_detected'])
        summary_points.append(f"ℹ️ Metadata: Document edited with {software}. Check creation vs. modification dates for authenticity.")
        
    if semantic_result.get('success'):
        if semantic_result.get('inconsistency_count', 0) > 0:
            count = semantic_result['inconsistency_count']
            summary_points.append(f"⚠️ Mathematical Audit: {count} inconsistency(ies) found in numerical data. Totals may not match component values.")
        else:
            summary_points.append("✓ Mathematical Audit: All numerical calculations appear consistent.")

    if ai_result and ai_result.get('success') and ai_result.get('is_ai_generated'):
        summary_points.append(f"⚠️ AI Detection: Document contains synthetic AI-generated content ({ai_result.get('overall_ai_probability', 0):.1f}% confidence).")
    else:
        summary_points.append("✓ AI Detection: Content appears organically generated.")
        
    return summary_points

@app.route('/')
def serve_index():
    return send_file('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'cyber_scanner': 'active',
            'visual_forensics': 'active',
            'metadata_inspector': 'active',
            'semantic_audit': 'active',
            'ai_detector': 'active'
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PDF, PNG, or JPG'}), 400
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        results = {
            'file_name': filename,
            'file_size': os.path.getsize(filepath),
            'analysis_timestamp': datetime.now().isoformat(),
            'analyses': {}
        }
        
        try:
            cyber_scanner = CyberScanner(filepath)
            results['analyses']['cyber_threats'] = cyber_scanner.scan()
        except Exception as e:
            results['analyses']['cyber_threats'] = {'error': str(e), 'threat_level': 'UNKNOWN'}
            traceback.print_exc()
        
        try:
            visual_ela = VisualELA(filepath, app.config['UPLOAD_FOLDER'])
            results['analyses']['visual_forensics'] = visual_ela.analyze()
        except Exception as e:
            results['analyses']['visual_forensics'] = {'success': False, 'error': str(e)}
            traceback.print_exc()
        
        try:
            metadata_inspector = MetadataInspector(filepath)
            results['analyses']['metadata'] = metadata_inspector.inspect()
        except Exception as e:
            results['analyses']['metadata'] = {'error': str(e), 'metadata': {}}
            traceback.print_exc()
        
        try:
            semantic_audit = SemanticAudit(filepath, app.config['UPLOAD_FOLDER'])
            results['analyses']['semantic_audit'] = semantic_audit.audit()
        except Exception as e:
            results['analyses']['semantic_audit'] = {'success': False, 'error': str(e)}
            traceback.print_exc()
            
        try:
            ai_detector = AIDetector(filepath, results['analyses'].get('semantic_audit', {}).get('extracted_text', ''))
            results['analyses']['ai_detection'] = ai_detector.scan()
        except Exception as e:
            results['analyses']['ai_detection'] = {'success': False, 'error': str(e)}
            traceback.print_exc()
        
        cyber_result = results['analyses'].get('cyber_threats', {})
        visual_result = results['analyses'].get('visual_forensics', {})
        metadata_result = results['analyses'].get('metadata', {})
        semantic_result = results['analyses'].get('semantic_audit', {})
        ai_result = results['analyses'].get('ai_detection', {})
        
        trust_score_result = calculate_trust_score(cyber_result, visual_result, metadata_result, semantic_result, ai_result)
        results['trust_score'] = trust_score_result
        
        results['executive_summary'] = generate_executive_summary(
            cyber_result, visual_result, metadata_result, semantic_result, ai_result, trust_score_result
        )
        
        results['file_paths'] = {
            'uploaded_file': f'/uploads/{unique_filename}',
            'original_image': visual_result.get('original_image_path', '').replace('\\', '/').replace('uploads/', '/uploads/') if visual_result.get('original_image_path') else None,
            'ela_heatmap': visual_result.get('ela_heatmap_path', '').replace('\\', '/').replace('uploads/', '/uploads/') if visual_result.get('ela_heatmap_path') else None
        }
        
        return jsonify(results), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 50MB'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
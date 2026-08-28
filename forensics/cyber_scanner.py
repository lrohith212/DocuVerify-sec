import hashlib
import re
import os
from typing import Dict, List, Any
import PyPDF2

class CyberScanner:
    """Detects malicious payloads in PDF files: JS, Launch actions, embedded files, etc."""
    
    MALICIOUS_TOKENS = [
        b'/JS', b'/JavaScript', b'/Launch', b'/EmbeddedFiles', 
        b'/OpenAction', b'/AA', b'/URI', b'/SubmitForm', b'/ImportData',
        b'/EmbedFont', b'/ObjStm', b'/ObjStmNum', b'/RichMedia', b'/Flash',
        b'/XFA', b'/AcroForm'
    ]
    
    THREAT_KEYWORDS = {
        '/JS': 'Embedded JavaScript detected',
        '/JavaScript': 'JavaScript code embedded',
        '/Launch': 'External application launch detected',
        '/EmbeddedFiles': 'Suspicious embedded files',
        '/OpenAction': 'Auto-execution on open',
        '/AA': 'Auto-action detected',
        '/URI': 'External URI reference',
        '/SubmitForm': 'Form submission action',
        '/ImportData': 'Data import action',
        '/RichMedia': 'Rich media embedded',
        '/Flash': 'Flash content detected',
        '/XFA': 'Dynamic XFA forms detected',
        '/AcroForm': 'Interactive forms present'
    }
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_hash = self._calculate_hash()
        self.is_pdf = file_path.lower().endswith('.pdf')
        self.threats = []
        self.threat_level = 'LOW'
        self.is_clean = True
        
    def _calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the file."""
        sha256_hash = hashlib.sha256()
        with open(self.file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _scan_pdf_streams(self) -> List[Dict[str, Any]]:
        """Scan PDF streams and objects for malicious tokens."""
        threats = []
        
        try:
            with open(self.file_path, 'rb') as f:
                content = f.read()
            
            # Check PDF header version (incremental updates may indicate tampering)
            if b'%PDF-' in content:
                pdf_version = re.search(b'%PDF-([\d.]+)', content)
                if pdf_version:
                    version = pdf_version.group(1).decode('utf-8', errors='ignore')
                    # Check for multiple xref sections (incremental updates)
                    xref_count = content.count(b'xref')
                    if xref_count > 1:
                        threats.append({
                            'type': 'Incremental Update',
                            'severity': 'MEDIUM',
                            'description': f'PDF has {xref_count} xref sections - possible incremental tampering',
                            'location': 'PDF structure'
                        })
            
            # Scan for each malicious token
            for token in self.MALICIOUS_TOKENS:
                if token in content:
                    token_str = token.decode('utf-8', errors='ignore')
                    description = self.THREAT_KEYWORDS.get(token_str, f'Suspicious token found: {token_str}')
                    
                    # Find context around the token
                    index = content.find(token)
                    context_start = max(0, index - 50)
                    context_end = min(len(content), index + 100)
                    context = content[context_start:context_end]
                    
                    severity = 'CRITICAL' if token_str in ['/JS', '/JavaScript', '/Launch', '/OpenAction'] else 'MEDIUM'
                    
                    threats.append({
                        'type': token_str,
                        'severity': severity,
                        'description': description,
                        'location': f'Byte offset: {index}',
                        'context': context.decode('utf-8', errors='ignore')[:100]
                    })
            
            # Check for suspicious patterns in stream objects
            stream_pattern = rb'stream\s*\n(.*?)\nendstream'
            streams = re.findall(stream_pattern, content[:10000], re.DOTALL)
            
            for i, stream in enumerate(streams[:5]):  # Check first 5 streams
                if len(stream) > 100:
                    if any(keyword in stream.lower() for keyword in [b'bash', b'cmd', b'powershell', b'exec']):
                        threats.append({
                            'type': 'Suspicious Stream Content',
                            'severity': 'CRITICAL',
                            'description': f'Shell execution patterns found in stream object {i}',
                            'location': f'Stream object {i}'
                        })
        
        except Exception as e:
            threats.append({
                'type': 'Scan Error',
                'severity': 'LOW',
                'description': f'Could not fully scan PDF: {str(e)}',
                'location': 'Scanner'
            })
        
        return threats
    
    def scan(self) -> Dict[str, Any]:
        """Run complete cyber threat scan."""
        if not self.is_pdf:
            return {
                'is_clean': True,
                'threat_level': 'LOW',
                'threats_detected': [],
                'file_hash': self.file_hash,
                'message': 'File is not a PDF - limited threat analysis available'
            }
        
        self.threats = self._scan_pdf_streams()
        
        # Determine threat level
        if any(t['severity'] == 'CRITICAL' for t in self.threats):
            self.threat_level = 'CRITICAL'
            self.is_clean = False
        elif any(t['severity'] == 'MEDIUM' for t in self.threats):
            self.threat_level = 'MEDIUM'
            self.is_clean = False
        else:
            self.threat_level = 'LOW'
            self.is_clean = True
        
        return {
            'is_clean': self.is_clean,
            'threat_level': self.threat_level,
            'threats_detected': self.threats,
            'file_hash': self.file_hash,
            'scan_timestamp': __import__('datetime').datetime.now().isoformat()
        }

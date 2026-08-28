from PIL import Image
from PIL.ExifTags import TAGS
import fitz
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from datetime import datetime

class MetadataInspector:
    """Extracts and analyzes metadata from PDFs and images."""
    
    EDITING_SOFTWARE_SIGNATURES = [
        'photoshop', 'gimp', 'canva', 'pdfescape', 'illustrator',
        'indesign', 'acrobat', 'preview', 'affinity', 'aspose',
        'imagemagick', 'graphicsmagick', 'ghostscript', 'poppler'
    ]
    
    SUSPICIOUS_METADATA_KEYWORDS = [
        'modified', 'edited', 'tampered', 'forged', 'fake',
        'corrupted', 'test', 'draft', 'sample', 'temporary'
    ]
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.metadata = {}
        self.software_detected = []
        self.creation_date = None
        self.modification_date = None
        self.suspicious_flags = []
        
    def _extract_image_exif(self) -> Dict[str, Any]:
        """Extract EXIF data from image files."""
        try:
            image = Image.open(self.file_path)
            exif_data = {}
            
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_data[tag] = str(value)[:100]
            
            # Also check for XMP data in image
            if hasattr(image, 'info'):
                exif_data.update({k: str(v)[:100] for k, v in image.info.items()})
            
            return exif_data
        except Exception as e:
            print(f"Error extracting image EXIF: {e}")
            return {}
    
    def _extract_pdf_metadata(self) -> Dict[str, Any]:
        """Extract metadata and XMP from PDF files."""
        metadata = {}
        xmp_data = {}
        
        try:
            pdf_doc = fitz.open(self.file_path)
            
            # Extract basic document metadata
            pdf_metadata = pdf_doc.metadata
            if pdf_metadata:
                for key, value in pdf_metadata.items():
                    if key and value:
                        metadata[key] = str(value)
            
            # Try to extract XMP metadata
            try:
                for page_num in range(min(3, len(pdf_doc))):  # Check first 3 pages
                    page = pdf_doc[page_num]
                    xmp_string = page.get_text('xml')
                    if xmp_string and 'xmpmeta' in xmp_string:
                        xmp_data[f'page_{page_num}'] = xmp_string[:200]
            except:
                pass
            
            pdf_doc.close()
        except Exception as e:
            print(f"Error extracting PDF metadata: {e}")
        
        return metadata | xmp_data
    
    def _check_software_signatures(self) -> List[str]:
        """Detect editing software from metadata."""
        signatures = []
        all_metadata_text = str(self.metadata).lower()
        
        for software in self.EDITING_SOFTWARE_SIGNATURES:
            if software in all_metadata_text:
                signatures.append(software.title())
        
        return signatures
    
    def _detect_suspicious_patterns(self) -> List[Dict[str, str]]:
        """Detect suspicious metadata patterns."""
        flags = []
        
        # Check for date mismatches
        if self.creation_date and self.modification_date:
            try:
                creation = datetime.fromisoformat(str(self.creation_date).replace('Z', '+00:00'))
                modification = datetime.fromisoformat(str(self.modification_date).replace('Z', '+00:00'))
                
                # If modification is significantly different from creation
                time_diff = abs((modification - creation).days)
                if time_diff > 365:
                    flags.append({
                        'type': 'Date Anomaly',
                        'severity': 'MEDIUM',
                        'description': f'Creation and modification dates differ by {time_diff} days',
                        'details': f'Created: {self.creation_date}, Modified: {self.modification_date}'
                    })
            except:
                pass
        
        # Check for suspicious keywords
        all_metadata = str(self.metadata).lower()
        suspicious_found = [kw for kw in self.SUSPICIOUS_METADATA_KEYWORDS if kw in all_metadata]
        
        if suspicious_found:
            flags.append({
                'type': 'Suspicious Keywords',
                'severity': 'LOW',
                'description': f'Found keywords: {", ".join(suspicious_found)}',
                'details': 'Document metadata contains suspicious terms'
            })
        
        # Check for multiple editing software
        if len(self.software_detected) > 2:
            flags.append({
                'type': 'Multiple Editors',
                'severity': 'MEDIUM',
                'description': f'Document edited with {len(self.software_detected)} different tools',
                'details': f'Tools: {", ".join(self.software_detected)}'
            })
        
        return flags
    
    def _parse_dates(self):
        """Extract and parse creation/modification dates."""
        try:
            # Common metadata date fields
            date_fields = {
                'CreationDate': lambda x: x,
                'ModDate': lambda x: x,
                'creation_date': lambda x: x,
                'modification_date': lambda x: x,
                'DateTime': lambda x: x,
                'DateTimeOriginal': lambda x: x,
                'DateCreated': lambda x: x,
                'DateModified': lambda x: x,
            }
            
            for key, value in self.metadata.items():
                if 'creat' in key.lower() and not self.creation_date:
                    self.creation_date = value
                if 'mod' in key.lower() and not self.modification_date:
                    self.modification_date = value
        except:
            pass
    
    def inspect(self) -> Dict[str, Any]:
        """Run complete metadata inspection."""
        # Extract metadata based on file type
        if self.file_path.lower().endswith('.pdf'):
            self.metadata = self._extract_pdf_metadata()
        else:
            self.metadata = self._extract_image_exif()
        
        # Parse dates
        self._parse_dates()
        
        # Check for software signatures
        self.software_detected = self._check_software_signatures()
        
        # Detect suspicious patterns
        self.suspicious_flags = self._detect_suspicious_patterns()
        
        return {
            'metadata': self.metadata,
            'software_detected': self.software_detected,
            'creation_date': str(self.creation_date) if self.creation_date else None,
            'modification_date': str(self.modification_date) if self.modification_date else None,
            'suspicious_patterns': self.suspicious_flags,
            'metadata_risk_level': 'MEDIUM' if len(self.suspicious_flags) > 0 else 'LOW',
            'editing_history': f'Edited by: {", ".join(self.software_detected)}' if self.software_detected else 'No editing software detected'
        }

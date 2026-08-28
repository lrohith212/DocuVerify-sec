import re
import fitz
from typing import Dict, List, Any, Tuple
import pytesseract
from PIL import Image
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class SemanticAudit:
    """Performs OCR-based text extraction and mathematical consistency audits."""
    
    MONETARY_PATTERNS = [
        r'(?:subtotal|sub[-\s]?total|amount)[:\s]*(\d+\.?\d*)',
        r'(?:tax|taxes|gst|vat)[:\s]*(\d+\.?\d*)',
        r'(?:total|grand total)[:\s]*(\d+\.?\d*)',
        r'(?:discount)[:\s]*(\d+\.?\d*)',
        r'(?:shipping|freight)[:\s]*(\d+\.?\d*)',
        r'(?:amount due|total due)[:\s]*(\d+\.?\d*)',
    ]
    
    ACADEMIC_PATTERNS = [
        r'(?:marks|score|points)[:\s]*(\d+\.?\d*)',
        r'(?:maximum|max|out of)[:\s]*(\d+\.?\d*)',
        r'(?:percentage|%)[:\s]*(\d+\.?\d*)',
        r'(?:grade)[:\s]*([a-fA-F+\-])',
    ]
    
    def __init__(self, file_path: str, output_dir: str = 'uploads'):
        self.file_path = file_path
        self.output_dir = output_dir
        self.extracted_text = ""
        self.numerical_values = {}
        self.inconsistencies = []
        self.confidence_score = 100.0
        
    def _extract_text_pytesseract(self, image) -> str:
        """Extract text using Tesseract OCR."""
        try:
            text = pytesseract.image_to_string(image, lang='eng')
            return text
        except Exception as e:
            print(f"Tesseract error: {e}")
            return ""
    
    def _extract_text_easyocr(self, image_path: str) -> str:
        """Fallback OCR using EasyOCR."""
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False)
            results = reader.readtext(image_path)
            text = '\n'.join([result[1] for result in results])
            return text
        except Exception as e:
            print(f"EasyOCR error: {e}")
            return ""
    
    def _extract_text_from_pdf(self) -> str:
        """Extract text directly from PDF using PyMuPDF."""
        try:
            pdf_doc = fitz.open(self.file_path)
            text = ""
            
            # Extract text from first 5 pages
            for page_num in range(min(5, len(pdf_doc))):
                page = pdf_doc[page_num]
                text += page.get_text('text')
            
            pdf_doc.close()
            return text
        except Exception as e:
            print(f"PDF text extraction error: {e}")
            return ""
    
    def _extract_text_from_image(self) -> str:
        """Extract text from image using OCR."""
        try:
            image = Image.open(self.file_path)
            
            # Try Tesseract first
            text = self._extract_text_pytesseract(image)
            
            # Fallback to EasyOCR if Tesseract fails
            if not text:
                text = self._extract_text_easyocr(self.file_path)
            
            return text
        except Exception as e:
            print(f"Image OCR error: {e}")
            return ""
    
    def _extract_numbers(self, text: str) -> Dict[str, List[float]]:
        """Extract all numerical values from text using regex patterns."""
        numbers = {
            'monetary': [],
            'academic': [],
            'general': []
        }
        
        # Extract monetary values
        for pattern in self.MONETARY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    numbers['monetary'].append(float(match))
                except ValueError:
                    pass
        
        # Extract academic values
        for pattern in self.ACADEMIC_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    numbers['academic'].append(float(match))
                except ValueError:
                    pass
        
        # Extract all general numbers
        general_matches = re.findall(r'\d+\.?\d*', text)
        for match in general_matches:
            try:
                numbers['general'].append(float(match))
            except ValueError:
                pass
        
        return numbers
    
    def _validate_monetary(self, numbers: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Validate monetary calculations."""
        inconsistencies = []
        monetary = numbers['monetary']
        
        if len(monetary) < 3:
            return inconsistencies
        
        # Sort values
        sorted_values = sorted(monetary)
        total = sorted_values[-1]  # Assume largest is total
        subtotal = None
        tax = None
        
        # Try to identify subtotal and tax
        if len(sorted_values) >= 3:
            subtotal = sorted_values[0]  # Smallest might be subtotal
            tax = sorted_values[1]  # Middle might be tax
        
        # Validate arithmetic
        if subtotal and tax:
            calculated_total = subtotal + tax
            tolerance = max(subtotal * 0.01, 0.01)  # 1% tolerance
            
            if abs(calculated_total - total) > tolerance:
                inconsistencies.append({
                    'type': 'Monetary Inconsistency',
                    'severity': 'HIGH',
                    'description': f'Subtotal ({subtotal}) + Tax ({tax}) = {calculated_total}, but Total is {total}',
                    'expected': calculated_total,
                    'actual': total,
                    'difference': abs(calculated_total - total)
                })
        
        return inconsistencies
    
    def _validate_academic(self, numbers: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Validate academic score calculations."""
        inconsistencies = []
        academic = numbers['academic']
        
        if len(academic) < 2:
            return inconsistencies
        
        # Check if scores exceed maximums
        marks = [v for v in academic if v < 100]
        max_marks = [v for v in academic if v >= 100]
        
        if marks and max_marks:
            for mark in marks:
                for maximum in max_marks:
                    if mark > maximum:
                        inconsistencies.append({
                            'type': 'Score Inconsistency',
                            'severity': 'HIGH',
                            'description': f'Score ({mark}) exceeds maximum ({maximum})',
                            'expected': f'Score <= {maximum}',
                            'actual': mark
                        })
        
        # Check percentage calculations
        if 'percentage' in str(numbers).lower():
            for mark in marks:
                for maximum in max_marks:
                    if maximum > 0:
                        expected_percentage = (mark / maximum) * 100
                        # If we can find a percentage value, check it
                        percentages = [v for v in academic if 0 <= v <= 100 and v not in marks]
                        for percentage in percentages:
                            if abs(percentage - expected_percentage) > 5:
                                inconsistencies.append({
                                    'type': 'Percentage Inconsistency',
                                    'severity': 'MEDIUM',
                                    'description': f'Percentage {percentage}% does not match calculated {expected_percentage:.1f}%',
                                    'expected': f'{expected_percentage:.1f}%',
                                    'actual': f'{percentage}%'
                                })
        
        return inconsistencies
    
    def audit(self) -> Dict[str, Any]:
        """Run complete semantic and mathematical audit."""
        # Extract text based on file type
        if self.file_path.lower().endswith('.pdf'):
            self.extracted_text = self._extract_text_from_pdf()
        else:
            self.extracted_text = self._extract_text_from_image()
        
        if not self.extracted_text:
            return {
                'success': False,
                'error': 'Could not extract text from file',
                'extracted_text': '',
                'numerical_values': {},
                'inconsistencies': [],
                'confidence_score': 0.0,
                'audit_status': 'FAILED'
            }
        
        # Extract numerical values
        self.numerical_values = self._extract_numbers(self.extracted_text)
        
        # Validate calculations
        monetary_issues = self._validate_monetary(self.numerical_values)
        academic_issues = self._validate_academic(self.numerical_values)
        
        self.inconsistencies = monetary_issues + academic_issues
        
        # Calculate confidence score
        if self.inconsistencies:
            severity_multiplier = sum([1 if i['severity'] == 'HIGH' else 0.5 for i in self.inconsistencies])
            self.confidence_score = max(0, 100 - (severity_multiplier * 15))
        
        return {
            'success': True,
            'extracted_text': self.extracted_text[:1000],  # First 1000 chars
            'text_length': len(self.extracted_text),
            'numerical_values': {
                'monetary_values': self.numerical_values['monetary'],
                'academic_values': self.numerical_values['academic'],
                'general_values': self.numerical_values['general'][:10]  # Limit to first 10
            },
            'inconsistencies': self.inconsistencies,
            'inconsistency_count': len(self.inconsistencies),
            'confidence_score': float(self.confidence_score),
            'audit_status': 'PASSED' if not self.inconsistencies else 'FLAGGED'
        }

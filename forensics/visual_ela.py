import cv2
import numpy as np
from PIL import Image
import os
from typing import Dict, List, Tuple, Any
import fitz

class VisualELA:
    """Performs Error Level Analysis (ELA) to detect pixel-level tampering and splicing."""
    
    def __init__(self, file_path: str, output_dir: str = 'uploads'):
        self.file_path = file_path
        self.output_dir = output_dir
        self.original_image = None
        self.ela_heatmap = None
        self.bounding_boxes = []
        self.tampering_confidence = 0.0
        
    def _extract_image(self) -> bool:
        """Extract first page of PDF as image or load image file directly."""
        try:
            if self.file_path.lower().endswith('.pdf'):
                # Convert PDF to image
                pdf_doc = fitz.open(self.file_path)
                if len(pdf_doc) == 0:
                    return False
                
                first_page = pdf_doc[0]
                # Render at 300 DPI for high resolution
                pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                img_data = pix.tobytes("ppm")
                
                from io import BytesIO
                self.original_image = Image.open(BytesIO(img_data))
                pdf_doc.close()
            else:
                # Load image directly
                self.original_image = Image.open(self.file_path)
            
            return self.original_image is not None
        except Exception as e:
            print(f"Error extracting image: {e}")
            return False
    
    def _calculate_ela(self) -> np.ndarray:
        """
        Calculate Error Level Analysis.
        Re-compress at quality 90, compute pixel-wise difference.
        """
        if self.original_image is None:
            return None
        
        try:
            # Convert to RGB if necessary
            if self.original_image.mode != 'RGB':
                original_rgb = self.original_image.convert('RGB')
            else:
                original_rgb = self.original_image
            
            # Save original as temporary file and reload as array
            temp_path = os.path.join(self.output_dir, 'temp_original.jpg')
            original_rgb.save(temp_path, 'JPEG', quality=100)
            original_array = cv2.imread(temp_path, cv2.IMREAD_COLOR)
            original_array = cv2.cvtColor(original_array, cv2.COLOR_BGR2RGB)
            
            # Re-compress at quality 90
            recompressed_path = os.path.join(self.output_dir, 'temp_recompressed.jpg')
            original_rgb.save(recompressed_path, 'JPEG', quality=90)
            recompressed_array = cv2.imread(recompressed_path, cv2.IMREAD_COLOR)
            recompressed_array = cv2.cvtColor(recompressed_array, cv2.COLOR_BGR2RGB)
            
            # Calculate absolute difference
            diff = cv2.absdiff(original_array.astype(np.float32), 
                              recompressed_array.astype(np.float32))
            
            # Scale by extrema factor for visibility
            diff_max = np.max(diff)
            if diff_max > 0:
                diff = (diff / diff_max) * 255
            
            # Convert to uint8
            diff_uint8 = np.clip(diff, 0, 255).astype(np.uint8)
            
            # Apply Gaussian blur for smoothing
            ela_smoothed = cv2.GaussianBlur(diff_uint8, (5, 5), 0)
            
            # Create heatmap (grayscale to colored)
            ela_heatmap = cv2.applyColorMap(ela_smoothed, cv2.COLORMAP_JET)
            ela_heatmap = cv2.cvtColor(ela_heatmap, cv2.COLOR_BGR2RGB)
            
            # Cleanup temp files
            for temp_file in [temp_path, recompressed_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            return ela_heatmap
        
        except Exception as e:
            print(f"Error calculating ELA: {e}")
            return None
    
    def _detect_tampering_regions(self, ela_heatmap: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect high-variance regions using contour detection.
        Return bounding boxes with confidence scores.
        """
        try:
            # Convert to grayscale for contour detection
            ela_gray = cv2.cvtColor(ela_heatmap, cv2.COLOR_RGB2GRAY)
            
            # Apply threshold to highlight high-variance regions
            _, binary = cv2.threshold(ela_gray, 100, 255, cv2.THRESH_BINARY)
            
            # Apply morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            bounding_boxes = []
            total_image_area = ela_heatmap.shape[0] * ela_heatmap.shape[1]
            
            for contour in contours:
                area = cv2.contourArea(contour)
                # Filter out very small or very large regions
                if area < 100 or area > total_image_area * 0.8:
                    continue
                
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate confidence based on variance in the region
                region = ela_gray[y:y+h, x:x+w]
                variance = np.var(region) / 255.0
                confidence = min(variance * 100, 100.0)
                
                if confidence > 20:  # Only include high-confidence detections
                    bounding_boxes.append({
                        'x': int(x),
                        'y': int(y),
                        'w': int(w),
                        'h': int(h),
                        'confidence': float(confidence),
                        'area_percentage': float((area / total_image_area) * 100)
                    })
            
            # Sort by confidence (descending)
            bounding_boxes.sort(key=lambda b: b['confidence'], reverse=True)
            
            return bounding_boxes[:10]  # Limit to top 10 regions
        
        except Exception as e:
            print(f"Error detecting tampering regions: {e}")
            return []
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete visual forensics analysis."""
        if not self._extract_image():
            return {
                'success': False,
                'error': 'Could not extract image from file',
                'original_image_path': None,
                'ela_heatmap_path': None,
                'bounding_boxes': [],
                'tampering_detected': False,
                'tampering_confidence': 0.0
            }
        
        # Save original rendered image
        original_path = os.path.join(self.output_dir, 'original_rendered.png')
        self.original_image.save(original_path, 'PNG')
        
        # Calculate ELA
        self.ela_heatmap = self._calculate_ela()
        if self.ela_heatmap is None:
            return {
                'success': False,
                'error': 'Could not calculate ELA',
                'original_image_path': original_path,
                'ela_heatmap_path': None,
                'bounding_boxes': [],
                'tampering_detected': False,
                'tampering_confidence': 0.0
            }
        
        # Save ELA heatmap
        ela_path = os.path.join(self.output_dir, 'ela_heatmap.png')
        ela_pil = Image.fromarray(self.ela_heatmap)
        ela_pil.save(ela_path, 'PNG')
        
        # Detect tampering regions
        self.bounding_boxes = self._detect_tampering_regions(self.ela_heatmap)
        
        # Calculate overall tampering confidence
        if self.bounding_boxes:
            self.tampering_confidence = np.mean([b['confidence'] for b in self.bounding_boxes])
        
        tampering_detected = len(self.bounding_boxes) > 3 or self.tampering_confidence > 50
        
        return {
            'success': True,
            'original_image_path': original_path,
            'ela_heatmap_path': ela_path,
            'bounding_boxes': self.bounding_boxes,
            'tampering_detected': tampering_detected,
            'tampering_confidence': float(self.tampering_confidence),
            'high_variance_regions': len(self.bounding_boxes),
            'analysis_details': 'ELA and contour analysis complete'
        }

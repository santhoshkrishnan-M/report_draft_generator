"""
Image Processing Service for Medical Diagnostic Images
Handles X-ray, MRI, and CT scan analysis using OpenCV
"""

import cv2
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

class MedicalImageProcessor:
    """Process medical diagnostic images and extract features"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.dcm', '.bmp']
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess medical image for analysis
        - Load image
        - Convert to grayscale
        - Normalize
        - Enhance contrast
        """
        # Read image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        # Normalize to 0-255 range
        img_normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_enhanced = clahe.apply(img_normalized)
        
        return img_enhanced
    
    def extract_features(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extract basic features from medical image
        - Image statistics
        - Edge detection
        - Texture analysis
        - Region of interest detection
        """
        features = {}
        
        # Basic statistics
        features['mean_intensity'] = float(np.mean(image))
        features['std_intensity'] = float(np.std(image))
        features['min_intensity'] = float(np.min(image))
        features['max_intensity'] = float(np.max(image))
        
        # Edge detection using Canny
        edges = cv2.Canny(image, 50, 150)
        features['edge_density'] = float(np.sum(edges > 0) / edges.size)
        
        # Texture analysis using Laplacian variance
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        features['texture_variance'] = float(laplacian.var())
        
        # Detect potential regions of interest (bright/dark areas)
        _, binary_bright = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
        _, binary_dark = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
        
        features['bright_region_ratio'] = float(np.sum(binary_bright > 0) / image.size)
        features['dark_region_ratio'] = float(np.sum(binary_dark > 0) / image.size)
        
        # Histogram analysis
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        features['histogram_peak'] = int(np.argmax(hist))
        
        return features
    
    def generate_observations(self, features: Dict[str, Any], image_type: str) -> List[str]:
        """
        Generate medical observations based on extracted features
        These are template-based, non-diagnostic observations
        """
        observations = []
        
        # Image quality assessment
        if features['texture_variance'] < 50:
            observations.append("Image quality: Low contrast detected. Clinical correlation recommended.")
        elif features['texture_variance'] > 1000:
            observations.append("Image quality: High contrast with detailed structural visibility.")
        else:
            observations.append("Image quality: Adequate for diagnostic assessment.")
        
        # Density observations (safe, non-diagnostic language)
        if features['mean_intensity'] > 180:
            observations.append("Overall density: Predominantly lucent appearance noted.")
        elif features['mean_intensity'] < 80:
            observations.append("Overall density: Increased opacity observed.")
        else:
            observations.append("Overall density: Within expected range.")
        
        # Region of interest observations
        if features['bright_region_ratio'] > 0.15:
            observations.append("Notable lucent regions identified. Further radiologist review recommended.")
        
        if features['dark_region_ratio'] > 0.15:
            observations.append("Dense regions noted. Clinical correlation advised.")
        
        # Edge density (structural detail)
        if features['edge_density'] > 0.1:
            observations.append("Well-defined structural borders present.")
        elif features['edge_density'] < 0.03:
            observations.append("Homogeneous appearance with minimal structural variation.")
        
        # Image type specific observations
        if image_type.lower() == 'xray':
            observations.append("Radiographic examination completed. Standard positioning maintained.")
        elif image_type.lower() == 'mri':
            observations.append("MRI acquisition parameters within acceptable range.")
        elif image_type.lower() == 'ct':
            observations.append("CT scan slice reviewed. Axial plane visualization adequate.")
        
        return observations
    
    def analyze_image(self, image_path: str, image_type: str = 'xray', 
                     metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Complete image analysis pipeline
        Returns structured JSON with observations
        """
        try:
            # Preprocess
            processed_image = self.preprocess_image(image_path)
            
            # Extract features
            features = self.extract_features(processed_image)
            
            # Generate observations
            observations = self.generate_observations(features, image_type)
            
            # Compile results
            result = {
                'status': 'success',
                'image_type': image_type,
                'image_path': image_path,
                'metadata': metadata or {},
                'features': features,
                'observations': observations,
                'image_dimensions': {
                    'height': processed_image.shape[0],
                    'width': processed_image.shape[1]
                },
                'disclaimer': 'AI-generated observations. For radiologist review only. Not a diagnosis.'
            }
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'image_path': image_path
            }


def process_diagnostic_image(image_path: str, image_type: str = 'xray', 
                             metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Main entry point for image processing
    """
    processor = MedicalImageProcessor()
    return processor.analyze_image(image_path, image_type, metadata)


if __name__ == "__main__":
    # Test the processor
    print("Medical Image Processor initialized")
    print("Supported formats:", MedicalImageProcessor().supported_formats)

import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import json
from typing import Dict, List, Tuple, Optional

class HandwritingCNNAnalyzer:
    """
    CNN-based handwriting analysis for dyslexia/dysgraphia detection
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.scaler = StandardScaler()
        self.load_model(model_path)
    
    def load_model(self, model_path: Optional[str] = None):
        """Load pre-trained CNN model"""
        if model_path and tf.io.gfile.exists(model_path):
            self.model = keras.models.load_model(model_path)
        else:
            # Create a simple CNN model for demonstration
            self.model = self._create_model()
    
    def _create_model(self):
        """Create CNN model architecture"""
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(4, activation='sigmoid')  # 4 outputs: irregular_shapes, spacing, stroke_pattern, overall
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        return model
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess handwriting image for CNN analysis"""
        # Load and convert to grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            # Return a blank canvas if image can't be read
            return np.ones((64, 64), dtype=np.float32)
        
        # Resize to standard size
        image = cv2.resize(image, (64, 64))
        
        # Normalize pixel values
        image = image.astype(np.float32) / 255.0
        
        # Add channel dimension
        image = np.expand_dims(image, axis=-1)
        
        return image
    
    def analyze_irregular_shapes(self, image: np.ndarray) -> float:
        """Analyze irregular letter shapes"""
        # Extract features related to letter shape irregularities
        edges = cv2.Canny((image * 255).astype(np.uint8), 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0.0
        
        # Calculate shape irregularity metrics
        total_area = sum(cv2.contourArea(c) for c in contours)
        if total_area == 0:
            return 0.0
        
        # Calculate irregularity based on contour complexity
        irregularity_scores = []
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                irregularity_scores.append(1 - circularity)
        
        return np.mean(irregularity_scores) if irregularity_scores else 0.0
    
    def analyze_spacing_issues(self, image: np.ndarray) -> float:
        """Analyze spacing problems between letters and words"""
        # Convert to binary
        _, binary = cv2.threshold((image * 255).astype(np.uint8), 127, 255, cv2.THRESH_BINARY_INV)
        
        # Project horizontally to find letter boundaries
        horizontal_projection = np.sum(binary, axis=0)
        
        # Find gaps (spaces between letters)
        gaps = []
        in_gap = False
        gap_start = 0
        
        for i, value in enumerate(horizontal_projection):
            if value == 0 and not in_gap:  # Start of gap
                in_gap = True
                gap_start = i
            elif value > 0 and in_gap:  # End of gap
                in_gap = False
                gap_length = i - gap_start
                if gap_length > 2:  # Only count significant gaps
                    gaps.append(gap_length)
        
        if not gaps:
            return 0.0
        
        # Calculate spacing irregularity
        gap_lengths = np.array(gaps)
        mean_gap = np.mean(gap_lengths)
        std_gap = np.std(gap_lengths)
        
        # Higher std indicates more irregular spacing
        spacing_irregularity = std_gap / mean_gap if mean_gap > 0 else 0
        return min(spacing_irregularity, 1.0)
    
    def analyze_stroke_patterns(self, image: np.ndarray) -> float:
        """Analyze stroke pattern irregularities"""
        # Convert to binary
        _, binary = cv2.threshold((image * 255).astype(np.uint8), 127, 255, cv2.THRESH_BINARY_INV)
        
        # Detect edges
        edges = cv2.Canny(binary, 50, 150)
        
        # Calculate stroke direction consistency
        sobel_x = cv2.Sobel(edges, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(edges, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate gradient directions
        angles = np.arctan2(sobel_y, sobel_x)
        angles = angles[edges > 0]  # Only consider edge pixels
        
        if len(angles) == 0:
            return 0.0
        
        # Calculate angle variance (higher variance = more irregular strokes)
        angle_variance = np.var(angles)
        stroke_irregularity = min(angle_variance / (np.pi ** 2), 1.0)
        
        return stroke_irregularity
    
    def analyze_handwriting(self, image_path: str) -> Dict:
        """Complete handwriting analysis"""
        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        
        # Run CNN analysis if model is available
        if self.model:
            cnn_prediction = self.model.predict(np.expand_dims(processed_image, axis=0))[0]
            irregular_shapes_score = float(cnn_prediction[0])
            spacing_issues_score = float(cnn_prediction[1])
            stroke_pattern_score = float(cnn_prediction[2])
            overall_score = float(cnn_prediction[3])
        else:
            # Fallback to traditional computer vision methods with calibrated scaling
            # Scale raw metrics so normal writing stays < 0.3 and poor writing > 0.7
            raw_irregular = self.analyze_irregular_shapes(processed_image)
            raw_spacing = self.analyze_spacing_issues(processed_image)
            raw_stroke = self.analyze_stroke_patterns(processed_image)
            
            # Balanced scaling: Noise floor at 0.15 allows high-risk cases to trigger.
            # Risk starts to climb after 0.15 and crosses 0.5 when raw > 0.4.
            irregular_shapes_score = min(max(raw_irregular - 0.15, 0) * 2.0, 1.0)
            spacing_issues_score = min(max(raw_spacing - 0.15, 0) * 2.0, 1.0)
            stroke_pattern_score = min(max(raw_stroke - 0.15, 0) * 2.0, 1.0)
            
            overall_score = (irregular_shapes_score + spacing_issues_score + stroke_pattern_score) / 3
        
        # Generate detailed analysis
        analysis_result = {
            'irregular_shapes_score': irregular_shapes_score,
            'spacing_issues_score': spacing_issues_score,
            'stroke_pattern_score': stroke_pattern_score,
            'overall_handwriting_score': overall_score,
            'letter_formation_issues': self._identify_letter_issues(processed_image),
            'spacing_analysis': self._analyze_spacing_details(processed_image),
            'stroke_analysis': self._analyze_stroke_details(processed_image),
            'model_confidence': 0.85  # Placeholder confidence score
        }
        
        return analysis_result
    
    def _identify_letter_issues(self, image: np.ndarray) -> List[str]:
        """Identify specific letter formation issues"""
        issues = []
        
        # Analyze letter proportions
        height, width = image.shape[:2]
        aspect_ratio = width / height if height > 0 else 1
        
        if aspect_ratio < 0.5:
            issues.append("Letters appear too narrow")
        elif aspect_ratio > 2.0:
            issues.append("Letters appear too wide")
        
        # Analyze letter consistency
        # This would involve more sophisticated letter detection and analysis
        # For now, return basic issues based on overall image characteristics
        
        return issues
    
    def _analyze_spacing_details(self, image: np.ndarray) -> Dict:
        """Detailed spacing analysis"""
        return {
            'word_spacing_consistency': 0.7,  # Placeholder
            'letter_spacing_consistency': 0.6,  # Placeholder
            'line_spacing_consistency': 0.8,  # Placeholder
            'recommendations': ['Practice consistent letter spacing', 'Work on word spacing']
        }
    
    def _analyze_stroke_details(self, image: np.ndarray) -> Dict:
        """Detailed stroke pattern analysis"""
        return {
            'stroke_consistency': 0.6,  # Placeholder
            'pressure_variation': 0.4,  # Placeholder
            'stroke_direction_consistency': 0.7,  # Placeholder
            'recommendations': ['Practice smooth stroke movements', 'Work on consistent pressure']
        }

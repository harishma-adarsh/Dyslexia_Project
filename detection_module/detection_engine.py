import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import json

class DyslexiaDetectionEngine:
    """
    Combined detection engine that integrates handwriting and speech analysis
    """
    
    def __init__(self):
        self.handwriting_weights = {
            'irregular_shapes': 0.3,
            'spacing_issues': 0.25,
            'stroke_patterns': 0.25,
            'overall_handwriting': 0.2
        }
        
        self.speech_weights = {
            'pronunciation': 0.3,
            'fluency': 0.25,
            'reading_speed': 0.2,
            'rhythm': 0.25
        }
        
        self.combined_weights = {
            'handwriting': 0.5,
            'speech': 0.5
        }
        
        # Risk thresholds
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    
    def calculate_handwriting_risk(self, handwriting_analysis: Dict) -> float:
        """Calculate dyslexia risk from handwriting analysis"""
        scores = []
        weights = []
        
        # Extract scores
        if 'irregular_shapes_score' in handwriting_analysis:
            scores.append(handwriting_analysis['irregular_shapes_score'])
            weights.append(self.handwriting_weights['irregular_shapes'])
        
        if 'spacing_issues_score' in handwriting_analysis:
            scores.append(handwriting_analysis['spacing_issues_score'])
            weights.append(self.handwriting_weights['spacing_issues'])
        
        if 'stroke_pattern_score' in handwriting_analysis:
            scores.append(handwriting_analysis['stroke_pattern_score'])
            weights.append(self.handwriting_weights['stroke_patterns'])
        
        if 'overall_handwriting_score' in handwriting_analysis:
            scores.append(handwriting_analysis['overall_handwriting_score'])
            weights.append(self.handwriting_weights['overall_handwriting'])
        
        if not scores:
            return 0.0
        
        # Calculate weighted average
        weighted_score = np.average(scores, weights=weights)
        return min(max(weighted_score, 0), 1)
    
    def calculate_speech_risk(self, speech_analysis: Dict) -> float:
        """Calculate dyslexia risk from speech analysis"""
        scores = []
        weights = []
        
        # Extract scores (invert some scores where lower is better)
        if 'pronunciation_score' in speech_analysis:
            # Lower pronunciation score = higher risk
            risk_score = 1 - speech_analysis['pronunciation_score']
            scores.append(risk_score)
            weights.append(self.speech_weights['pronunciation'])
        
        if 'fluency_score' in speech_analysis:
            # Lower fluency score = higher risk
            risk_score = 1 - speech_analysis['fluency_score']
            scores.append(risk_score)
            weights.append(self.speech_weights['fluency'])
        
        if 'reading_speed' in speech_analysis:
            # Normalize reading speed (assume 150 WPM is normal)
            normalized_speed = min(speech_analysis['reading_speed'] / 150, 1)
            risk_score = 1 - normalized_speed
            scores.append(risk_score)
            weights.append(self.speech_weights['reading_speed'])
        
        if 'rhythm_score' in speech_analysis:
            # Lower rhythm score = higher risk
            risk_score = 1 - speech_analysis['rhythm_score']
            scores.append(risk_score)
            weights.append(self.speech_weights['rhythm'])
        
        if not scores:
            return 0.0
        
        # Calculate weighted average
        weighted_score = np.average(scores, weights=weights)
        return min(max(weighted_score, 0), 1)
    
    def calculate_combined_risk(self, handwriting_risk: float, speech_risk: float) -> float:
        """Calculate combined dyslexia risk score"""
        combined_risk = (
            handwriting_risk * self.combined_weights['handwriting'] +
            speech_risk * self.combined_weights['speech']
        )
        return min(max(combined_risk, 0), 1)
    
    def determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on score"""
        if risk_score < self.risk_thresholds['low']:
            return 'low'
        elif risk_score < self.risk_thresholds['medium']:
            return 'medium'
        else:
            return 'high'
    
    def generate_recommendations(self, handwriting_analysis: Dict, speech_analysis: Dict, risk_level: str) -> List[str]:
        """Generate personalized recommendations based on analysis"""
        recommendations = []
        
        # Handwriting-based recommendations
        if 'letter_formation_issues' in handwriting_analysis:
            if handwriting_analysis['letter_formation_issues']:
                recommendations.append("Practice letter formation exercises")
        
        if 'spacing_analysis' in handwriting_analysis:
            spacing_analysis = handwriting_analysis['spacing_analysis']
            if spacing_analysis.get('word_spacing_consistency', 1) < 0.7:
                recommendations.append("Work on consistent word spacing")
            if spacing_analysis.get('letter_spacing_consistency', 1) < 0.7:
                recommendations.append("Practice letter spacing exercises")
        
        # Speech-based recommendations
        if 'mispronunciations' in speech_analysis and speech_analysis['mispronunciations']:
            recommendations.append("Practice pronunciation exercises")
        
        if 'fluency_issues' in speech_analysis and speech_analysis['fluency_issues']:
            recommendations.append("Work on speech fluency and rhythm")
        
        # Risk-level specific recommendations
        if risk_level == 'high':
            recommendations.extend([
                "Consider professional assessment",
                "Implement intensive intervention program",
                "Regular progress monitoring recommended"
            ])
        elif risk_level == 'medium':
            recommendations.extend([
                "Continue with targeted exercises",
                "Monitor progress regularly",
                "Consider additional support if needed"
            ])
        else:
            recommendations.extend([
                "Continue current activities",
                "Regular practice recommended",
                "Monitor for any changes"
            ])
        
        return recommendations
    
    def identify_strengths(self, handwriting_analysis: Dict, speech_analysis: Dict) -> List[str]:
        """Identify areas of strength"""
        strengths = []
        
        # Handwriting strengths
        if handwriting_analysis.get('overall_handwriting_score', 0) > 0.7:
            strengths.append("Good overall handwriting quality")
        
        if handwriting_analysis.get('stroke_pattern_score', 0) > 0.7:
            strengths.append("Consistent stroke patterns")
        
        # Speech strengths
        if speech_analysis.get('pronunciation_score', 0) > 0.7:
            strengths.append("Good pronunciation accuracy")
        
        if speech_analysis.get('fluency_score', 0) > 0.7:
            strengths.append("Good speech fluency")
        
        if speech_analysis.get('rhythm_score', 0) > 0.7:
            strengths.append("Good speech rhythm")
        
        return strengths
    
    def identify_concerns(self, handwriting_analysis: Dict, speech_analysis: Dict) -> List[str]:
        """Identify areas of concern"""
        concerns = []
        
        # Handwriting concerns
        if handwriting_analysis.get('irregular_shapes_score', 0) > 0.6:
            concerns.append("Irregular letter shapes detected")
        
        if handwriting_analysis.get('spacing_issues_score', 0) > 0.6:
            concerns.append("Spacing issues in handwriting")
        
        if handwriting_analysis.get('stroke_pattern_score', 0) > 0.6:
            concerns.append("Inconsistent stroke patterns")
        
        # Speech concerns
        if speech_analysis.get('pronunciation_score', 0) < 0.4:
            concerns.append("Pronunciation difficulties")
        
        if speech_analysis.get('fluency_score', 0) < 0.4:
            concerns.append("Speech fluency issues")
        
        if speech_analysis.get('reading_speed', 0) < 100:  # WPM
            concerns.append("Slow reading speed")
        
        return concerns
    
    def calculate_confidence(self, handwriting_analysis: Dict, speech_analysis: Dict) -> float:
        """Calculate overall detection confidence"""
        confidence_scores = []
        
        # Handwriting confidence
        if 'model_confidence' in handwriting_analysis:
            confidence_scores.append(handwriting_analysis['model_confidence'])
        
        # Speech confidence
        if 'model_confidence' in speech_analysis:
            confidence_scores.append(speech_analysis['model_confidence'])
        
        if not confidence_scores:
            return 0.5  # Default confidence
        
        return np.mean(confidence_scores)
    
    def detect_dyslexia(self, handwriting_analysis: Optional[Dict] = None, 
                       speech_analysis: Optional[Dict] = None) -> Dict:
        """
        Main detection function that combines handwriting and speech analysis
        """
        results = {
            'dyslexia_probability': 0.0,
            'dysgraphia_probability': 0.0,
            'overall_risk_score': 0.0,
            'risk_level': 'low',
            'detection_confidence': 0.0,
            'recommended_actions': [],
            'strengths_identified': [],
            'areas_of_concern': []
        }
        
        # Calculate individual risks
        handwriting_risk = 0.0
        speech_risk = 0.0
        
        if handwriting_analysis:
            handwriting_risk = self.calculate_handwriting_risk(handwriting_analysis)
            results['dysgraphia_probability'] = handwriting_risk
        
        if speech_analysis:
            speech_risk = self.calculate_speech_risk(speech_analysis)
        
        # Calculate combined risk
        if handwriting_analysis and speech_analysis:
            results['overall_risk_score'] = self.calculate_combined_risk(handwriting_risk, speech_risk)
            results['dyslexia_probability'] = results['overall_risk_score']
        elif handwriting_analysis:
            results['overall_risk_score'] = handwriting_risk
            results['dyslexia_probability'] = handwriting_risk
        elif speech_analysis:
            results['overall_risk_score'] = speech_risk
            results['dyslexia_probability'] = speech_risk
        
        # Determine risk level
        results['risk_level'] = self.determine_risk_level(results['overall_risk_score'])
        
        # Generate recommendations and analysis
        results['recommended_actions'] = self.generate_recommendations(
            handwriting_analysis or {}, speech_analysis or {}, results['risk_level']
        )
        
        results['strengths_identified'] = self.identify_strengths(
            handwriting_analysis or {}, speech_analysis or {}
        )
        
        results['areas_of_concern'] = self.identify_concerns(
            handwriting_analysis or {}, speech_analysis or {}
        )
        
        # Calculate confidence
        results['detection_confidence'] = self.calculate_confidence(
            handwriting_analysis or {}, speech_analysis or {}
        )
        
        return results

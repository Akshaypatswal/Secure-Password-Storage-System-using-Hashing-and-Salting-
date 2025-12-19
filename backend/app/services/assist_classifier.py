"""
Assist Mode Classifier
Rule-based and ML classifier for assist mode recommendation
"""

import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class AssistClassifier:
    """
    Classifier for assist mode recommendation
    
    Uses rule-based classification with optional ML enhancement
    """
    
    def __init__(self):
        self.is_ml_loaded = False
        # In production, load trained ML model here
        # self.ml_model = load_model('models/assist_classifier.pkl')
    
    def is_loaded(self) -> bool:
        """Check if classifier is loaded"""
        return True  # Rule-based is always available
    
    def classify(self, features: Dict) -> Dict:
        """
        Classify features and return recommendation
        
        Args:
            features: Dictionary of extracted features
        
        Returns:
            Recommendation with mode, confidence, cues, scores, and explainability
        """
        # Extract features
        hand_sign_freq = features.get('handSignFreq', 0.0)
        speech_detected = features.get('speechDetected', False)
        gaze_pattern = features.get('gazePattern')
        posture = features.get('posture')
        interaction_behavior = features.get('interactionBehavior')
        
        # Calculate scores for each mode
        scores = self._calculate_scores(
            hand_sign_freq, speech_detected, gaze_pattern, 
            posture, interaction_behavior
        )
        
        # Get top mode
        top_mode = max(scores.items(), key=lambda x: x[1])
        mode, confidence = top_mode
        
        # Generate cues
        cues = self._generate_cues(
            mode, hand_sign_freq, speech_detected, 
            gaze_pattern, posture, interaction_behavior
        )
        
        # Explainability
        explainability = {
            "top_features": self._get_top_features(scores),
            "reasoning": self._get_reasoning(mode, scores, features)
        }
        
        return {
            "mode": mode,
            "confidence": confidence,
            "cues": cues,
            "scores": scores,
            "explainability": explainability
        }
    
    def _calculate_scores(
        self, 
        hand_sign_freq: float,
        speech_detected: bool,
        gaze_pattern: str,
        posture: str,
        interaction_behavior: str
    ) -> Dict[str, float]:
        """
        Calculate scores for each assist mode
        
        Returns:
            Dictionary of mode scores
        """
        scores = {
            "voice": 0.0,
            "sign": 0.0,
            "text": 0.0,
            "gesture": 0.0,
            "motor": 0.0
        }
        
        # Sign mode scoring
        if hand_sign_freq > 3.0:
            scores["sign"] += 0.6
        if hand_sign_freq > 5.0:
            scores["sign"] += 0.3
        if hand_sign_freq > 7.0:
            scores["sign"] += 0.1
        
        # Voice mode scoring
        if speech_detected:
            scores["voice"] += 0.4
        if gaze_pattern == "low" or gaze_pattern == "inconsistent":
            scores["voice"] += 0.3
        if interaction_behavior == "voice":
            scores["voice"] += 0.3
        
        # Text mode scoring
        if not speech_detected and hand_sign_freq < 2.0:
            scores["text"] += 0.5
        if interaction_behavior == "text":
            scores["text"] += 0.5
        
        # Gesture mode scoring
        if hand_sign_freq > 1.0 and hand_sign_freq < 3.0:
            scores["gesture"] += 0.4
        if posture == "seated" or posture == "wheelchair":
            scores["gesture"] += 0.3
        if interaction_behavior == "gesture":
            scores["gesture"] += 0.3
        
        # Motor mode scoring
        if posture == "wheelchair" or posture == "assistive_device":
            scores["motor"] += 0.5
        if interaction_behavior == "limited_mobility":
            scores["motor"] += 0.5
        
        # Normalize scores to [0, 1]
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1.0
        scores = {k: min(v / max_score, 1.0) for k, v in scores.items()}
        
        # If all scores are low, default to text mode
        if max(scores.values()) < 0.3:
            scores["text"] = 0.5
        
        return scores
    
    def _generate_cues(
        self,
        mode: str,
        hand_sign_freq: float,
        speech_detected: bool,
        gaze_pattern: str,
        posture: str,
        interaction_behavior: str
    ) -> List[str]:
        """Generate explainability cues"""
        cues = []
        
        if mode == "sign":
            if hand_sign_freq > 5.0:
                cues.append(f"Detected repeated hand-signing gestures (frequency: {hand_sign_freq:.1f})")
            if hand_sign_freq > 3.0:
                cues.append("Strong indication of sign language preference")
        
        elif mode == "voice":
            if speech_detected:
                cues.append("Speech activity detected during scan")
            if gaze_pattern == "low" or gaze_pattern == "inconsistent":
                cues.append("Gaze patterns suggest low-vision interaction needs")
            if interaction_behavior == "voice":
                cues.append("User demonstrated voice command preference")
        
        elif mode == "text":
            if not speech_detected:
                cues.append("No speech detected - text-based interface may be preferred")
            if interaction_behavior == "text":
                cues.append("User demonstrated text input preference")
        
        elif mode == "gesture":
            if hand_sign_freq > 1.0:
                cues.append("Hand movement detected - gesture interface may be suitable")
            if posture == "seated" or posture == "wheelchair":
                cues.append("Posture cues suggest gesture-based interaction")
        
        elif mode == "motor":
            if posture == "wheelchair" or posture == "assistive_device":
                cues.append("Posture/mobility cues suggest motor-adapted interface")
            if interaction_behavior == "limited_mobility":
                cues.append("Interaction patterns suggest motor adaptation needs")
        
        # Default cue if no specific cues
        if not cues:
            cues.append("Based on general interaction patterns")
        
        return cues[:3]  # Return top 3 cues
    
    def _get_top_features(self, scores: Dict[str, float]) -> List[Tuple[str, float]]:
        """Get top features by score"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:3]
    
    def _get_reasoning(
        self, 
        mode: str, 
        scores: Dict[str, float], 
        features: Dict
    ) -> str:
        """Generate reasoning explanation"""
        top_score = scores[mode]
        
        if top_score > 0.7:
            return f"Strong recommendation for {mode} mode based on clear interaction patterns."
        elif top_score > 0.5:
            return f"Moderate recommendation for {mode} mode. Consider manual selection if unsure."
        else:
            return f"Weak recommendation. Manual selection is recommended."


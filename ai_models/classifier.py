"""
Assist Mode Classifier
Rule-based and ML classifier for assist mode recommendation
"""

import numpy as np
from typing import Dict, List, Tuple
import pickle
import os

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. Using rule-based classifier only.")


class RuleBasedClassifier:
    """
    Rule-based classifier for assist mode recommendation
    """
    
    def classify(self, features: Dict) -> Dict:
        """
        Classify features using rule-based approach
        
        Args:
            features: Dictionary of extracted features
        
        Returns:
            Recommendation with mode, confidence, cues, and scores
        """
        # Extract features
        hand_sign_freq = features.get('handSignFreq', 0.0)
        speech_detected = features.get('speechDetected', False)
        gaze_pattern = features.get('gazePattern')
        posture = features.get('posture')
        interaction_behavior = features.get('interactionBehavior')
        
        # Calculate scores
        scores = {
            "voice": 0.0,
            "sign": 0.0,
            "text": 0.0,
            "gesture": 0.0,
            "motor": 0.0
        }
        
        # Sign mode
        if hand_sign_freq > 5.0:
            scores["sign"] = 0.9
        elif hand_sign_freq > 3.0:
            scores["sign"] = 0.7
        elif hand_sign_freq > 1.0:
            scores["sign"] = 0.5
        
        # Voice mode
        if speech_detected:
            scores["voice"] += 0.4
        if gaze_pattern in ["low", "inconsistent"]:
            scores["voice"] += 0.3
        if interaction_behavior == "voice":
            scores["voice"] += 0.3
        
        # Text mode
        if not speech_detected and hand_sign_freq < 2.0:
            scores["text"] = 0.6
        if interaction_behavior == "text":
            scores["text"] = 0.8
        
        # Gesture mode
        if 1.0 < hand_sign_freq < 3.0:
            scores["gesture"] = 0.6
        if posture in ["seated", "wheelchair"]:
            scores["gesture"] += 0.3
        
        # Motor mode
        if posture in ["wheelchair", "assistive_device"]:
            scores["motor"] = 0.8
        if interaction_behavior == "limited_mobility":
            scores["motor"] = 0.9
        
        # Normalize scores
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1.0
        scores = {k: min(v / max_score, 1.0) for k, v in scores.items()}
        
        # Get top mode
        top_mode = max(scores.items(), key=lambda x: x[1])
        mode, confidence = top_mode
        
        # Generate cues
        cues = self._generate_cues(mode, features, scores)
        
        return {
            "mode": mode,
            "confidence": confidence,
            "cues": cues,
            "scores": scores
        }
    
    def _generate_cues(self, mode: str, features: Dict, scores: Dict) -> List[str]:
        """Generate explainability cues"""
        cues = []
        
        if mode == "sign":
            if features.get('handSignFreq', 0) > 5.0:
                cues.append(f"Detected repeated hand-signing gestures (frequency: {features['handSignFreq']:.1f})")
            cues.append("Strong indication of sign language preference")
        
        elif mode == "voice":
            if features.get('speechDetected'):
                cues.append("Speech activity detected during scan")
            if features.get('gazePattern') in ["low", "inconsistent"]:
                cues.append("Gaze patterns suggest low-vision interaction needs")
        
        elif mode == "text":
            if not features.get('speechDetected'):
                cues.append("No speech detected - text-based interface may be preferred")
        
        elif mode == "gesture":
            if features.get('handSignFreq', 0) > 1.0:
                cues.append("Hand movement detected - gesture interface may be suitable")
        
        elif mode == "motor":
            if features.get('posture') in ["wheelchair", "assistive_device"]:
                cues.append("Posture/mobility cues suggest motor-adapted interface")
        
        if not cues:
            cues.append("Based on general interaction patterns")
        
        return cues[:3]


class MLClassifier:
    """
    ML-based classifier (optional enhancement)
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.model_path = model_path or "models/assist_classifier.pkl"
        
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            print(f"Model not found at {self.model_path}. Using rule-based classifier.")
    
    def load_model(self):
        """Load trained model"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        Train ML model on synthetic/sample data
        
        Args:
            X: Feature matrix
            y: Target labels
        """
        if not SKLEARN_AVAILABLE:
            print("scikit-learn not available. Cannot train ML model.")
            return
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def classify(self, features: Dict) -> Dict:
        """
        Classify using ML model
        
        Args:
            features: Dictionary of extracted features
        
        Returns:
            Recommendation
        """
        if self.model is None:
            # Fallback to rule-based
            rule_classifier = RuleBasedClassifier()
            return rule_classifier.classify(features)
        
        # Convert features to array
        feature_vector = self._features_to_vector(features)
        
        # Predict
        prediction = self.model.predict([feature_vector])[0]
        probabilities = self.model.predict_proba([feature_vector])[0]
        
        # Map to mode names
        mode_names = ["voice", "sign", "text", "gesture", "motor"]
        mode = mode_names[prediction]
        confidence = float(probabilities[prediction])
        
        # Get all scores
        scores = {mode_names[i]: float(prob) for i, prob in enumerate(probabilities)}
        
        # Generate cues
        cues = self._generate_cues(mode, features, scores)
        
        return {
            "mode": mode,
            "confidence": confidence,
            "cues": cues,
            "scores": scores
        }
    
    def _features_to_vector(self, features: Dict) -> np.ndarray:
        """Convert features dictionary to feature vector"""
        vector = [
            features.get('handSignFreq', 0.0),
            1.0 if features.get('speechDetected') else 0.0,
            1.0 if features.get('gazePattern') == 'low' else 0.0,
            1.0 if features.get('posture') == 'wheelchair' else 0.0,
            1.0 if features.get('interactionBehavior') == 'voice' else 0.0,
        ]
        return np.array(vector)
    
    def _generate_cues(self, mode: str, features: Dict, scores: Dict) -> List[str]:
        """Generate explainability cues"""
        cues = []
        
        if mode == "sign":
            cues.append("ML model detected sign language patterns")
        elif mode == "voice":
            cues.append("ML model detected voice interaction patterns")
        elif mode == "text":
            cues.append("ML model detected text interaction patterns")
        elif mode == "gesture":
            cues.append("ML model detected gesture interaction patterns")
        elif mode == "motor":
            cues.append("ML model detected motor adaptation needs")
        
        return cues


def generate_synthetic_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic training data
    
    Args:
        n_samples: Number of samples to generate
    
    Returns:
        X (features), y (labels)
    """
    np.random.seed(42)
    
    X = []
    y = []
    
    for _ in range(n_samples):
        # Generate random features
        hand_sign_freq = np.random.uniform(0, 10)
        speech_detected = np.random.choice([0, 1])
        gaze_low = np.random.choice([0, 1])
        wheelchair = np.random.choice([0, 1])
        voice_behavior = np.random.choice([0, 1])
        
        features = [hand_sign_freq, speech_detected, gaze_low, wheelchair, voice_behavior]
        X.append(features)
        
        # Generate label based on rules
        if hand_sign_freq > 5:
            label = 1  # sign
        elif speech_detected and gaze_low:
            label = 0  # voice
        elif wheelchair:
            label = 4  # motor
        elif hand_sign_freq > 1:
            label = 3  # gesture
        else:
            label = 2  # text
        
        y.append(label)
    
    return np.array(X), np.array(y)


def main():
    """Demo: Train and test classifier"""
    print("Assist Mode Classifier Demo")
    print("=" * 50)
    
    # Test rule-based classifier
    print("\n1. Testing Rule-Based Classifier:")
    rule_classifier = RuleBasedClassifier()
    
    test_features = {
        "handSignFreq": 6.5,
        "speechDetected": False,
        "gazePattern": "normal",
        "posture": "seated",
        "interactionBehavior": None
    }
    
    result = rule_classifier.classify(test_features)
    print(f"Mode: {result['mode']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Cues: {result['cues']}")
    print(f"Scores: {result['scores']}")
    
    # Train ML classifier if sklearn available
    if SKLEARN_AVAILABLE:
        print("\n2. Training ML Classifier:")
        X, y = generate_synthetic_data(n_samples=500)
        
        ml_classifier = MLClassifier()
        ml_classifier.train(X, y)
        
        print("\n3. Testing ML Classifier:")
        result = ml_classifier.classify(test_features)
        print(f"Mode: {result['mode']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Cues: {result['cues']}")


if __name__ == "__main__":
    main()


"""
MediaPipe Keypoint Extractor
Extracts hand, pose, and face keypoints from camera feed
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Optional
import json

class MediaPipeExtractor:
    """
    Extract keypoints using MediaPipe for assist mode detection
    """
    
    def __init__(self):
        # Initialize MediaPipe solutions
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_face = mp.solutions.face_mesh
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.face = self.mp_face.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
    
    def extract_hand_features(self, image: np.ndarray) -> Dict:
        """
        Extract hand keypoints and features
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            Dictionary of hand features
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)
        
        features = {
            "num_hands": 0,
            "hand_landmarks": [],
            "hand_sign_detected": False,
            "hand_movement_freq": 0.0
        }
        
        if results.multi_hand_landmarks:
            features["num_hands"] = len(results.multi_hand_landmarks)
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract landmark coordinates
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.append({
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z
                    })
                features["hand_landmarks"].append(landmarks)
                
                # Detect signing gestures (simplified heuristic)
                if self._detect_signing_gesture(landmarks):
                    features["hand_sign_detected"] = True
                    features["hand_movement_freq"] += 1.0
        
        return features
    
    def extract_pose_features(self, image: np.ndarray) -> Dict:
        """
        Extract pose keypoints and features
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            Dictionary of pose features
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_image)
        
        features = {
            "pose_detected": False,
            "posture": None,
            "mobility_cues": []
        }
        
        if results.pose_landmarks:
            features["pose_detected"] = True
            
            # Analyze posture
            landmarks = results.pose_landmarks.landmark
            
            # Detect sitting/standing
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
            left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            # Simple heuristic: if hips and ankles are close in Y, likely sitting
            hip_ankle_diff = abs((left_hip.y + right_hip.y) / 2 - (left_ankle.y + right_ankle.y) / 2)
            
            if hip_ankle_diff < 0.2:
                features["posture"] = "seated"
            else:
                features["posture"] = "standing"
            
            # Detect wheelchair/assistive device (simplified)
            # In production, use more sophisticated detection
            features["mobility_cues"] = ["posture_detected"]
        
        return features
    
    def extract_face_features(self, image: np.ndarray) -> Dict:
        """
        Extract face keypoints and gaze features
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            Dictionary of face features
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face.process(rgb_image)
        
        features = {
            "face_detected": False,
            "gaze_pattern": None,
            "eye_openness": None,
            "mouth_movement": False
        }
        
        if results.multi_face_landmarks:
            features["face_detected"] = True
            
            # Extract face landmarks
            face_landmarks = results.multi_face_landmarks[0]
            
            # Analyze eye openness (simplified)
            # In production, use more sophisticated gaze estimation
            features["eye_openness"] = "normal"  # Placeholder
            
            # Analyze mouth movement
            # In production, detect lip motion
            features["mouth_movement"] = False
            
            # Gaze pattern (simplified)
            features["gaze_pattern"] = "normal"  # Placeholder
        
        return features
    
    def extract_all_features(self, image: np.ndarray) -> Dict:
        """
        Extract all features from image
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            Combined features dictionary
        """
        hand_features = self.extract_hand_features(image)
        pose_features = self.extract_pose_features(image)
        face_features = self.extract_face_features(image)
        
        return {
            "hand": hand_features,
            "pose": pose_features,
            "face": face_features,
            "timestamp": None  # Add timestamp if needed
        }
    
    def _detect_signing_gesture(self, landmarks: List[Dict]) -> bool:
        """
        Detect if hand is making signing gesture (simplified heuristic)
        
        Args:
            landmarks: Hand landmark coordinates
        
        Returns:
            True if signing gesture detected
        """
        # Simplified heuristic: check if fingers are extended
        # In production, use more sophisticated gesture recognition
        
        if len(landmarks) < 21:
            return False
        
        # Check thumb extension
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        
        # Check index finger extension
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        
        # Simple heuristic: if fingers are extended, might be signing
        thumb_extended = thumb_tip["x"] > thumb_ip["x"]
        index_extended = index_tip["y"] < index_pip["y"]
        
        return thumb_extended and index_extended
    
    def process_video_stream(self, video_source: int = 0, duration: int = 20):
        """
        Process video stream and extract features
        
        Args:
            video_source: Video source (0 for webcam)
            duration: Duration in seconds
        
        Returns:
            Aggregated features
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            raise ValueError("Could not open video source")
        
        all_features = []
        frame_count = 0
        start_time = cv2.getTickCount()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Extract features from frame
            features = self.extract_all_features(frame)
            all_features.append(features)
            
            frame_count += 1
            
            # Check duration
            elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if elapsed >= duration:
                break
        
        cap.release()
        
        # Aggregate features
        aggregated = self._aggregate_features(all_features)
        return aggregated
    
    def _aggregate_features(self, features_list: List[Dict]) -> Dict:
        """
        Aggregate features from multiple frames
        
        Args:
            features_list: List of feature dictionaries
        
        Returns:
            Aggregated features
        """
        if not features_list:
            return {}
        
        # Aggregate hand features
        hand_sign_freq = sum(
            f["hand"]["hand_movement_freq"] for f in features_list
        ) / len(features_list)
        
        # Aggregate pose features
        postures = [f["pose"]["posture"] for f in features_list if f["pose"]["posture"]]
        most_common_posture = max(set(postures), key=postures.count) if postures else None
        
        # Aggregate face features
        face_detected_count = sum(
            1 for f in features_list if f["face"]["face_detected"]
        )
        face_detection_rate = face_detected_count / len(features_list)
        
        return {
            "handSignFreq": hand_sign_freq,
            "posture": most_common_posture,
            "face_detection_rate": face_detection_rate,
            "total_frames": len(features_list)
        }


def main():
    """Demo: Extract features from webcam"""
    extractor = MediaPipeExtractor()
    
    print("Starting camera feed...")
    print("Press 'q' to quit")
    
    try:
        features = extractor.process_video_stream(duration=5)
        print("\nExtracted Features:")
        print(json.dumps(features, indent=2))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


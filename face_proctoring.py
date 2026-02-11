import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

class FaceProctoring:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, 
            min_detection_confidence=0.5
        )
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.violations = []
    
    def analyze_frame(self, frame):
        """
        Analyze a single frame for proctoring violations
        Returns: dict with violation details
        """
        violations = {
            'multiple_faces': False,
            'no_face': False,
            'looking_away': False,
            'face_count': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        results = self.face_detection.process(rgb_frame)
        
        if results.detections:
            face_count = len(results.detections)
            violations['face_count'] = face_count
            
            # Check for multiple faces
            if face_count > 1:
                violations['multiple_faces'] = True
                violations['severity'] = 'high'
                violations['description'] = f'{face_count} faces detected'
            
            # Analyze face mesh for gaze direction
            mesh_results = self.face_mesh.process(rgb_frame)
            if mesh_results.multi_face_landmarks:
                for face_landmarks in mesh_results.multi_face_landmarks:
                    # Simple gaze detection based on eye landmarks
                    left_eye = face_landmarks.landmark[33]  # Left eye
                    right_eye = face_landmarks.landmark[263]  # Right eye
                    nose = face_landmarks.landmark[1]  # Nose tip
                    
                    # Calculate if looking away (simplified)
                    eye_center_x = (left_eye.x + right_eye.x) / 2
                    deviation = abs(eye_center_x - nose.x)
                    
                    if deviation > 0.05:  # Threshold for looking away
                        violations['looking_away'] = True
                        violations['severity'] = 'medium'
                        violations['description'] = 'Student looking away from screen'
        else:
            violations['no_face'] = True
            violations['severity'] = 'high'
            violations['description'] = 'No face detected'
        
        return violations
    
    def get_violation_summary(self, violations):
        """Generate summary of violations"""
        if violations['multiple_faces']:
            return {
                'type': 'multiple_faces',
                'severity': 'high',
                'message': f"Multiple faces detected: {violations['face_count']}"
            }
        elif violations['no_face']:
            return {
                'type': 'no_face',
                'severity': 'high',
                'message': 'No face detected in frame'
            }
        elif violations['looking_away']:
            return {
                'type': 'looking_away',
                'severity': 'medium',
                'message': 'Student appears to be looking away'
            }
        return None
    
    def __del__(self):
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()

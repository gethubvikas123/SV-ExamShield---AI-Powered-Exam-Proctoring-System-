"""
Simplified Object Detection Module
This version uses a mock detector to avoid dependency issues
For production, you can integrate YOLO when dependencies are resolved
"""

import cv2
import numpy as np

class ObjectDetection:
    def __init__(self):
        """
        Initialize simplified object detector
        This is a placeholder that simulates object detection
        """
        print("Initialized Simplified Object Detection (Mock Mode)")
        print("To enable YOLO detection, fix torch/ultralytics dependencies")
        
        # Define suspicious objects (same as original)
        self.suspicious_objects = {
            'cell phone': 'high',
            'book': 'medium',
            'laptop': 'high',
            'tablet': 'high',
            'mouse': 'low',
            'keyboard': 'low',
            'remote': 'medium',
            'backpack': 'low'
        }
        
        # Mock detection mode
        self.use_mock = True
    
    def detect_objects(self, frame):
        """
        Detect objects in frame
        Currently using mock detection to avoid dependency issues
        
        To enable real YOLO detection:
        1. Fix torch/ultralytics compatibility
        2. Set self.use_mock = False
        3. Uncomment the real YOLO code below
        """
        
        violations = {
            'suspicious_objects': [],
            'severity': 'none',
            'detected_items': []
        }
        
        if self.use_mock:
            # Mock detection - randomly detect objects for demo purposes
            # In production, replace this with actual YOLO detection
            import random
            
            # 10% chance to detect a suspicious object (for demo)
            if random.random() < 0.1:
                mock_objects = ['cell phone', 'book', 'laptop']
                detected = random.choice(mock_objects)
                severity = self.suspicious_objects[detected]
                
                violations['suspicious_objects'].append({
                    'object': detected,
                    'confidence': round(random.uniform(0.5, 0.95), 2),
                    'severity': severity
                })
                
                violations['detected_items'].append(detected)
                violations['severity'] = severity
        
        # REAL YOLO DETECTION CODE (uncomment when dependencies are fixed):
        """
        else:
            results = self.model(frame, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    
                    if class_name in self.suspicious_objects and confidence > 0.5:
                        severity = self.suspicious_objects[class_name]
                        
                        violations['suspicious_objects'].append({
                            'object': class_name,
                            'confidence': confidence,
                            'severity': severity
                        })
                        
                        violations['detected_items'].append(class_name)
                        
                        if severity == 'high':
                            violations['severity'] = 'high'
                        elif severity == 'medium' and violations['severity'] != 'high':
                            violations['severity'] = 'medium'
        """
        
        return violations
    
    def get_violation_message(self, violations):
        """Generate violation message"""
        if violations['suspicious_objects']:
            items = ', '.join(violations['detected_items'])
            return {
                'type': 'suspicious_object',
                'severity': violations['severity'],
                'message': f"Suspicious objects detected: {items}"
            }
        return None


# Instructions to enable real YOLO detection:
"""
TO ENABLE REAL YOLO OBJECT DETECTION:

1. Fix PyTorch/Ultralytics compatibility:
   pip uninstall torch torchvision ultralytics -y
   pip install torch==2.0.1 torchvision==0.15.2
   pip install ultralytics==8.0.200

2. Replace the code in __init__ with:

   def __init__(self):
       from ultralytics import YOLO
       import os
       
       model_path = '../models/yolov8n.pt'
       
       if not os.path.exists(model_path):
           print("Downloading YOLOv8 model...")
           self.model = YOLO('yolov8n.pt')
       else:
           self.model = YOLO(model_path)
       
       self.suspicious_objects = {
           'cell phone': 'high',
           'book': 'medium',
           'laptop': 'high',
           'tablet': 'high',
           'mouse': 'low',
           'keyboard': 'low',
           'remote': 'medium',
           'backpack': 'low'
       }
       
       self.use_mock = False

3. Uncomment the real YOLO detection code in detect_objects method

For now, the system works with mock detection for demonstration.
"""
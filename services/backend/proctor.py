import cv2
import numpy as np
import os

class ProctorEngine:
    def __init__(self):
        """Initialize with OpenCV's Haar Cascade for face detection (more reliable than MediaPipe)"""
        self.face_cascade = None
        self.eye_cascade = None
        
        try:
            # Try to load Haar Cascade classifiers
            cascade_path = cv2.data.haarcascades
            face_cascade_path = os.path.join(cascade_path, 'haarcascade_frontalface_default.xml')
            eye_cascade_path = os.path.join(cascade_path, 'haarcascade_eye.xml')
            glass_cascade_path = os.path.join(cascade_path, 'haarcascade_eye_tree_eyeglasses.xml')
            
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
            self.glass_cascade = cv2.CascadeClassifier(glass_cascade_path)
            
            if self.face_cascade.empty() or self.eye_cascade.empty():
                print("⚠️ Haar Cascade files not found. Proctoring will be limited.")
                self.face_cascade = None
                self.eye_cascade = None
            else:
                print("✅ OpenCV Haar Cascade initialized for behavioral proctoring (Glasses support added).")
        except Exception as e:
            print(f"⚠️ Proctor initialization failed: {e}")
            self.face_cascade = None
            self.eye_cascade = None

    def analyze_behavior(self, video_path: str):
        """
        Analyzes behavioral patterns using OpenCV face/eye detection.
        Detects: face absence, looking away, eye closure patterns.
        """
        if not self.face_cascade:
            return [{
                "timestamp": "00:00", 
                "issue": "Proctoring module disabled (OpenCV Haar Cascade not available)", 
                "severity": "Info"
            }]

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return [{
                    "timestamp": "00:00",
                    "issue": f"Could not open video file: {video_path}",
                    "severity": "Error"
                }]
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps <= 0: 
                fps = 30
            
            frame_count = 0
            flags = []
            consecutive_no_face = 0
            consecutive_no_eyes = 0
            total_samples = 0
            samples_with_faces = 0
            
            # Sample every 2 seconds to balance accuracy and performance
            sample_interval = int(fps * 2)

            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                frame_count += 1
                
                # Skip frames for performance
                if frame_count % sample_interval != 0:
                    continue

                total_samples += 1
                timestamp_sec = frame_count / fps
                timestamp_str = f"{int(timestamp_sec // 60):02d}:{int(timestamp_sec % 60):02d}"

                # Convert to grayscale for detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=5, 
                    minSize=(30, 30)
                )

                if len(faces) > 0:
                    samples_with_faces += 1

                if len(faces) == 0:
                    consecutive_no_face += 1
                    consecutive_no_eyes = 0
                    
                if len(faces) == 0:
                    consecutive_no_face += 1
                    consecutive_no_eyes = 0
                    
                    # Flag if face is missing for more than 3 consecutive samples (6+ seconds)
                    # Increased threshold slightly to prevent noise but still catch absences
                    if consecutive_no_face >= 3:
                        flags.append({
                            "timestamp": timestamp_str,
                            "issue": "Candidate face not visible (Webcam obscured or away)",
                            "severity": "High"
                        })
                        consecutive_no_face = 0
                else:
                    consecutive_no_face = 0
                    
                    # Check for eyes within detected face
                    for (x, y, w, h) in faces:
                        roi_gray = gray[y:y+h, x:x+w]
                        
                        # Use more sensitive scaleFactor for small eyes in PiP
                        eyes = self.eye_cascade.detectMultiScale(
                            roi_gray, 
                            scaleFactor=1.05, 
                            minNeighbors=4,    
                            minSize=(15, 15)
                        )
                        
                        # Fallback for eyeglasses
                        if len(eyes) == 0 and self.glass_cascade is not None:
                            eyes = self.glass_cascade.detectMultiScale(
                                roi_gray,
                                scaleFactor=1.05,
                                minNeighbors=3,
                                minSize=(15, 15)
                            )
                        
                        # Detection Logic: Flag if eyes/glasses are missing for multiple samples
                        # Removed the >100px restriction to support smaller webcam windows
                        if len(eyes) == 0:
                            consecutive_no_eyes += 1
                            if consecutive_no_eyes >= 3:
                                flags.append({
                                    "timestamp": timestamp_str,
                                    "issue": "Suspected Gaze Aversion (Looking away from screen)",
                                    "severity": "Medium"
                                })
                                consecutive_no_eyes = 0
                        else:
                            consecutive_no_eyes = 0

            cap.release()
            
            # Check if this is a screen recording (no faces detected at all)
            if total_samples > 0 and samples_with_faces == 0:
                return [{
                    "timestamp": "00:00",
                    "issue": "Screen-only recording detected - No webcam/face visible. Behavioral proctoring not applicable.",
                    "severity": "Info"
                }]
            
            if not flags:
                flags.append({
                    "timestamp": "00:00",
                    "issue": "No behavioral anomalies detected",
                    "severity": "Info"
                })
            
            return flags
            
        except Exception as e:
            print(f"❌ Proctoring analysis failed: {e}")
            return [{
                "timestamp": "00:00",
                "issue": f"Analysis error: {str(e)}",
                "severity": "Error"
            }]

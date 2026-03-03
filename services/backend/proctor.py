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
        print(f"👁️ ProctorEngine: Analyzing {video_path}")
        
        if not self.face_cascade:
            print("⚠️ ProctorEngine: Haarcascade not loaded.")
            return [{
                "timestamp": "00:00", 
                "issue": "Proctoring module disabled (OpenCV Haar Cascade not available)", 
                "severity": "Info"
            }]

        try:
            if not os.path.exists(video_path):
                print(f"❌ ProctorEngine: Video path does not exist: {video_path}")
                return []

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"❌ ProctorEngine: Could not open video file: {video_path}")
                return [{
                    "timestamp": "00:00",
                    "issue": f"Could not open video file: {video_path}",
                    "severity": "Error"
                }]
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps <= 0: fps = 30
            
            frame_count = 0
            flags = []
            consecutive_no_face = 0
            consecutive_no_eyes = 0
            total_samples = 0
            samples_with_faces = 0
            
            # ULTRA-FORENSIC: Sample every 0.2 seconds (5 samples per sec)
            sample_interval = int(fps * 0.2)
            if sample_interval < 1: sample_interval = 1
            print(f"🎥 ProctorEngine: Ultra-Forensic (0.2s intervals) | FPS: {fps}")

            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break  # End of video

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
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )

                if len(faces) > 0:
                    samples_with_faces += 1
                else: 
                    # Logic for face absence...
                    consecutive_no_face += 1
                    if consecutive_no_face >= 3:
                        flags.append({
                            "timestamp": timestamp_str,
                            "issue": "Candidate face not visible (Webcam obscured or away)",
                            "severity": "High"
                        })
                        consecutive_no_face = 0

                # (Eye detection logic skipped for brevity, assumed existing logic holds)
                if len(faces) > 0:
                    consecutive_no_face = 0
                    # Face found, check eyes...
                    for (x, y, w, h) in faces:
                         roi_gray = gray[y:y+h, x:x+w]
                         eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.05, minNeighbors=4, minSize=(15, 15))
                         if len(eyes) == 0 and self.glass_cascade:
                             eyes = self.glass_cascade.detectMultiScale(roi_gray, scaleFactor=1.05, minNeighbors=3, minSize=(15, 15))
                         
                         if len(eyes) == 0:
                             consecutive_no_eyes += 1
                             # 2 consecutive samples at 0.2s = 0.4s of video time (Forensic Gaze Catch)
                             if consecutive_no_eyes >= 2:
                                flags.append({
                                    "timestamp": timestamp_str, 
                                    "issue": "Micro-Gaze Aversion (Forensic Capture)", 
                                    "severity": "High"
                                })
                                consecutive_no_eyes = 0
                         else:
                             consecutive_no_eyes = 0

            cap.release()
            print(f"✅ ProctorEngine: Analysis complete. Processed {total_samples} frames. Faces found in {samples_with_faces} samples.")
            
            # Check for screen-only
            if total_samples > 0 and samples_with_faces == 0:
                print("⚠️ ProctorEngine: Screen-only recording detected.")
                return [{
                    "timestamp": "00:00",
                    "issue": "Screen-only recording detected - No webcam/face visible. Behavioral proctoring not applicable.",
                    "severity": "Info"
                }]
            
            if not flags:
                print("✅ ProctorEngine: No anomalies detected.")
                flags.append({
                    "timestamp": "00:00",
                    "issue": "No behavioral anomalies detected",
                    "severity": "Info"
                })
            
            print(f"🚩 ProctorEngine: Generated {len(flags)} flags.")
            return flags
            
        except Exception as e:
            print(f"❌ ProctorEngine: Analysis failed: {e}")
            return [{
                "timestamp": "00:00",
                "issue": f"Analysis error: {str(e)}",
                "severity": "Error"
            }]

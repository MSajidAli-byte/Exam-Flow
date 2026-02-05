import mediapipe as mp
print(f"MediaPipe version: {mp.__version__}")
try:
    print(f"Solutions: {mp.solutions}")
    print("Success")
except AttributeError as e:
    print(f"Error: {e}")
    print(f"Dir(mp): {dir(mp)}")

import os
import mediapipe
path = os.path.join(mediapipe.__path__[0], "tasks")
print(f"Listing files in {path}:")
for root, dirs, files in os.walk(path):
    print(root)

import os
import mediapipe
path = mediapipe.__path__[0]
print(f"Listing files in {path}:")
for item in os.listdir(path):
    print(item)

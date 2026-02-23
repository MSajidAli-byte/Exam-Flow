import os
start_path = r"D:\development\Upwork Projects\Exam-Flow\venv\Lib\site-packages"
for root, dirs, files in os.walk(start_path):
    if "solutions" in dirs:
        print(f"Found solutions in: {root}")

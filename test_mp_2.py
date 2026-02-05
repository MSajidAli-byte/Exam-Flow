try:
    import mediapipe.solutions as solutions
    print("Imported mediapipe.solutions successfully")
    print(f"Dir(solutions): {dir(solutions)}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")

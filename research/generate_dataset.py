import zipfile
import os

def create_solution_package(case_id, video_source, code_content, context_content, output_name):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_name), exist_ok=True)
    
    with zipfile.ZipFile(output_name, 'w') as zipf:
        # Add video
        if os.path.exists(video_source):
            zipf.write(video_source, os.path.basename(video_source))
        
        # Add code
        code_ext = ".java" if "java" in case_id.lower() else ".py"
        zipf.writestr(f"student_submission{code_ext}", code_content)
        
        # Add context (instruction)
        zipf.writestr("context.txt", context_content)

def generate_all_cases():
    base_video = "Java_Demo_Exam-Flow.mp4" # Corrected filename
    cases_dir = "research/cases"
    
    # Case 1: Standard Success (Java)
    create_solution_package(
        "Case1", base_video,
        """
public class Dog extends Animal {
    @Override
    public void makeSound() { System.out.println("Bark"); }
}""",
        "Task: Extend Animal and override makeSound with 'Bark'.",
        f"{cases_dir}/case1_standard_success.zip"
    )

    # Case 2: Semantic Variation (Python Factorial)
    create_solution_package(
        "Case2", base_video,
        """
def compute_factorial(val):
    res = 1
    # Student uses while loop instead of recursion
    while val > 0:
        res *= val
        val -= 1
    return res
""",
        "Task: Implement factorial in Python.",
        f"{cases_dir}/case2_semantic_variation.zip"
    )

    # Case 3: Sudden Logic (Cheating Simulation)
    create_solution_package(
        "Case3", base_video,
        """
# Extremely complex code that appeared instantly
def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 1: return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1: return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1: return False
        return True
    # [Rest of complex N-Queens solver...]
""",
        "Task: Write a simple loop.",
        f"{cases_dir}/case3_sudden_logic.zip"
    )

    # Case 5: Library-Blind (Public Plagiarism)
    create_solution_package(
        "Case5", base_video,
        """
# Identical to a famous GeeksForGeeks solution not in RAG
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
""",
        "Task: Sort an array.",
        f"{cases_dir}/case5_library_blind.zip"
    )

    # Case 4: Gaze Deviation (Distraction)
    create_solution_package(
        "Case4", base_video,
        """
def slow_logic():
    # Simple code produced while student is looking away
    x = 10
    y = 20
    return x + y
""",
        "Task: Add two numbers.",
        f"{cases_dir}/case4_gaze_deviation.zip"
    )

    # Case 6: Keyboard Warrior (Logical Gibberish)
    create_solution_package(
        "Case6", base_video,
        """
def gibberish():
    a = 1
    b = 2
    # Frantic typing but logic is circular or broken
    while a == a:
        a = b
        b = a
        if a == b: break
""",
        "Task: Implement a sorting algorithm.",
        f"{cases_dir}/case6_keyboard_warrior.zip"
    )

    # Case 7: False Positive Trap (Legitimate Thinking)
    create_solution_package(
        "Case7", base_video,
        """
def complex_math(n):
    # Student is slow, pondering, looking around
    if n < 2: return n
    return complex_math(n-1) + complex_math(n-2)
""",
        "Task: Implement Fibonacci.",
        f"{cases_dir}/case7_thinking_pause.zip"
    )

    print("Golden Dataset (ZIP Packages) generated in research/cases/")

if __name__ == "__main__":
    generate_all_cases()

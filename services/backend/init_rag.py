from rag.rag_manager import RagManager
import os

def init_library():
    print("Initialize Ideal Solution Library...")
    rag = RagManager()
    
    # 1. Java OOP
    rag.add_solution(
        solution_id="java_oop_001",
        context="A Java application demonstrating Inheritance, Polymorphism, and Encapsulation.",
        code="""
public class Animal {
    private String name;
    public void makeSound() { System.out.println("Generic sound"); }
}
public class Dog extends Animal {
    @Override
    public void makeSound() { System.out.println("Bark"); }
}
        """,
        metadata={"category": "Java", "difficulty": "Intermediate"}
    )
    
    # 2. Dockerfile Best Practices
    rag.add_solution(
        solution_id="docker_001",
        context="A multi-stage build Dockerfile for a Python application.",
        code="""
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
        """,
        metadata={"category": "Docker", "difficulty": "Advanced"}
    )

    # 3. Python Factorial (Recursive)
    rag.add_solution(
        solution_id="python_fact_001",
        context="Recursive factorial implementation in Python.",
        code="""
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
        """,
        metadata={"category": "Python", "difficulty": "Beginner"}
    )
    
    print("Library initialized successfully.")

if __name__ == "__main__":
    init_library()

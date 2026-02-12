from rag.rag_manager import RagManager
import os

def init_library():
    print("Initialize Ideal Solution Library...")
    rag = RagManager()
    
    # Sample Application: Java OOP
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
    
    # Sample Application: Dockerfile Best Practices
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
    
    print("Library initialized successfully.")

if __name__ == "__main__":
    init_library()

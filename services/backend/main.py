from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Exam-Flow AI Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Exam-Flow Backend is running", "status": "online"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    # Placeholder for video processing logic
    return {"filename": file.filename, "status": "received"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

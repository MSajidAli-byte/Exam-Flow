import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(
    page_title="Exam-Flow | AI Grading & Proctoring",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Exam-Flow AI Assistant")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Assessment")
    uploaded_file = st.file_uploader("Upload Zoom Recording (MP4)", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button("🚀 Start AI Grading"):
            with st.spinner("Analyzing Video & Behavior..."):
                # Placeholder for backend call
                # files = {"file": uploaded_file.getvalue()}
                # response = requests.post(f"{BACKEND_URL}/upload-video", files=files)
                st.success("Analysis Complete! (Mock)")

with col2:
    st.header("📊 AI Insights")
    st.info("Upload a video to see real-time grading and proctoring reports.")
    
    # Mock data for demonstration
    if uploaded_file:
        st.subheader("Behavioral Flags")
        st.error("⚠️ 02:15 - Looking away from screen")
        st.warning("⚠️ 04:30 - Background noise detected")
        
        st.subheader("Technical Grade")
        st.success("✅ Docker configuration: 10/10")
        st.success("✅ Java Error Resolution: 9/10")

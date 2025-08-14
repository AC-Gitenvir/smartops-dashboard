import streamlit as st
from PIL import Image

# Optional: Load a logo
# logo = Image.open("assets/logo.png")  # if you have one

st.set_page_config(page_title="SmartOps AI Dashboard", layout="wide")

# Title Section
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🤖 SmartOps AI Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align: center; color: #FAFAFA;'>Your All-in-One Automation, Cloud & AI Assistant</h4>",
    unsafe_allow_html=True,
)

st.markdown("---")

# Introduction
with st.expander("📢 What is SmartOps?", expanded=True):
    st.write("""
    **SmartOps** is a student-built, AI-powered automation dashboard that merges voice, scripting, and intelligent agents to solve real-world tasks like:
    - Python & Web Automation
    - Voice-controlled Windows/Linux tasks
    - SSH/Docker control
    - File management with Gemini
    - ML Playground and CloudOps (AWS, K8s)

    🛠 Designed for students, developers, and tech enthusiasts.
    """)

st.markdown("### 🔍 Navigate to Modules")

# Dashboard Navigation Cards
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧩 Python Automation"):
        st.switch_page("Python_Tasks.py")
    if st.button("🔐 Linux SSH"):
        st.switch_page("Linux_SSH.py")

with col2:
    if st.button("🐳 Docker Manager"):
        st.switch_page("Docker_SSH.py")
    if st.button("🗃️ Smart File Explorer"):
        st.switch_page("File_Explorer_AI.py")

with col3:
    if st.button("💬 AI Assistant"):
        st.switch_page("AI_Assistant.py")
    if st.button("🤖 ML Zone"):
        st.switch_page("ML_Zone.py")

st.markdown("---")

# Footer
st.markdown(
    "<div style='text-align: center; color: gray;'>© 2025 Ayush Choudhary | SmartOps</div>",
    unsafe_allow_html=True
)

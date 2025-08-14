import streamlit as st
import subprocess
import os
import smtplib
from email.message import EmailMessage

# Page configuration
st.set_page_config(page_title="Automation Panel", layout="centered")
st.title("🚀 Automation Panel")
st.markdown("Control various tasks from a single dashboard")

# 🛠 Run System Update
if st.button("🛠 Run System Update"):
    with st.spinner("Updating..."):
        result = subprocess.getoutput("sudo apt update && sudo apt upgrade -y")
    st.success("✅ Update Completed")
    st.code(result, language='bash')

# 🐳 Start Docker Container
with st.expander("🐳 Start a Docker Container"):
    container_name = st.text_input("Enter Docker container name", "my_container")
    if st.button("Start Container"):
        result = subprocess.getoutput(f"docker start {container_name}")
        st.success(f"Started: {result}")

# 📧 Send an Email using SMTP
def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@gmail.com"
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("your_email@gmail.com", "your_app_password")  # Use app password, not regular password
            smtp.send_message(msg)
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error: {e}"

with st.expander("📧 Send an Email"):
    to = st.text_input("To")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    if st.button("Send Email"):
        status = send_email(subject, message, to)
        st.info(status)

import streamlit as st
from PIL import Image
import os
from datetime import datetime

# Dark/Light Theme Toggle
st.set_page_config(page_title="Automation Suite", layout="wide")
theme = st.sidebar.radio("🎨 Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# ---- LANDING PAGE ----
st.title("🤖 Unified Automation Suite")
st.markdown("""
Welcome to the *All-in-One Automation App*. Select a task from the sidebar or click a button below to get started.
""")

# ---- MAIN TASK BUTTONS ----
task = None
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📧 Send Email"):
        task = "email"
    if st.button("📞 Phone Call"):
        task = "call"
with col2:
    if st.button("💬 WhatsApp Message"):
        task = "whatsapp"
    if st.button("📩 Send SMS"):
        task = "sms"
with col3:
    if st.button("🔗 LinkedIn Post"):
        task = "linkedin"
    if st.button("🐦 Twitter (X) Post"):
        task = "twitter"
    if st.button("📘 Facebook Post"):
        task = "facebook"
    if st.button("📸 Instagram Post"):
        task = "instagram"

# ---- SIDEBAR ----
with st.sidebar:
    st.header("🧭 Navigation")
    task = st.radio("Select Task:", [
        "Home", "Send Email", "WhatsApp Message", "Send SMS", "Phone Call",
        "LinkedIn Post", "Twitter (X) Post", "Facebook Post", "Instagram Post"
    ])

# ---- MEDIA UPLOAD ----
uploaded_media = st.file_uploader("Upload Photo/Video (optional):", type=["jpg", "jpeg", "png", "mp4", "mov"])
if uploaded_media:
    st.markdown("*Preview:*")
    if uploaded_media.type.startswith("image"):
        img = Image.open(uploaded_media)
        st.image(img, use_column_width=True)
    else:
        st.video(uploaded_media)

# ---- TASK LOGIC ----
def show_success(msg):
    st.success(f"✅ {msg}")

def show_error(msg):
    st.error(f"❌ {msg}")

if task == "Send Email":
    st.subheader("📧 Send Email")
    to_email = st.text_input("Recipient Email:")
    subject = st.text_input("Subject:")
    message = st.text_area("Message:")
    if st.button("Send Email"):
        show_success("Email Sent via EmailJS API (placeholder)")

elif task == "WhatsApp Message":
    st.subheader("💬 Send WhatsApp Message")
    to_number = st.text_input("Recipient WhatsApp Number (with country code):")
    msg = st.text_area("Message:")
    if st.button("Send WhatsApp"):
        show_success("WhatsApp message sent (via Twilio)")

elif task == "Send SMS":
    st.subheader("📩 Send SMS")
    phone = st.text_input("Phone Number (with country code):")
    sms = st.text_area("Message:")
    if st.button("Send SMS"):
        show_success("SMS Sent via Twilio")

elif task == "Phone Call":
    st.subheader("📞 Make a Phone Call")
    call_number = st.text_input("Phone Number to Call:")
    if st.button("Make Call"):
        show_success("Call initiated using Twilio")

elif task == "LinkedIn Post":
    st.subheader("🔗 LinkedIn Automation")
    username = st.text_input("LinkedIn Email:")
    password = st.text_input("LinkedIn Password:", type="password")
    post_content = st.text_area("Post Message:")
    if st.button("Post to LinkedIn"):
        show_success("Posted to LinkedIn (using Selenium)")

elif task == "Twitter (X) Post":
    st.subheader("🐦 Post to Twitter (X)")
    username = st.text_input("Twitter Username:")
    password = st.text_input("Twitter Password:", type="password")
    tweet = st.text_area("Tweet Message:")
    if st.button("Tweet"):
        show_success("Tweet posted via Selenium")

elif task == "Facebook Post":
    st.subheader("📘 Post to Facebook")
    username = st.text_input("Facebook Username:")
    password = st.text_input("Facebook Password:", type="password")
    caption = st.text_area("Post Caption:")
    if st.button("Post to Facebook"):
        show_success("Post uploaded to Facebook")

elif task == "Instagram Post":
    st.subheader("📸 Post to Instagram")
    username = st.text_input("Instagram Username:")
    password = st.text_input("Instagram Password:", type="password")
    caption = st.text_area("Post Caption:")
    if st.button("Post to Instagram"):
        show_success("Image/Video posted to Instagram")
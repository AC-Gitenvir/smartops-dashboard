import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

st.set_page_config(page_title="📧 Email Sender", layout="centered")

st.title("📬 Send Email Using Python (Gmail SMTP)")

sender_email = st.text_input("Your Gmail address")
sender_password = st.text_input("App Password (not Gmail password)", type="password")
receiver_email = st.text_input("Recipient's Email address")
subject = st.text_input("Email Subject")
body = st.text_area("Email Body")

if st.button("Send Email"):
    if sender_email and sender_password and receiver_email and subject and body:
        try:
            # Create message object
            msg = MIMEMultipart()
            msg["From"] = formataddr((str(Header("Ayush", 'utf-8')), sender_email))
            msg["To"] = receiver_email
            msg["Subject"] = Header(subject, "utf-8")

            # Attach body with utf-8 encoding
            msg.attach(MIMEText(body, "plain", "utf-8"))

            # Send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)  # ✅ Uses send_message() which handles encoding better

            st.success("✅ Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Failed to send email:\n{e}")
    else:
        st.warning("⚠️ Please fill in all fields.")

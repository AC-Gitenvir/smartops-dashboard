# pages/5_twilio_sms.py

import streamlit as st
from twilio.rest import Client

st.title("📨 Twilio SMS Automation")

# --- Load Credentials Securely ---
try:
    account_sid = st.secrets["twilio_credentials"]["account_sid"]
    auth_token = st.secrets["twilio_credentials"]["auth_token"]
    twilio_phone_number = st.secrets["twilio_credentials"]["twilio_phone_number"]
except KeyError:
    st.error("Twilio credentials not found! Please add them to your secrets.toml file.")
    st.stop()

# --- User Input ---
st.subheader("Enter SMS Details")
recipient_number = st.text_input("Recipient's Phone Number", "+91")
sms_message = st.text_area("Message to send", "Hello from the SmartOps Dashboard!")

if st.button("Send SMS", use_container_width=True):
    if not recipient_number or not sms_message:
        st.warning("Please provide both a recipient number and a message.")
    else:
        try:
            with st.spinner("Sending SMS..."):
                client = Client(account_sid, auth_token)
                
                message = client.messages.create(
                    body=sms_message,
                    from_=twilio_phone_number,
                    to=recipient_number
                )
                
            st.success(f"SMS sent successfully! Message SID: {message.sid}")
        except Exception as e:
            st.error(f"Failed to send SMS: {e}")
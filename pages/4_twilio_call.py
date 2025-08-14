# pages/4_twilio_call.py

import streamlit as st
from twilio.rest import Client

st.title("📞 Twilio Voice Call Automation")

# --- Load Credentials Securely ---
try:
    account_sid = st.secrets["twilio_credentials"]["account_sid"]
    auth_token = st.secrets["twilio_credentials"]["auth_token"]
    twilio_phone_number = st.secrets["twilio_credentials"]["twilio_phone_number"]
except KeyError:
    st.error("Twilio credentials not found! Please add them to your secrets.toml file.")
    st.stop()

# --- User Input ---
st.subheader("Enter Call Details")
recipient_number = st.text_input("Recipient's Phone Number", "+91")
call_message = st.text_area("Message to be spoken", "Hello! This is an automated call from the SmartOps Dashboard.")

if st.button("Make the Call", use_container_width=True):
    if not recipient_number or not call_message:
        st.warning("Please provide both a recipient number and a message.")
    else:
        try:
            with st.spinner("Initiating call..."):
                client = Client(account_sid, auth_token)
                
                call = client.calls.create(
                    twiml=f'<Response><Say>{call_message}</Say></Response>',
                    to=recipient_number,
                    from_=twilio_phone_number
                )
                
            st.success(f"Call initiated successfully! Call SID: {call.sid}")
        except Exception as e:
            st.error(f"Failed to make the call: {e}")
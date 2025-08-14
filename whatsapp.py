import streamlit as st
import pywhatkit as kit
import datetime
import time

st.set_page_config(page_title="📲 WhatsApp Automation", layout="centered")
st.title("📱 WhatsApp Message Sender")

option = st.radio("Choose Action:", ["Send Message", "Send Image (Experimental)", "Schedule Message"])

phone = st.text_input("📞 Enter Phone Number (with country code)", value="+91")

if option == "Send Message":
    message = st.text_area("💬 Enter Message")
    if st.button("Send Now"):
        try:
            kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10, tab_close=True)
            st.success("✅ Message sent successfully.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

elif option == "Send Image (Experimental)":
    image_path = st.text_input("🖼 Enter full image path (e.g. C:\\Users\\User\\Desktop\\image.jpg)")
    caption = st.text_input("📝 Image Caption")
    if st.button("Send Image"):
        try:
            kit.sendwhats_image(receiver=phone, img_path=image_path, caption=caption, wait_time=15, tab_close=True)
            st.success("✅ Image sent successfully.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

elif option == "Schedule Message":
    message = st.text_area("💬 Enter Message to Schedule")
    hour = st.number_input("⏰ Hour (24-hour format)", min_value=0, max_value=23, step=1)
    minute = st.number_input("🕒 Minute", min_value=0, max_value=59, step=1)
    if st.button("Schedule"):
        try:
            kit.sendwhatmsg(phone_no=phone, message=message, time_hour=int(hour), time_min=int(minute))
            st.success(f"📨 Scheduled for {hour:02}:{minute:02}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

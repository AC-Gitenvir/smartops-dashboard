import streamlit as st
import os
from openai import OpenAI

# Set page title
st.set_page_config(page_title="🧘 CalmPulse: Your Mental Peace Companion")

st.title("🧘 CalmPulse: Your Mental Peace Companion")
st.write("A safe space to share your thoughts and get calming advice 💬")

# --- SECURELY LOAD API KEY ---
try:
    # This securely loads the key from your .streamlit/secrets.toml file
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Google API Key not found! Please check your .streamlit/secrets.toml file.")
    st.stop()

# This is a placeholder and may not be needed if your setup is standard
base_url = "https://generativelanguage.googleapis.com/v1beta/openai"

# Initialize API client
try:
    gemini_model = OpenAI(api_key=api_key, base_url=base_url)
except Exception as e:
    st.error(f"Failed to initialize the AI model. Please check your API key and base URL. Error: {e}")
    st.stop()


# Core function
def calmpulsellm(myprompt):
    mymsg = [
        {"role": "system", "content": "you are AI assistant work like a mental health peace & give motivation , reply in 3 lines"},
        {"role": "user", "content": myprompt}
    ]
    response = gemini_model.chat.completions.create(model="gemini-2.5-flash", messages=mymsg)
    return response.choices[0].message.content

# Input from user
user_input = st.text_area("💭 How are you feeling today?", height=150)

if st.button("🧘 Get Supportive Advice"):
    if user_input.strip() != "":
        with st.spinner("Sending calm vibes..."):
            try:
                response = calmpulsellm(user_input)
                st.success("Here's a calming message for you:")
                st.write(f"💬 *{response}*")
            except Exception as e:
                st.error(f"An error occurred while getting advice: {e}")
    else:
        st.warning("Please type something so I can help you.")
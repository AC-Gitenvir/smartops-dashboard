# main.py (The Definitive, Perfected Final Version)

import streamlit as st
import base64
from pathlib import Path

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SmartOps Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PATHS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
background_image_file = current_dir / "static" / "background.png"
sidebar_image_file = current_dir / "static" / "sidebar_icon.png"
profile_pic_file = current_dir / "static" / "profile_pic.jpg"

# --- IMAGE ENCODING ---
def get_image_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

background_image_base64 = get_image_as_base64(background_image_file)

# --- INITIALIZE SESSION STATE FOR MODAL ---
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

# --- STYLING ---
# Part 1: Inject all the static CSS.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    @keyframes backgroundPan {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }

    :root {
        --accent-color: #00d4ff;
        --border-color: rgba(255, 255, 255, 0.2);
    }
    
    body { font-family: 'Poppins', sans-serif; }

    [data-testid="stSidebar"] { width: 350px !important; }

    /* Styling for Sidebar Icon */
    [data-testid="stSidebar"] div[data-testid="stImage"] {
        text-align: center; /* Center the container */
    }
    [data-testid="stSidebar"] div[data-testid="stImage"] img {
        max-width: 220px; /* Adjust this value for size */
        margin-bottom: 1rem;
    }

    .stApp {
        background-size: 120%;
        background-position: center;
        background-attachment: fixed;
        animation: backgroundPan 45s linear infinite alternate;
    }
    [data-testid="stSidebar"] {
        background-size: cover;
        background-position: center;
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebarUserContent"] { padding: 1rem; }
    [data-testid="stSidebarNav"] > ul { display: none; }

    /* Main Welcome Page Styles */
    .welcome-container {
        display: flex; flex-direction: column; justify-content: center;
        align-items: center; height: 80vh; text-align: center;
    }
    .welcome-title {
        font-size: 4rem; font-weight: 700; color: #FFFFFF;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.7); margin-bottom: 1rem;
    }
    .profile-details {
        font-size: 1.25rem; color: #e0e0e0; line-height: 1.6;
    }
    .profile-details strong { color: var(--accent-color); font-weight: 600; }

    /* Sidebar Expander Menu Styles */
    [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border-color); border-radius: 10px; margin-bottom: 1rem;
    }
    [data-testid="stExpander"] summary {
        font-size: 1.1rem; font-weight: 600; color: var(--accent-color);
    }
    
    /* Styling for the Profile Picture in the Dialog */
    div[data-testid="stDialog"] div[data-testid="stImage"] {
        margin: 0 auto;
        width: fit-content;
    }
    div[data-testid="stDialog"] div[data-testid="stImage"] img {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 3px solid var(--accent-color);
        object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

# Part 2: Inject ONLY the dynamic CSS that needs the Base64 variable.
if background_image_base64:
    st.markdown(f"""
    <style>
        .stApp, [data-testid="stSidebar"] {{
            background-image:
                linear-gradient(rgba(10, 10, 26, 0.8), rgba(10, 10, 26, 0.9)),
                url("data:image/png;base64,{background_image_base64}");
        }}
    </style>
    """, unsafe_allow_html=True)

# --- PROFILE ICON BUTTON (Top Right) ---
_, col_btn = st.columns([0.9, 0.1])
with col_btn:
    if st.button("👤", use_container_width=True, help="View Profile"):
        st.session_state.show_profile = True

# --- PROFILE DIALOG (Pop-up) ---
if st.session_state.show_profile:
    @st.dialog("My Profile")
    def show_profile_modal():
        if profile_pic_file.exists():
            st.image(str(profile_pic_file))
        st.markdown("<h2 style='text-align: center; color: var(--accent-color);'>Ayush Choudhary</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>AI Engineer</strong></p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>ayush.choudhary9460@gmail.com</p>", unsafe_allow_html=True)
        
        if st.button("Go Back", use_container_width=True):
            st.session_state.show_profile = False
            st.rerun()

    show_profile_modal()

# --- HOMEPAGE CONTENT ---
st.markdown("""
<div class="welcome-container">
    <div class="welcome-title">Welcome to SmartOps</div>
    <div class="profile-details">
        A project by<br>
        <strong>Ayush Choudhary</strong><br>
        Exploring AI and Automation
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR WITH WORKING COLLAPSIBLE MENUS ---
with st.sidebar:
    if sidebar_image_file.exists():
        st.image(str(sidebar_image_file))
    
    st.markdown("<h2 style='text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
    st.divider()

    with st.expander("🤖 AI Projects", expanded=True):
        st.page_link("pages/9_calmpulse_companion.py", label="CalmPulse Companion", icon="🧠")
        st.page_link("pages/10_system_info_ai.py", label="System Info via AI", icon="💻")
        st.page_link("pages/14_game_predicter.py", label="Game Predictor", icon="🎮")

    with st.expander("🐍 Python & Automation"):
        st.page_link("pages/1_whatsapp_automation.py", label="WhatsApp Automation", icon="💬")
        st.page_link("pages/2_social_media_posting.py", label="Social Media Posting", icon="🌐")
        st.page_link("pages/3_linkedin_autoconnect.py", label="LinkedIn Autoconnect", icon="🔗")
        st.page_link("pages/4_twilio_call.py", label="Twilio Call", icon="📞")
        st.page_link("pages/5_twilio_sms.py", label="Twilio SMS", icon="📨")
        st.page_link("pages/7_email_sender.py", label="Email Sender", icon="📧")
        st.page_link("pages/12_digital_image.py", label="Image Steganography", icon="🖼️")
        st.page_link("pages/13_web_scrap.py", label="Web Scraper", icon="🕸️")

    with st.expander("⚙️ Infrastructure"):
        st.page_link("pages/11_SSH_Remote_Execution.py", label="SSH Remote Execution", icon="📡")
        st.page_link("pages/15_windows_kubernetes_manager.py", label="Kubernetes Manager", icon="☸️")
        st.page_link("pages/16_jenkins_manager.py", label="Jenkins Manager", icon="🚀")
        st.page_link("pages/17_monitoring_dashboard.py", label="System Monitoring", icon="📈")
        
    with st.expander("🌐 Web & JS Tools"):
        st.page_link("pages/8_html_js_tools.py", label="HTML/JS Tools", icon="⚙️")
    
    st.divider()
    st.markdown("<h3 style='text-align: center;'>Socials</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("👤 Portfolio", "https://your-portfolio-link.netlify.app", use_container_width=True)
    with col2:
        st.link_button("💼 Ayush's LinkedIn", "https://www.linkedin.com/in/ayush-choudhary-338378286/", use_container_width=True)

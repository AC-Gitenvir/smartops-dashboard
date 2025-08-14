import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Website Downloader",
    page_icon="🌐",
    layout="centered"
)


# --- App Title and UI ---
st.title("🌐 Website Downloader (JS Supported)")
st.write(
    "Enter a URL to open it with Selenium. This app will fetch the page's HTML source, "
    "which you can then download."
)

url_input = st.text_input(
    "Enter Website URL",
    placeholder="https://www.google.com"
)


# --- Button and Logic ---
if st.button("Fetch Website"):
    # 1. Validate the user input
    if not url_input or not url_input.startswith("http"):
        st.error("Please enter a valid URL beginning with 'http' or 'https'.")
    else:
        driver = None  # Initialize driver to None to ensure it's defined
        try:
            # 2. Show a spinner while setting up the driver
            with st.spinner("Initializing browser... This may take a moment."):
                
                # --- This is the key fix ---
                # It automatically finds your Chrome version and downloads the correct driver.
                service = ChromeService(ChromeDriverManager().install())
                
                # You can add options, e.g., to run headless (without opening a visible browser window)
                # options = webdriver.ChromeOptions()
                # options.add_argument("--headless") 
                # driver = webdriver.Chrome(service=service, options=options)
                
                # For local testing, running with a visible browser is fine.
                driver = webdriver.Chrome(service=service)
                # -------------------------

            # 3. Open the website
            with st.spinner(f"Loading {url_input}..."):
                driver.get(url_input)
                # Wait a few seconds for JavaScript content to potentially load
                time.sleep(3)

            # 4. "Download" Logic: Get the page source and title
            st.success("Website loaded successfully!")
            page_title = driver.title
            page_source = driver.page_source

            st.subheader(f"Page Title: {page_title}")

            # Provide a download button for the full HTML source code
            st.download_button(
                label="⬇️ Download Page Source (HTML)",
                data=page_source,
                file_name=f"{page_title.replace(' ', '_').lower()}_source.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info(
                "This could be due to a network issue, a firewall, or the website "
                "blocking automated requests. Please try another URL."
            )

        finally:
            # 5. This 'finally' block ensures the browser is always closed properly
            if driver:
                driver.quit()
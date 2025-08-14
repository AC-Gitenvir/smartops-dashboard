import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def login_and_comment(platform, username, password, post_url, comment):
    options = Options()
    options.add_argument("--headless")  # remove this line if you want browser visible
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        if platform == "Instagram":
            driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(5)
            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)
            time.sleep(7)
            driver.get(post_url)
            time.sleep(5)
            comment_box = driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
            comment_box.click()
            comment_box.send_keys(comment)
            comment_box.send_keys(Keys.ENTER)

        elif platform == "Facebook":
            driver.get("https://www.facebook.com/")
            time.sleep(5)
            driver.find_element(By.ID, "email").send_keys(username)
            driver.find_element(By.ID, "pass").send_keys(password + Keys.ENTER)
            time.sleep(7)
            driver.get(post_url)
            time.sleep(6)
            comment_area = driver.find_element(By.XPATH, "//div[@aria-label='Write a comment']")
            comment_area.click()
            comment_area.send_keys(comment)
            comment_area.send_keys(Keys.ENTER)

        elif platform == "Twitter":
            driver.get("https://twitter.com/login")
            time.sleep(5)
            driver.find_element(By.NAME, "text").send_keys(username + Keys.ENTER)
            time.sleep(3)
            driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)
            time.sleep(7)
            driver.get(post_url)
            time.sleep(5)
            reply_btn = driver.find_element(By.XPATH, "//div[@data-testid='reply']")
            reply_btn.click()
            time.sleep(3)
            comment_box = driver.find_element(By.XPATH, "//div[@data-testid='tweetTextarea_0']")
            comment_box.send_keys(comment)
            driver.find_element(By.XPATH, "//div[@data-testid='tweetButton']").click()
        else:
            st.error("Unsupported platform selected.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        time.sleep(10)
        driver.quit()

# 🌐 Streamlit UI
st.title("Social Media Auto Comment Bot")

with st.form("comment_form"):
    platform = st.selectbox("Choose Platform", ["Instagram", "Facebook", "Twitter"])
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    post_url = st.text_input("Enter Post URL")
    comment = st.text_area("Enter Comment")
    submitted = st.form_submit_button("Post Comment")

    if submitted:
        st.info("⏳ Working... Please wait.")
        login_and_comment(platform, username, password, post_url, comment)
        st.success("✅ Task Completed")

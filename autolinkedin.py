import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import ipywidgets as widgets
from IPython.display import display, clear_output

# --- UI Widgets ---
email = widgets.Text(
    description="Email:",
    placeholder="Enter LinkedIn email",
    layout=widgets.Layout(width='400px')
)

password = widgets.Password(
    description="Password:",
    placeholder="Enter LinkedIn password",
    layout=widgets.Layout(width='400px')
)

post_url = widgets.Text(
    description="Post URL:",
    placeholder="https://www.linkedin.com/feed/update/...",
    layout=widgets.Layout(width='600px')
)

comment_text = widgets.Textarea(
    description="Comment:",
    placeholder="Type your comment here...",
    layout=widgets.Layout(width='600px', height='100px')
)

submit_btn = widgets.Button(
    description="Post Comment on LinkedIn",
    button_style='success'
)

output = widgets.Output()

# --- Display All Together ---
form = widgets.VBox([email, password, post_url, comment_text, submit_btn, output])
display(form)

# --- Automation Logic ---
def post_linkedin_comment(btn):
    output.clear_output()
    with output:
        try:
            print("🚀 Launching browser...")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get("https://www.linkedin.com/login")
            time.sleep(3)

            # Log in
            driver.find_element(By.ID, "username").send_keys(email.value)
            driver.find_element(By.ID, "password").send_keys(password.value)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(5)

            # Go to post URL
            driver.get(post_url.value)
            time.sleep(6)

            # Scroll to load comment section
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(3)

            # Click "Comment" button
            try:
                comment_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Comment')]")
                comment_button.click()
                time.sleep(3)
            except:
                print("⚠ Comment button not found. Trying to continue.")

            # Find comment box and type
            comment_box = driver.find_element(By.XPATH, "//div[contains(@class, 'comments-comment-box__editor')]")
            comment_box.click()
            comment_box.send_keys(comment_text.value + Keys.RETURN)
            time.sleep(3)
            print("✅ Comment posted successfully!")

            driver.quit()
        except Exception as e:
            print("❌ Failed:", e)

# --- Bind Button ---
submit_btn.on_click(post_linkedin_comment)
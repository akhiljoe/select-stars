# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # --- Update with your LinkedIn credentials ---
# LINKEDIN_EMAIL = "c.joe.akhil@gmail.com"
# LINKEDIN_PASSWORD = "yhHE-b*f@sK6JbV"

# # Launch Chrome
# driver = webdriver.Chrome()

# # Step 1: Open LinkedIn login
# driver.get("https://www.linkedin.com/login")

# # Step 2: Fill username & password
# username = driver.find_element(By.ID, "username")
# password = driver.find_element(By.ID, "password")

# username.send_keys(LINKEDIN_EMAIL)
# password.send_keys(LINKEDIN_PASSWORD)

# driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# # Step 3: Go to the LinkedIn post
# post_url = "https://www.linkedin.com/posts/im-nsk_sql-activity-7328260280931557376-kZFS"
# driver.get(post_url)

# # Step 4: Wait for the post content to load
# try:
#     post_content = WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "div.update-components-text, div.break-words"))
#     ).text

#     print("\n✅ Post content:\n", post_content)

# except Exception as e:
#     print("❌ Could not find post content:", e)

# # Optional: Keep browser open for inspection
# input("\nPress Enter to quit...")
# driver.quit()
import ast

with open("expanded.json", "r", encoding="utf-8") as f:
    urls = ast.literal_eval(f.read())

LINKEDIN_EMAIL = "c.joe.akhil@gmail.com"
LINKEDIN_PASSWORD = "yhHE-b*f@sK6JbV"

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --------------------------
# CONFIG
# --------------------------


output_dir = "linkedin_posts"
os.makedirs(output_dir, exist_ok=True)

# --------------------------
# SELENIUM SETUP
# --------------------------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --------------------------
# LOGIN
# --------------------------
driver.get("https://www.linkedin.com/login")
time.sleep(2)

driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(3)

# --------------------------
# PROCESS EACH POST
# --------------------------
for url in urls:
    driver.get(url)
    time.sleep(5)

    post_id = url.split("/")[-1]
    post_dir = os.path.join(output_dir, post_id)
    os.makedirs(post_dir, exist_ok=True)

    # Extract post text (this CSS selector targets post body only)
    try:
        content_elem = driver.find_element(By.CSS_SELECTOR, "div.update-components-text")
        content = content_elem.text

        # Remove unwanted lines
        lines = content.splitlines()
        cleaned_lines = [
            line for line in lines
            if not line.startswith("Get the interview call:") 
            and not line.startswith("Join the community:")
            and not line.startswith("❣️Love it?")
            and not line.startswith("𝐒𝐜𝐡𝐞𝐝𝐮𝐥𝐞 𝐚 1:1 𝐜𝐚𝐥𝐥 𝐟𝐨𝐫 𝐆𝐮𝐢𝐝𝐚𝐧𝐜𝐞/𝐌𝐞𝐧𝐭𝐨𝐫𝐬𝐡𝐢𝐩")
        ]
        content = "\n".join(cleaned_lines)

        with open(os.path.join(post_dir, "content.txt"), "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Saved content for {url}")
    except Exception as e:
        print(f"❌ Could not extract text for {url}: {e}")

    # Extract post images (only inside the post body, not icons)
    try:
        image_elems = driver.find_elements(By.CSS_SELECTOR, "div.update-components-image img")
        for i, img in enumerate(image_elems, start=1):
            img_url = img.get_attribute("src")
            if img_url:
                img_data = requests.get(img_url).content
                with open(os.path.join(post_dir, f"image_{i}.jpg"), "wb") as f:
                    f.write(img_data)
        print(f"✅ Saved {len(image_elems)} images for {url}")
    except Exception as e:
        print(f"❌ Could not extract images for {url}: {e}")

driver.quit()

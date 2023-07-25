"""
This script uses requests and OpenAI to scrape the web & find relevant job postings.
"""


import os
import time

# from bs4 import BeautifulSoup
from selenium import webdriver
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
URL = "https://bymason.com/careers/"


driver = webdriver.Chrome()
# driver.maximize_window()
driver.get(URL)

time.sleep(1)
content = driver.page_source.encode("utf-8").strip()
while "BizOps" not in str(content):
    print("Trying...")
    time.sleep(1)
    content = driver.page_source.encode("utf-8").strip()

print(content)

driver.quit()

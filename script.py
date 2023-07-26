"""
This script uses requests and OpenAI to scrape the web & find relevant job postings.
"""


import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import openai

from board_page import BoardPage


openai.api_key = os.getenv("OPENAI_API_KEY")
URL = "https://bymason.com/careers/"


# page = requests.get(url)
# print(page.text)

req = Request(url=URL, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(req) as f:
    page = f.read().decode("utf-8")

soup = BeautifulSoup(page, "html.parser")

# Create a new BoardPage
board_page = BoardPage(soup, URL)
print(board_page.get_page_soup().prettify())
print(board_page.get_url())
print(board_page.get_ats_base_url())

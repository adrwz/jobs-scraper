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
ROLE_KEYWORDS = [
    # Ops
    "BizOps",
    "Operations",
    "Chief of Staff",
    "Business",
    "Strategy",
    # Marketing
    "Marketing",
    "Growth",
    "Community",
    # Sales
    "Sales",
]


# page = requests.get(url)
# print(page.text)

req = Request(url=URL, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(req) as f:
    page = f.read().decode("utf-8")

soup = BeautifulSoup(page, "html.parser")

# Create a new BoardPage
board_page = BoardPage(soup, URL)
print(board_page.scrape_all_relevant_roles(ROLE_KEYWORDS))

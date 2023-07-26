"""
This script uses requests and OpenAI to scrape the web & find relevant job postings.

The script works for most pages except:
1. Careers pages that are dynamically generated
    a. Most larger companies that have a shit ton of job postings that are dynamically grouped
    b. Most companies that host on Ashby
2. Careers pages on websites with bot verifiers (will return a 403 forbidden)
3. Job postings on specific listings
    a. Wellfound
    b. YC
"""


import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import openai

from board_page import BoardPage


openai.api_key = os.getenv("OPENAI_API_KEY")
URL = "http://careers.hebbia.ai/"
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

try:
    with urlopen(req) as f:
        page = f.read().decode("utf-8")
except HTTPError as e:
    print("HTTPError on request:", e)
except URLError as e:
    print("URLError on request:", e)
else:
    soup = BeautifulSoup(page, "html.parser")

    # Create a new BoardPage
    board_page = BoardPage(soup, URL)
    # print(board_page.get_page_soup().prettify())
    print(board_page.scrape_all_relevant_roles(ROLE_KEYWORDS))

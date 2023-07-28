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
    c. LinkedIn
"""


import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import openai

from board_page import BoardPage
from listing_page import ListingPage


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


def open_and_create_soup(url: str) -> BeautifulSoup:
    """
    Requests and creates a bs4 object from url
    """
    req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urlopen(req) as f:
            page = f.read().decode("utf-8")
    except HTTPError as e:
        print("HTTPError on request:", e)
    except URLError as e:
        print("URLError on request:", e)
    else:
        return BeautifulSoup(page, "html.parser")
    return None


# Create a new BoardPage
board_page = BoardPage(open_and_create_soup(URL), URL)
relevant_role_links = board_page.scrape_all_relevant_roles(ROLE_KEYWORDS)
base_url = board_page.get_ats_base_url()

listing_pages = []
for relevant_role_link in relevant_role_links:
    listing_page = ListingPage(
        open_and_create_soup(relevant_role_link), relevant_role_link, base_url=base_url
    )
    print(listing_page.scrape_job_title())
    print(listing_page.scrape_job_description())
    listing_pages.append(listing_page)

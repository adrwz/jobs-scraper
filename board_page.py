"""
Page listing all job listings
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from models import ATSBaseURL


class BoardPage:
    """
    The page listing all job listings
    """

    def __init__(self, page_soup: BeautifulSoup, url: str) -> None:
        self.url = url
        self._iterate_to_base_soup(page_soup)
        self._identify_base_url(url)

    def _iterate_to_base_soup(self, page_soup: BeautifulSoup) -> None:
        """
        Recursively loop through iframes until the base board page is found
        Assumption: the base soup probably has a host of ATSBaseURL links
        """
        self.page_soup = page_soup

        # First, try and parse through iframes because they're handled differently
        iframes = page_soup.find_all("iframe")
        for iframe in iframes:
            # Fetch the right source & open
            iframe_src = iframe.attrs.get("src", "")
            if "http" not in iframe_src:
                iframe_src = iframe.attrs.get("data-src", "")

            ats_base_urls = list(ATSBaseURL.__members__.values())
            for ats_base_url in ats_base_urls:
                if ats_base_url in iframe_src:
                    with urlopen(iframe_src) as response:
                        self.page_soup = BeautifulSoup(response, "html.parser")
                    return

    def _identify_base_url(self, url: str) -> bool:
        """
        Takes in a URL and figures out which ATS platform the page is hosted on
        """
        # Attempt to match current url
        ats_base_urls = list(ATSBaseURL.__members__.values())
        for ats_base_url in ats_base_urls:
            if url in ats_base_url:
                self.ats_base_url = ats_base_url
                return True

        # Loop through all <a> tags and attempt to match href links
        ats_base_urls = list(ATSBaseURL.__members__.values())
        for ats_base_url in ats_base_urls:
            if ats_base_url in str(self.page_soup):
                self.ats_base_url = ats_base_url
                return True

        # Not an ATS system; set to none
        self.ats_base_url = None
        return False

    def scrape_all_relevant_roles(self, role_keywords: str) -> list[str]:
        """
        Scrapes self.page_soup for all relevant roles; returns a list of links
        """
        role_links = []
        for role_keyword in role_keywords:
            role_tags = self.page_soup.find_all(
                lambda tag, keyword=role_keyword: len(tag.find_all()) == 0
                and keyword in tag.text
            )
            for role_tag in role_tags:
                href = role_tag.attrs.get("href", "")
                if href:
                    role_links.append(href)

        return role_links

    def get_page_soup(self) -> BeautifulSoup:
        """
        Returns the bs4 obj
        """
        return self.page_soup

    def get_url(self) -> str:
        """
        Returns the base url
        """
        return self.url

    def get_ats_base_url(self) -> str:
        """
        Returns the ATS system
        """
        return self.ats_base_url

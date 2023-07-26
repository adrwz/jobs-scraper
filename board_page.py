"""
Page listing all job listings
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from models import ATSBaseURL


class BoardPage:
    """
    The page listing all job listings
    """

    def __init__(self, page_soup: BeautifulSoup, url: str) -> None:
        self.url = url
        self._iterate_to_base_soup(page_soup)
        self._identify_base_url(url)

    def _has_ats_base_url_links(self, page_soup: BeautifulSoup) -> str:
        """
        Returns a str if there exists an ATS base url <a> tag; None otherwise
        """
        ats_base_urls = list(ATSBaseURL.__members__.values())

        links = page_soup.find_all("a")
        for link in links:
            link_href = link.attrs.get("href", "")
            for ats_base_url in ats_base_urls:
                if link_href in ats_base_url:
                    return ats_base_url

        return None

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

            # Parse
            with urlopen(iframe_src) as response:
                iframe_soup = BeautifulSoup(response, "html.parser")

            if self._has_ats_base_url_links(iframe_soup):
                self.page_soup = iframe_soup
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
        ats_base_url = self._has_ats_base_url_links(self.page_soup)
        if ats_base_url:
            self.ats_base_url = ats_base_url
            return True

        # Not an ATS system; set to none
        self.ats_base_url = None
        return False

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

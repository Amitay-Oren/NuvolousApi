import requests
from bs4 import BeautifulSoup
from typing import List


class WebScraper:
    """
    A class for scraping a website and extracting text from it.
    """

    def __init__(self, url: str):
        """
        Initializes the class with the website URL.
        """
        self.url = url

    def get_text(self) -> str:
        """
        Scrapes the website and returns the extracted text.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        return text

    def get_links(self) -> List[str]:
        """
        Scrapes the website and returns a list of links within the same domain.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and self.url in href:
                links.append(href)
        return links

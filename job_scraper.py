# beautifulsoup, requets
# gets the job description from the url and extracts the required skills and experience from it.
import json

import requests
from bs4 import BeautifulSoup



class BaseJDExtractor:

    def extract(self, html):
        raise NotImplementedError

class JDHTMLExtractor:
    @staticmethod
    def extract(url):
        html = requests.get(url).text
        return BeautifulSoup(html, "html.parser")

class LDJsonExtractor(BaseJDExtractor):

    def extract(self, soup: BeautifulSoup) -> str:

        scripts = soup.find_all("script", {"type": "application/ld+json"})

        for script in scripts:
            try:
                data = json.loads(script.string)

                if isinstance(data, dict) and "description" in data:
                    desc_html = data["description"]
                    return BeautifulSoup(desc_html, "html.parser").get_text("\n")

            except:
                continue

        return ""

class DOMExtractor(BaseJDExtractor):

    def extract(self, soup: BeautifulSoup) -> str:


        # remove noise
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # heuristic: find large text blocks
        candidates = soup.find_all(["div", "section"])

        best_text = ""
        max_len = 0

        for tag in candidates:
            text = tag.get_text(separator="\n").strip()

            if len(text) > max_len:
                max_len = len(text)
                best_text = text

        return best_text

class HeuristicExtractor(BaseJDExtractor):

    KEYWORDS = [
        "responsibilities",
        "requirements",
        "qualifications",
        "job description"
    ]

    def extract(self, soup: BeautifulSoup) -> str:

        text = soup.get_text("\n").lower()

        for keyword in self.KEYWORDS:
            if keyword in text:
                return text

        return ""

class JDExtractor:
    def __init__(self):
        self.extractors = [LDJsonExtractor(), DOMExtractor(), HeuristicExtractor()]

    def extract(self, soup: BeautifulSoup) -> str:
        for extractor in self.extractors:
            result = extractor.extract(soup)

            if result and len(result) > 200:
                return result

        return ""
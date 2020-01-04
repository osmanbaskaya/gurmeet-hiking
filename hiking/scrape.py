from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


SEARCH_URL = "https://gurmeet.net/hiking/hike_search.html"
HIKE_URL = "https://gurmeet.net/hiking/hikes/"


def get_all_hike_links():
    soup = BeautifulSoup(urlopen(SEARCH_URL), "html.parser")
    links = soup.find_all(href=re.compile(HIKE_URL))
    for link in links:
        yield link["href"]


def download_hikes():
    hike_urls = get_all_hike_links()
    for i, url in enumerate(hike_urls, 1):
        print("{}. Downloading {}...".format(i, url))
        content = urlopen(url).read()
        hike_name = get_hike_name(url)
        with open("hikes/{}".format(hike_name), "wt") as f:
            f.write(str(content))


def get_hike_name(url):
    base_url = url.rsplit("/", 1)[1]
    return base_url.lower()


download_hikes()

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import shutil
import re

class Url:
    def __init__(self, full_url):
        self.full_url = full_url
        parsed = urlparse(self.full_url)
        self.domain = parsed.netloc
        self.scheme = parsed.scheme
        self.root_domain = f"{parsed.scheme}://{parsed.netloc}"
        self.path = parsed.path
        self.folder = "/".join(self.path.split("/")[:-1]) + "/"
        self.file = self.path.split("/")[-1]
        if self.file == "":
            self.file = "index.html"

    def request(self):
        self.response = requests.get(self.full_url)
        self.content_type = self.response.headers.get("Content-Type", "")

    def download(self, folder, file):
        os.makedirs(folder, exist_ok=True)
        self.request()

        with open(folder + file, "wb") as f:
            f.write(self.response.content)

    def extract_urls(self, text):
        urls = []

        # src="..." or href="..."
        urls += re.findall(r'src="(.*?)"', text)
        urls += re.findall(r"src='(.*?)'", text)
        urls += re.findall(r'href="(.*?)"', text)
        urls += re.findall(r"href='(.*?)'", text)

        # url(...) in CSS/JS
        urls += re.findall(r'url\(\s*["\']?(.*?)["\']?\s*\)', text)

        return urls
    def extract_links(self):
        if self.content_type == "text/css":
            return self.parse_css(self.response.text, self.full_url);
        if self.content_type == "text/javascript":
            return self.parse_js(self.response.text, self.full_url)
        if self.content_type == "text/html":
            return self.parse_html(self.response.text, self.full_url)
        return []

    def parse_css(self, text, url):
        urls = re.findall(r'url\(\s*[\'"]?(.*?)[\'"]?\s*\)', text)
        links = []
        for src in urls:
            if src.startswith("data"):
                continue
            link = urljoin(url, src)
            if not link.startswith("http"):
                    continue
            links.append(link)

        return links

    def parse_js(self, text, url):
        # Find potential URLs
        urls = re.findall(r"""["'`](?!data:|blob:)([a-zA-Z0-9_\-./?=&%#]+?\.[a-zA-Z0-9]{2,4}[^"'`]*)["'`]""", text)

        links = []
        for src in urls:
            print(src)
            link = urljoin(url, src)
            links.append(link)
        return links

    def parse_html(self, text, url):
        soup = BeautifulSoup(text, "html.parser")
        links = []
        for tag, attr in [("a", "href"), ("img", "src"), ("script", "src"), ("link", "href")]:
            for element in soup.find_all(tag):
                src = element.get(attr)
                if src is None:
                    continue
                if src in ["javascript:void(0);", "javascript: void(0);", "#"]:
                    continue
                if src.startswith("#"):
                    continue
                link = urljoin(url, src)
                if url == link:
                    continue
                if not link.startswith("http"):
                    continue
                links.append(link)

        return list(set(links))

class Scrape:
    def __init__(self, full_url):
        self.url = Url(full_url)
        self.original_domain = self.url.root_domain
        self.scraped_links = []

    def scan(self, full_url=None):
        if full_url is None:
            full_url = self.url.full_url
        if full_url in self.scraped_links:
            return
        url = Url(full_url)
        if url.root_domain != self.original_domain:
            return
        print(url.full_url)
        url.download(os.getcwd() + url.folder, url.file)
        self.scraped_links.append(url.full_url)
        for link in url.extract_links():
            self.scan(link)

    def zip_folder(self, folder):
        shutil.make_archive(folder, "zip", folder)
        print("Zipped to:", folder + ".zip")

full_url = "https://kanakku.dreamstechnologies.com/html/template/index.html"
#full_url = "https://kanakku.dreamstechnologies.com/html/template/assets/js/theme-script.js"
#full_url = "https://kanakku.dreamstechnologies.com/html/template/assets/css/style.css"
url = Url(full_url)
url.request()
urls = re.findall(r'href=["\'](.+?)["\']|src=["\'](.+?)["\']|url\((.+?)\)', url.response.text)
urls = [u for match in urls for u in match if u]
urls = list(set(urls))
for url in urls:
    print(url.strip('"\''))
#print(url.extract_links())
#scrape = Scrape(full_url)
#scrape.scan()
#scrape.zip_folder("html")

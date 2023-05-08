from bs4 import BeautifulSoup

from . import request


def search2dict(html: str):
    soup = BeautifulSoup(html, "html.parser")
    search_result = soup.find("div", {"id": "articles-result", "class": "search-result"})
    card_posts = search_result.find_all("card-post-index")

    results = []
    for card_post in card_posts:
        url_path =  "https://www.alodokter.com" + card_post["url-path"]
        if "e-book-covid-19" not in url_path:
            results.append({
                "url_path": url_path,
                "image_url": card_post["image-url"],
                "category": card_post["category"],
                "label": card_post["label"],
                "title": card_post["title"],
                "short_description": card_post["short-description"].replace("...", ""),
                "content": request.get_article(url_path)
            })

    return results


def parse_article(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("div", {"class": "post-content"}).get_text()


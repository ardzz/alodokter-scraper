from bs4 import BeautifulSoup
import concurrent.futures
from . import request
from .sanitazer import Sanitizer


def sanitize_dict(data: dict):
    return {
        "url_path": data["url_path"],
        "image_url": data["image_url"],
        "category": data["category"],
        "title": sanitize_text(data["title"]),
        "short_description": sanitize_text(data["short_description"]),
        "article": sanitize_text(data["article"]),
    }


def sanitize_text(text: str):
    if text is None:
        return ""
    else:
        return Sanitizer(text).sanitize()


def search2dict(html: str):
    soup = BeautifulSoup(html, "html.parser")
    search_result = soup.find("div", {"id": "articles-result", "class": "search-result"})
    card_posts = search_result.find_all("card-post-index")

    results = []
    for card_post in card_posts:
        url_path = "https://www.alodokter.com" + card_post["url-path"]
        if "e-book-covid-19" not in url_path:
            results.append({
                "url_path": url_path,
                "image_url": card_post["image-url"],
                "category": card_post["category"],
                "title": card_post["title"],
                "short_description": card_post["short-description"].replace("...", ""),
            })
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=30)
    futures = []
    for result in results:
        futures.append(pool.submit(request.get_article, result["url_path"]))
    concurrent.futures.wait(futures)
    for index, future in enumerate(futures):
        results[index]["article"] = future.result()

    futures_sanitizer = []
    for result in results:
        futures_sanitizer.append(pool.submit(sanitize_dict, result))
    concurrent.futures.wait(futures_sanitizer)
    for index, future in enumerate(futures_sanitizer):
        results[index] = future.result()

    return results


def parse_article(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("div", {"class": "post-content"}).get_text()

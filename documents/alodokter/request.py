from requests import get
from urllib.parse import urlparse
from . import parser


def search(query, max_result=25):
    output = []
    index = 1
    base_url = "https://www.alodokter.com/search"
    while len(output) < max_result:
        request = get(base_url, params={"s": query, "page": index}, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-CA,en-US;q=0.5",
        })
        if request.status_code == 200 and "Tidak ditemukan pencarian dengan kata kunci" not in request.text:
            for result in parser.search2dict(request.text):
                if len(output) >= max_result:
                    break
                else:
                    output.append(result)
        else:
            break
        index += 1
    return output


def search_image_by_query(query, max_result=25):
    output = []
    index = 1
    base_url = "https://www.alodokter.com/search"
    while len(output) < max_result:
        request = get(base_url, params={"s": query, "page": index}, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-CA,en-US;q=0.5",
        })
        if request.status_code == 200 and "Tidak ditemukan pencarian dengan kata kunci" not in request.text:
            for result in parser.search_image_to_dict(request.text):
                if len(output) >= max_result:
                    break
                else:
                    output.append(result)
        else:
            break
        index += 1
    return output


def get_article(url):
    url_parse = urlparse(url)
    if len(url_parse.path.split("/")) == 2:
        request = get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-CA,en-US;q=0.5",
        })
        if request.status_code == 200:
            return parser.parse_article(request.text)
        else:
            return None
    else:
        return None

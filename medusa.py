import argparse
import os
import sys
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from queue import Queue
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description="Medusa - Static HTML Scraper")
    parser.add_argument("entry_url", help="Starting URL for scraping")
    parser.add_argument("path", nargs="?", help="Path to scrape (default: path of entry_url)")
    parser.add_argument("--output", help="Output directory for scraped content")
    parser.add_argument("--rewrite", help="File to write URL rewrites")
    return parser.parse_args()

def get_file_path(url, is_dir=False):
    parsed = urlparse(url)
    path = parsed.path
    if not path or path.endswith('/'):
        path += 'index'
    if parsed.query:
        query = parsed.query.replace('?', '_').replace('&', '-')
        path += f"_{query}"
    if is_dir and not path.endswith('/index'):
        path += '/index'
    return f"{path}.html"

def download_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, response.headers.get('content-type', '')
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return None, None

def extract_urls(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for tag in soup.find_all(['a', 'img', 'link', 'script']):
        if tag.name == 'a' and tag.has_attr('href'):
            urls.add(urljoin(base_url, tag['href']))
        elif tag.name == 'img' and tag.has_attr('src'):
            urls.add(urljoin(base_url, tag['src']))
        elif tag.name == 'link' and tag.has_attr('href'):
            urls.add(urljoin(base_url, tag['href']))
        elif tag.name == 'script' and tag.has_attr('src'):
            urls.add(urljoin(base_url, tag['src']))
    return urls

def is_valid_url(url, base_url, path):
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)
    return (parsed_url.netloc == parsed_base.netloc and
            parsed_url.scheme == parsed_base.scheme and
            parsed_url.path.startswith(path))

def rewrite_urls(html, url_map):
    for old_url, new_url in url_map.items():
        html = html.replace(old_url, new_url)
    return html

def main():
    args = parse_arguments()
    entry_url = args.entry_url
    base_path = args.path or urlparse(entry_url).path
    output_dir = args.output
    rewrite_file = args.rewrite

    url_queue = Queue()
    url_queue.put(entry_url)
    processed_urls = set()
    url_map = {}

    while not url_queue.empty():
        current_url = url_queue.get()
        if current_url in processed_urls:
            continue

        html_content, content_type = download_url(current_url)
        if not html_content:
            continue

        processed_urls.add(current_url)

        if 'text/html' in content_type:
            urls = extract_urls(html_content, current_url)
            for url in urls:
                if is_valid_url(url, entry_url, base_path) and url not in processed_urls:
                    url_queue.put(url)

            file_path = get_file_path(current_url, urlparse(current_url).path.endswith('/'))
            new_url = os.path.join(base_path, file_path)
            url_map[current_url] = new_url

            html_content = rewrite_urls(html_content, url_map)

            if output_dir:
                full_path = os.path.join(output_dir, file_path.lstrip('/'))
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            else:
                print(f"{current_url} -> {new_url}")

    if rewrite_file:
        with open(rewrite_file, 'w', encoding='utf-8') as f:
            for old_url, new_url in url_map.items():
                f.write(f"{old_url} -> {new_url}\n")

if __name__ == "__main__":
    main()
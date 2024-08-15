import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime

def get_all_links(url):
    """Crawl the website and return a set of all URLs."""
    urls = set()
    to_visit = [url]
    visited = set()

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        visited.add(current_url)
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_link = urljoin(url, link['href'])
                if urlparse(full_link).netloc == urlparse(url).netloc:
                    urls.add(full_link)
                    to_visit.append(full_link)
        except requests.RequestException:
            continue

    return urls

def generate_sitemap(urls, filename='sitemap.xml'):
    """Generate an XML sitemap from a set of URLs."""
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        for url in urls:
            f.write('  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n')
            f.write('    <changefreq>monthly</changefreq>\n')
            f.write('    <priority>0.5</priority>\n')
            f.write('  </url>\n')

        f.write('</urlset>')

if __name__ == "__main__":
    base_url = 'https://streamhublive.vercel.app/'  # Replace with your website's URL
    urls = get_all_links(base_url)
    generate_sitemap(urls)

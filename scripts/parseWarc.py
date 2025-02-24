from warcio.archiveiterator import ArchiveIterator
import gzip
from bs4 import BeautifulSoup

def parse_warc_file(warc_filename):
    with gzip.open(warc_filename, 'rb') as warc_file:
        for record in ArchiveIterator(warc_file):
            if record.rec_type == 'response':  # Extract HTTP responses
                url = record.rec_headers.get_header('WARC-Target-URI')
                raw_content = record.content_stream().read()

                header_end = raw_content.find(b"\r\n\r\n")
                if header_end != -1:
                    html_content = raw_content[header_end + 4:].decode('utf-8', errors='ignore')

                    print(f"\n[+] URL: {url}")
                    parse_html(html_content)  

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.title.string if soup.title else "No Title"
    text = soup.get_text(separator=" ")  

    print(f"\n[+] Extracted Title: {title}")
    print(f"[+] Extracted Text Preview: {text[:500]}...")  

parse_warc_file("warc_store/CC-NEWS-20250101020153-00156.warc.gz")

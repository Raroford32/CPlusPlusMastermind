import trafilatura
import requests
from urllib.parse import urlparse
from config import WEBSITES, MAX_SAMPLES_PER_SOURCE, MIN_SAMPLE_LENGTH, MAX_SAMPLE_LENGTH
from database.db_operations import insert_code_sample

def get_website_code(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)

    code_samples = []
    lines = text.split('\n')
    in_code_block = False
    current_block = []

    for line in lines:
        if line.strip().startswith('```cpp') or line.strip().startswith('```c++'):
            in_code_block = True
            current_block = []
        elif line.strip() == '```' and in_code_block:
            in_code_block = False
            code = '\n'.join(current_block)
            if MIN_SAMPLE_LENGTH <= len(code) <= MAX_SAMPLE_LENGTH:
                code_samples.append({
                    'source': url,
                    'filename': f"{urlparse(url).netloc}_{len(code_samples)}.cpp",
                    'content': code,
                    'language': 'cpp'
                })
            if len(code_samples) >= MAX_SAMPLES_PER_SOURCE:
                break
        elif in_code_block:
            current_block.append(line)

    return code_samples

def scrape_websites():
    for website in WEBSITES:
        samples = get_website_code(website)
        for sample in samples:
            insert_code_sample(sample)

if __name__ == '__main__':
    scrape_websites()

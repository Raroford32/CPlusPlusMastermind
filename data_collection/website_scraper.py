import trafilatura
import requests
from urllib.parse import urlparse
from config import WEBSITES, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_website_content(url):
    downloaded = trafilatura.fetch_url(url)
    return trafilatura.extract(downloaded)

def extract_code_blocks(text):
    code_blocks = []
    lines = text.split('\n')
    in_code_block = False
    current_block = []
    current_language = ''

    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:
                code_blocks.append({
                    'language': current_language,
                    'content': '\n'.join(current_block)
                })
                in_code_block = False
                current_block = []
                current_language = ''
            else:
                in_code_block = True
                current_language = line.strip()[3:].lower()
        elif in_code_block:
            current_block.append(line)

    return code_blocks

def categorize_code_block(code_block):
    language = code_block['language']
    content = code_block['content'].lower()
    
    if language in ['html', 'css', 'javascript', 'js']:
        return 'frontend'
    elif language in ['python', 'java', 'php', 'ruby', 'go', 'c#', 'nodejs']:
        if 'express' in content or 'flask' in content or 'django' in content or 'spring' in content:
            return 'backend'
        elif 'select' in content or 'insert' in content or 'update' in content or 'delete' in content:
            return 'database'
    elif language in ['sql']:
        return 'database'
    
    return 'other'

def get_website_code(url):
    content = get_website_content(url)
    code_blocks = extract_code_blocks(content)

    code_samples = []
    for i, block in enumerate(code_blocks):
        category = categorize_code_block(block)
        if category != 'other':
            code_samples.append({
                'source': url,
                'filename': f"{urlparse(url).netloc}_{i}.{block['language']}",
                'content': block['content'],
                'language': block['language'],
                'file_type': category
            })

    return code_samples[:MAX_SAMPLES_PER_SOURCE]

def scrape_websites():
    for website in WEBSITES:
        samples = get_website_code(website)
        for sample in samples:
            insert_code_sample(sample)

if __name__ == '__main__':
    scrape_websites()

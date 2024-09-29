import requests
from bs4 import BeautifulSoup
from config import SOURCEFORGE_PROJECTS, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_sourceforge_code(project):
    base_url = f"https://sourceforge.net/p/{project}/code/HEAD/tree/"
    
    samples = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for file_link in soup.select('a[href*="/HEAD/tree/"]'):
        file_url = f"https://sourceforge.net{file_link['href']}"
        file_content = requests.get(file_url).text
        samples.append({
            'source': f'sourceforge/{project}',
            'filename': file_link.text,
            'content': file_content,
            'language': file_link.text.split('.')[-1],
            'file_type': 'backend'  # You may want to improve this classification
        })
    
    return samples[:MAX_SAMPLES_PER_SOURCE]

def scrape_sourceforge():
    all_samples = []
    for project in SOURCEFORGE_PROJECTS:
        samples = get_sourceforge_code(project)
        all_samples.extend(samples)

    for sample in all_samples:
        insert_code_sample(sample)

if __name__ == '__main__':
    scrape_sourceforge()

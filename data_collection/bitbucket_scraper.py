import requests
from config import BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD, BITBUCKET_REPOS, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_bitbucket_code(repo):
    api_url = f"https://api.bitbucket.org/2.0/repositories/{repo}/src"
    auth = (BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD)
    
    samples = []
    for item in requests.get(api_url, auth=auth).json()['values']:
        if item['type'] == 'file':
            file_content = requests.get(item['links']['self']['href'], auth=auth).text
            samples.append({
                'source': f'bitbucket/{repo}',
                'filename': item['path'],
                'content': file_content,
                'language': item['path'].split('.')[-1],
                'file_type': 'backend'  # You may want to improve this classification
            })
    
    return samples[:MAX_SAMPLES_PER_SOURCE]

def scrape_bitbucket():
    all_samples = []
    for repo in BITBUCKET_REPOS:
        samples = get_bitbucket_code(repo)
        all_samples.extend(samples)

    for sample in all_samples:
        insert_code_sample(sample)

if __name__ == '__main__':
    scrape_bitbucket()

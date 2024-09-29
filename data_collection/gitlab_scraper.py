import requests
from config import GITLAB_API_TOKEN, GITLAB_REPOS, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_gitlab_code(repo):
    api_url = f"https://gitlab.com/api/v4/projects/{repo}/repository/tree"
    headers = {"PRIVATE-TOKEN": GITLAB_API_TOKEN}
    
    samples = []
    for item in requests.get(api_url, headers=headers).json():
        if item['type'] == 'blob':
            file_content = requests.get(f"{api_url}/{item['path']}", headers=headers).json()['content']
            samples.append({
                'source': f'gitlab/{repo}',
                'filename': item['path'],
                'content': file_content,
                'language': item['path'].split('.')[-1],
                'file_type': 'backend'  # You may want to improve this classification
            })
    
    return samples[:MAX_SAMPLES_PER_SOURCE]

def scrape_gitlab():
    all_samples = []
    for repo in GITLAB_REPOS:
        samples = get_gitlab_code(repo)
        all_samples.extend(samples)

    for sample in all_samples:
        insert_code_sample(sample)

if __name__ == '__main__':
    scrape_gitlab()

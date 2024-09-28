import requests
import base64
from config import GITHUB_API_TOKEN, GITHUB_REPOS, MAX_SAMPLES_PER_SOURCE, MIN_SAMPLE_LENGTH, MAX_SAMPLE_LENGTH
from database.db_operations import insert_code_sample

def get_github_code(repo, file_extension):
    headers = {'Authorization': f'token {GITHUB_API_TOKEN}'}
    url = f'https://api.github.com/repos/{repo}/git/trees/master?recursive=1'
    response = requests.get(url, headers=headers)
    files = [file for file in response.json()['tree'] if file['path'].endswith(file_extension)]

    code_samples = []
    for file in files:
        file_url = f'https://api.github.com/repos/{repo}/contents/{file["path"]}'
        file_response = requests.get(file_url, headers=headers)
        if file_response.status_code == 200:
            content = base64.b64decode(file_response.json()['content']).decode('utf-8')
            if MIN_SAMPLE_LENGTH <= len(content) <= MAX_SAMPLE_LENGTH:
                code_samples.append({
                    'source': f'github/{repo}',
                    'filename': file['path'],
                    'content': content,
                    'language': 'cpp' if file_extension == '.cpp' else 'python'
                })
        
        if len(code_samples) >= MAX_SAMPLES_PER_SOURCE:
            break

    return code_samples

def scrape_github():
    for repo in GITHUB_REPOS:
        cpp_samples = get_github_code(repo, '.cpp')
        python_samples = get_github_code(repo, '.py')

        for sample in cpp_samples + python_samples:
            insert_code_sample(sample)

if __name__ == '__main__':
    scrape_github()

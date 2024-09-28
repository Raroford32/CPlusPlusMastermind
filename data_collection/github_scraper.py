import requests
import base64
from config import GITHUB_API_TOKEN, GITHUB_REPOS, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_repo_contents(repo, path=''):
    headers = {'Authorization': f'token {GITHUB_API_TOKEN}'}
    url = f'https://api.github.com/repos/{repo}/contents/{path}'
    response = requests.get(url, headers=headers)
    return response.json()

def is_full_stack_repo(repo):
    contents = get_repo_contents(repo)
    has_frontend = any(item['name'].lower() in ['frontend', 'client', 'web'] for item in contents if item['type'] == 'dir')
    has_backend = any(item['name'].lower() in ['backend', 'server', 'api'] for item in contents if item['type'] == 'dir')
    return has_frontend and has_backend

def get_file_content(repo, file_path):
    headers = {'Authorization': f'token {GITHUB_API_TOKEN}'}
    url = f'https://api.github.com/repos/{repo}/contents/{file_path}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        return content
    return None

def get_github_code(repo):
    if not is_full_stack_repo(repo):
        print(f"{repo} is not a full-stack repository. Skipping.")
        return []

    code_samples = []
    stack = [('', 'root')]

    while stack and len(code_samples) < MAX_SAMPLES_PER_SOURCE:
        current_path, current_type = stack.pop()
        contents = get_repo_contents(repo, current_path)

        for item in contents:
            if item['type'] == 'dir':
                stack.append((item['path'], 'dir'))
            elif item['type'] == 'file':
                _, ext = os.path.splitext(item['name'])
                if ext.lower() in ['.py', '.js', '.html', '.css', '.cpp', '.h', '.sql']:
                    content = get_file_content(repo, item['path'])
                    if content:
                        code_samples.append({
                            'source': f'github/{repo}',
                            'filename': item['path'],
                            'content': content,
                            'language': ext[1:],  # Remove the dot from the extension
                            'file_type': 'frontend' if ext.lower() in ['.js', '.html', '.css'] else 'backend'
                        })

    return code_samples

def scrape_github():
    for repo in GITHUB_REPOS:
        samples = get_github_code(repo)
        for sample in samples:
            insert_code_sample(sample)

if __name__ == '__main__':
    scrape_github()

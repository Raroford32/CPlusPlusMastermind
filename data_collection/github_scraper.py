import os
import tempfile
from git import Repo
import shutil
from config import GITHUB_API_TOKEN, GITHUB_REPOS, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def clone_repository(repo_url, temp_dir):
    try:
        Repo.clone_from(repo_url, temp_dir)
        return True
    except Exception as e:
        print(f"Error cloning repository {repo_url}: {str(e)}")
        return False

def process_file(repo, file_path, temp_dir):
    _, ext = os.path.splitext(file_path)
    if ext.lower() in ['.py', '.js', '.html', '.css', '.cpp', '.h', '.sql', '.txt', '.md']:
        with open(os.path.join(temp_dir, file_path), 'r', encoding='utf-8') as file:
            content = file.read()
        return {
            'source': f'github/{repo}',
            'filename': file_path,
            'content': content,
            'language': ext[1:],  # Remove the dot from the extension
            'file_type': 'frontend' if ext.lower() in ['.js', '.html', '.css'] else 'backend'
        }
    return None

def process_directory(repo, directory, temp_dir):
    samples = []
    for root, _, files in os.walk(os.path.join(temp_dir, directory)):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), temp_dir)
            sample = process_file(repo, file_path, temp_dir)
            if sample:
                samples.append(sample)
    return samples

def get_github_code(repo):
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_url = f"https://github.com/{repo}.git"
        if not clone_repository(repo_url, temp_dir):
            return []

        return process_directory(repo, '', temp_dir)

def scrape_github():
    all_samples = []
    for repo in GITHUB_REPOS:
        samples = get_github_code(repo)
        all_samples.extend(samples[:MAX_SAMPLES_PER_SOURCE])

    for sample in all_samples:
        insert_code_sample(sample)

if __name__ == '__main__':
    scrape_github()

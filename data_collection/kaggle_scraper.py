import os
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
from config import KAGGLE_SOURCES, MAX_SAMPLES_PER_SOURCE, KAGGLE_USERNAME, KAGGLE_KEY
from database.db_operations import insert_code_sample

def authenticate_kaggle():
    try:
        os.environ['KAGGLE_USERNAME'] = KAGGLE_USERNAME
        os.environ['KAGGLE_KEY'] = KAGGLE_KEY
        api = KaggleApi()
        api.authenticate()
        return api
    except Exception as e:
        print(f"Error authenticating with Kaggle API: {str(e)}")
        return None

def download_and_process_kaggle_dataset(api, dataset):
    try:
        # Download the dataset
        api.dataset_download_files(dataset, path='./kaggle_data', unzip=True)
        
        samples = []
        for root, _, files in os.walk('./kaggle_data'):
            for file in files:
                if file.endswith(('.py', '.cpp', '.h', '.hpp')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    samples.append({
                        'source': f'kaggle/{dataset}',
                        'filename': file,
                        'content': content,
                        'language': 'python' if file.endswith('.py') else 'cpp',
                        'file_type': 'backend'  # You may want to improve this classification
                    })
        
        # Clean up downloaded files
        for root, dirs, files in os.walk('./kaggle_data', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir('./kaggle_data')
        
        return samples[:MAX_SAMPLES_PER_SOURCE]
    except Exception as e:
        print(f"Error processing Kaggle dataset {dataset}: {str(e)}")
        return []

def scrape_kaggle():
    api = authenticate_kaggle()
    if not api:
        return

    all_samples = []
    for dataset in KAGGLE_SOURCES:
        samples = download_and_process_kaggle_dataset(api, dataset)
        all_samples.extend(samples)

    for sample in all_samples:
        insert_code_sample(sample)

if __name__ == '__main__':
    scrape_kaggle()

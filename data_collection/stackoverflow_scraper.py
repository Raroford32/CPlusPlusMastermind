import requests
from config import STACKOVERFLOW_API_KEY, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_stackoverflow_code(tag):
    url = 'https://api.stackexchange.com/2.3/questions'
    params = {
        'order': 'desc',
        'sort': 'votes',
        'tagged': tag,
        'site': 'stackoverflow',
        'filter': 'withbody',
        'key': STACKOVERFLOW_API_KEY
    }

    code_samples = []
    page = 1
    while len(code_samples) < MAX_SAMPLES_PER_SOURCE:
        params['page'] = page
        response = requests.get(url, params=params)
        questions = response.json()['items']

        if not questions:
            break

        for question in questions:
            code_blocks = extract_code_blocks(question['body'])
            for code in code_blocks:
                code_samples.append({
                    'source': f'stackoverflow/{question["question_id"]}',
                    'filename': f'stackoverflow_{question["question_id"]}.{tag}',
                    'content': code,
                    'language': 'cpp' if tag == 'c++' else 'python',
                    'file_type': 'backend'  # Assuming most StackOverflow code is backend-related
                })

        page += 1

    return code_samples[:MAX_SAMPLES_PER_SOURCE]

def extract_code_blocks(html_content):
    # Simple regex-based code block extraction (can be improved with HTML parsing)
    import re
    return re.findall(r'<code>(.*?)</code>', html_content, re.DOTALL)

def scrape_stackoverflow():
    cpp_samples = get_stackoverflow_code('c++')
    python_samples = get_stackoverflow_code('python')

    for sample in cpp_samples + python_samples:
        insert_code_sample(sample)

if __name__ == '__main__':
    scrape_stackoverflow()

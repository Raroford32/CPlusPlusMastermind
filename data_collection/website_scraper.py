import trafilatura
import requests
from urllib.parse import urlparse
from config import WEBSITES, MAX_SAMPLES_PER_SOURCE
from database.db_operations import insert_code_sample

def get_website_code(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)

    code_samples = []
    lines = text.split('\n')
    in_code_block = False
    current_block = []

    for line in lines:
        if line.strip().startswith('
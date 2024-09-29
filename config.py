import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.environ['PGHOST'],
    'database': os.environ['PGDATABASE'],
    'user': os.environ['PGUSER'],
    'password': os.environ['PGPASSWORD'],
    'port': os.environ['PGPORT']
}

# GitHub API configuration
GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')

# GitLab API configuration
GITLAB_API_TOKEN = os.environ.get('GITLAB_API_TOKEN')

# Bitbucket API configuration
BITBUCKET_USERNAME = os.environ.get('BITBUCKET_USERNAME')
BITBUCKET_APP_PASSWORD = os.environ.get('BITBUCKET_APP_PASSWORD')

# StackOverflow API configuration
STACKOVERFLOW_API_KEY = os.environ.get('STACKOVERFLOW_API_KEY')

# List of popular C++ and Python repositories to scrape
GITHUB_REPOS = [
    'opencv/opencv',
    'tensorflow/tensorflow',
    'electron/electron',
    'apple/swift',
    'microsoft/terminal',
    'google/googletest',
    'protocolbuffers/protobuf',
    'nlohmann/json',
    'google/leveldb',
    'facebook/rocksdb',
    'apache/thrift',
    'grpc/grpc',
    'bitcoin/bitcoin',
    'ethereum/solidity',
    'BVLC/caffe'
]

# List of GitLab repositories to scrape
GITLAB_REPOS = [
    'gitlab-org/gitlab',
    'gnachman/iTerm2',
    'python/cpython',
    'scikit-learn/scikit-learn'
]

# List of Bitbucket repositories to scrape
BITBUCKET_REPOS = [
    'atlassian/python-bitbucket',
    'atlassian/commonmark-java',
    'atlassian/aui'
]

# List of SourceForge projects to scrape
SOURCEFORGE_PROJECTS = [
    'codeblocks',
    'mingw-w64',
    'sevenzip',
    'notepad-plus-plus'
]

# List of official documentation URLs to scrape
OFFICIAL_DOCS = [
    'https://docs.python.org/3/',
    'https://en.cppreference.com/w/',
    'https://flask.palletsprojects.com/en/2.1.x/',
    'https://docs.djangoproject.com/en/3.2/'
]

# List of programming books to scrape (placeholder)
PROGRAMMING_BOOKS = [
    {'title': 'Python Cookbook', 'author': 'David Beazley', 'url': 'https://example.com/python_cookbook'},
    {'title': 'Effective Modern C++', 'author': 'Scott Meyers', 'url': 'https://example.com/effective_modern_cpp'}
]

# List of academic sources to scrape
ACADEMIC_SOURCES = [
    'https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/',
    'https://web.stanford.edu/class/cs106b/'
]

# List of websites to scrape for code samples
WEBSITES = [
    'https://www.geeksforgeeks.org/c-plus-plus/',
    'https://www.cplusplus.com/doc/tutorial/',
    'https://en.cppreference.com/w/cpp/language',
    'https://www.learncpp.com/',
    'https://www.codeproject.com/KB/cpp/'
]

# Maximum number of code samples to collect per source
MAX_SAMPLES_PER_SOURCE = 1000

# Minimum and maximum code sample lengths (in characters)
MIN_SAMPLE_LENGTH = 100
MAX_SAMPLE_LENGTH = 10000

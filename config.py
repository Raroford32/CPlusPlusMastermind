import os

# Database configuration
DB_CONFIG = {
    'host': os.environ['PGHOST'],
    'database': os.environ['PGDATABASE'],
    'user': os.environ['PGUSER'],
    'password': os.environ['PGPASSWORD'],
    'port': os.environ['PGPORT']
}

# GitHub API configuration
GITHUB_API_TOKEN = 'your_github_api_token'

# StackOverflow API configuration
STACKOVERFLOW_API_KEY = 'your_stackoverflow_api_key'

# List of popular C++ repositories to scrape
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

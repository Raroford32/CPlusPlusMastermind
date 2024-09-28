import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_code_sample(sample):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO code_samples (source, filename, content, language)
                VALUES (%s, %s, %s, %s)
            """, (sample['source'], sample['filename'], sample['content'], sample['language']))

def get_all_code_samples():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM code_samples")
            return cur.fetchall()

def update_code_sample(sample):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE code_samples
                SET content = %s, categories = %s, complexity = %s
                WHERE id = %s
            """, (sample['content'], sample['categories'], sample['complexity'], sample['id']))

def get_samples_for_fine_tuning(limit=1000):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                SELECT * FROM code_samples
                ORDER BY RANDOM()
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

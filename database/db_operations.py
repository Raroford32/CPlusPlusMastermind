import psycopg2
from psycopg2.extras import execute_values, DictCursor
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_code_sample(sample):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO code_samples (source, filename, content, language, categories, complexity)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (sample['source'], sample['filename'], sample['content'], sample['language'], sample['categories'], sample['complexity']))

def get_all_code_samples():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
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

def get_samples_by_criteria(criteria):
    query = "SELECT * FROM code_samples WHERE 1=1"
    params = []

    if criteria.get('language'):
        query += " AND language = %s"
        params.append(criteria['language'])

    if criteria.get('category'):
        query += " AND %s = ANY(categories)"
        params.append(criteria['category'])

    if criteria.get('complexity'):
        if criteria['complexity'] == 'simple':
            query += " AND complexity < 5"
        elif criteria['complexity'] == 'moderate':
            query += " AND complexity >= 5 AND complexity < 10"
        elif criteria['complexity'] == 'complex':
            query += " AND complexity >= 10"

    query += " LIMIT 100"  # Limit the number of results

    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

def get_samples_for_fine_tuning(limit=1000):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM code_samples
                ORDER BY RANDOM()
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

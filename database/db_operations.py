import psycopg2
from psycopg2.extras import execute_values, DictCursor
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_project(project):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO projects (name, repository_url, build_system, dependencies)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (project['name'], project['repository_url'], project['build_system'], project['dependencies']))
            return cur.fetchone()[0]

def insert_code_sample(sample, project_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO code_samples (project_id, filename, content, language, file_type, categories, complexity, content_windows)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (project_id, sample['filename'], sample['content'], sample['language'], sample['file_type'], sample['categories'], sample['complexity'], sample.get('content_windows')))
            return cur.fetchone()[0]

def insert_file_relationship(sample_id, related_sample_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO file_relationships (sample_id, related_sample_id)
                VALUES (%s, %s)
            """, (sample_id, related_sample_id))

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
                SET content = %s, categories = %s, complexity = %s, content_windows = %s
                WHERE id = %s
            """, (sample['content'], sample['categories'], sample['complexity'], sample.get('content_windows'), sample['id']))

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

def get_samples_for_fine_tuning(limit=10000):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM code_samples
                ORDER BY RANDOM()
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

def get_project_structures():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM projects
            """)
            projects = cur.fetchall()
            if not projects:
                return {}  # Return an empty dictionary if there are no projects
            return {row['name']: dict(row) for row in projects}

def get_project_details(project_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT p.*, array_agg(DISTINCT cs.*) as files
                FROM projects p
                LEFT JOIN code_samples cs ON p.id = cs.project_id
                WHERE p.id = %s
                GROUP BY p.id
            """, (project_id,))
            project = cur.fetchone()
            
            if project:
                project = dict(project)
                project['files'] = [dict(file) for file in project['files'] if file['id'] is not None]
                return project
            else:
                return None
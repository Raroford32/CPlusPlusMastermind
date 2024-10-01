import os
import psycopg2

def initialize_database():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    cur = conn.cursor()

    with open('database/db_schema.sql', 'r') as schema_file:
        cur.execute(schema_file.read())

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_database()

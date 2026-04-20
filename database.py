import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        sslmode = os.getenv("DB_SSLMODE")
    )
    
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("""
            CREATE TABLE IF NOT EXISTS persons 
            (
                id SERIAL PRIMARY KEY, 
                first_name VARCHAR(50), 
                last_name VARCHAR(50),
                address VARCHAR(100),
                age INTEGER
            );
            """)
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully.")
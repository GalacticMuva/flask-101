from flask import Flask, jsonify
from psycopg2.extras import RealDictCursor
import database

app = Flask(__name__)

# Initialize the table on startup
database.init_db()

@app.route("/")
def home():
    return jsonify({"message": "Hello, Galaxy!"})

@app.route("/persons") # Changed to match assignment specs
def get_persons(): 
    conn = database.get_connection()
    # Using RealDictCursor automatically formats rows as dictionaries
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM persons;")
        results = cur.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Ensure this is NOT indented
if __name__ == "__main__":
    app.run(debug=True)
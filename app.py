from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
import database_config

app = Flask(__name__)

database_config.init_db()

@app.route("/")
def home():
    return jsonify({"message": "Hello, Galaxy!"})

@app.route("/persons") 
def get_persons(): 
    conn = database_config.get_connection()
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

@app.route("/persons", methods=["POST"])
def add_person():
    data = request.get_json()
    
    conn = database_config.get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:       
        cur.execute("""
            INSERT INTO persons (first_name, last_name, address, age)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (data['first_name'], data['last_name'], data['address'], data['age']))
        
        new_person = cur.fetchone()
        conn.commit()
        return jsonify({"message": "User added!", "user": new_person}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()        

if __name__ == "__main__":
    app.run(debug=True)
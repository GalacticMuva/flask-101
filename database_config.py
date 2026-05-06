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
    
    # 1. Drivers 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            license_type VARCHAR(50)
        );
    """)

    # 2. Vehicles (1:1 with Driver)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id SERIAL PRIMARY KEY,
            model VARCHAR(100),
            license_plate VARCHAR(20) UNIQUE,
            driver_id INTEGER UNIQUE REFERENCES drivers(driver_id)
        );
    """)

    # 3. Routes (1:N with Driver)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            route_id SERIAL PRIMARY KEY,
            date DATE DEFAULT CURRENT_DATE,
            service_zone VARCHAR(100),
            driver_id INTEGER REFERENCES drivers(driver_id)
        );
    """)

    # 4. Packages (1:N with Route)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            package_id SERIAL PRIMARY KEY,
            description TEXT,
            weight NUMERIC,
            route_id INTEGER REFERENCES routes(route_id)
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Logistics database initialized successfully.")

# --- DRIVER CRUD ---

def create_driver(name, license_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO drivers (name, license_type) VALUES (%s, %s) RETURNING driver_id;", (name, license_type))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def get_drivers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drivers;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_driver(driver_id, name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE drivers SET name = %s WHERE driver_id = %s;", (name, driver_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_driver(driver_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM drivers WHERE driver_id = %s;", (driver_id,))
    conn.commit()
    cur.close()
    conn.close()

# --- VEHICLE CRUD ---

def create_vehicle(model, license_plate, driver_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO vehicles (model, license_plate, driver_id) VALUES (%s, %s, %s) RETURNING vehicle_id;", (model, license_plate, driver_id))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

# --- ROUTE CRUD ---

def create_route(service_zone, driver_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO routes (service_zone, driver_id) VALUES (%s, %s) RETURNING route_id;", (service_zone, driver_id))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

# --- PACKAGE CRUD ---

def create_package(description, weight, route_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO packages (description, weight, route_id) VALUES (%s, %s, %s) RETURNING package_id;", (description, weight, route_id))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def get_packages_by_route(route_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM packages WHERE route_id = %s;", (route_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
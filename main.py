from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Connect to Render PostgreSQL
conn = psycopg2.connect(
    host="dpg-d2glglogjchc73b9cs7g-a",
    dbname="key_system_db",
    user="key_system_db_user",
    password="key_system_db_user",
    port="5432",
    sslmode="require"
)

# Temporary setup route to create the table
@app.route("/setup", methods=["GET"])
def setup_table():
    try:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            id SERIAL PRIMARY KEY,
            key TEXT UNIQUE NOT NULL
        );
        """)
        conn.commit()
        cur.close()
        return {"message": "Table created successfully!"}
    except Exception as e:
        return {"error": str(e)}, 400

# Generate key (store in DB)
@app.route('/generate', methods=['POST'])
def generate_key():
    data = request.json
    key = data.get('key')
    if not key:
        return jsonify({"error": "No key provided"}), 400

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO keys (key) VALUES (%s) ON CONFLICT DO NOTHING", (key,))
        conn.commit()
        cur.close()
        return jsonify({"message": "Key generated", "key": key}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Validate key (check DB)
@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    if not key:
        return jsonify({"error": "No key provided"}), 400

    cur = conn.cursor()
    cur.execute("SELECT * FROM keys WHERE key = %s", (key,))
    result = cur.fetchone()
    cur.close()

    if result:
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

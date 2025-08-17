from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# File to store keys in the same folder as main.py
KEYS_FILE = os.path.join(os.path.dirname(__file__), "keys.txt")

# Load keys from file
if os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, "r") as f:
        keys = set(line.strip() for line in f.readlines())
else:
    keys = set()

# Save keys to file
def save_keys():
    with open(KEYS_FILE, "w") as f:
        for key in keys:
            f.write(key + "\n")

# Optional: Generate key via URL
@app.route('/generate', methods=['GET'])
def generate_key():
    key = request.args.get('key')
    if not key:
        return jsonify({"error": "No key provided"}), 400
    keys.add(key)
    save_keys()
    return jsonify({"message": "Key generated", "key": key}), 200

# Validate key via URL
@app.route('/validate', methods=['GET'])
def validate_key():
    key = request.args.get('key')
    if key in keys:
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 403

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# File to store keys
KEYS_FILE = "keys.txt"

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

# Generate key (optional; remove if you don't want dynamic generation)
@app.route('/generate', methods=['POST'])
def generate_key():
    data = request.json
    key = data.get('key')
    if not key:
        return jsonify({"error": "No key provided"}), 400
    keys.add(key)
    save_keys()
    return jsonify({"message": "Key generated", "key": key}), 200

# Validate key
@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    if key in keys:
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 403

# Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

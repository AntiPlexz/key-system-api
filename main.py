from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for keys
keys = set()

@app.route('/generate', methods=['POST'])
def generate_key():
    data = request.json
    key = data.get('key')
    if not key:
        return jsonify({"error": "No key provided"}), 400
    keys.add(key)
    return jsonify({"message": "Key generated", "key": key}), 200

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    if key in keys:
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

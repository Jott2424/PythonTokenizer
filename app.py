from flask import Flask, request, jsonify
from functools import wraps
from encryption import encrypt_data, decrypt_data, batch_encrypt_data, batch_decrypt_data

app = Flask(__name__)

# Simple auth
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

def validateCredentials(username, password):
    return username == USERNAME and password == PASSWORD

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if USERNAME is None or PASSWORD is None:
            return jsonify({"error": "Server misconfiguration: credentials not set"}), 500

        auth = request.authorization
        if not auth or not validateCredentials(auth.username, auth.password):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

@app.route('/encrypt', methods=['POST'])
@require_auth
def encrypt_route():
    content = request.json
    data = content.get("data")
    key = content.get("key")

    if not data or not key:
        return jsonify({"error": "Missing 'data' or 'key'"}), 400

    try:
        ciphertext = encrypt_data(data, key)
        return jsonify({"ciphertext": ciphertext})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
@require_auth
def decrypt_route():
    content = request.json
    ciphertext = content.get("ciphertext")
    key = content.get("key")

    if not ciphertext or not key:
        return jsonify({"error": "Missing 'ciphertext' or 'key'"}), 400

    try:
        plaintext = decrypt_data(ciphertext, key)
        return jsonify({"plaintext": plaintext})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_encrypt', methods=['POST'])
@require_auth
def batch_encrypt_route():
    content = request.json
    data_list = content.get("data")
    key = content.get("key")

    if not data_list or not key or not isinstance(data_list, list):
        return jsonify({"error": "Missing or invalid 'data' list or 'key'"}), 400

    try:
        ciphertext_list = batch_encrypt_data(data_list, key)
        return jsonify({"ciphertext": ciphertext_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_decrypt', methods=['POST'])
@require_auth
def batch_decrypt_route():
    content = request.json
    ciphertext_list = content.get("ciphertext")
    key = content.get("key")

    if not ciphertext_list or not key or not isinstance(ciphertext_list, list):
        return jsonify({"error": "Missing or invalid 'ciphertext' list or 'key'"}), 400

    try:
        plaintext_list = batch_decrypt_data(ciphertext_list, key)
        return jsonify({"plaintext": plaintext_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Here, we simulate password hashing as it would be stored in a secure system.
users = {
    "user3": {
        "password_hash": generate_password_hash("pass3"),
    }
}

@app.route('/authenticate', methods=['POST'])
def authenticate():
    credentials = request.json
    username = credentials['username']
    password = credentials['password']

    user = users.get(username)

    # Verify the password against the hashed version
    if user and check_password_hash(user['password_hash'], password):
        # Authentication successful
        return jsonify({
            'status': 'success',
            'username': username,
        }), 200
    else:
        # Authentication failed
        return jsonify({
            'status': 'failure',
            'message': 'Invalid credentials'
        }), 401

if __name__ == '__main__':
    app.run(port=5002, debug=True)
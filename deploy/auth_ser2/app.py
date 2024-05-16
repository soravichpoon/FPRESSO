from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)

# Here, we simulate password hashing as it would be stored in a secure system.
users = {
    "user3": {
        "password_hash": generate_password_hash("pass3"),
        "role": "admin"
    }
}

@app.route('/')
@cross_origin()
def hello():
    return 'auth2'

@app.route('/authenticate', methods=['POST'])
@cross_origin()
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
            'role': user['role']
        }), 200
    else:
        # Authentication failed
        return jsonify({
            'status': 'failure',
            'message': 'Invalid credentials'
        }), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
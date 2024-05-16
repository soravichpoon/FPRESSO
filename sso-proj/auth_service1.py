from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jwt_secret_key1'
CORS(app)

@app.route('/authenticate', methods=['POST'])
@cross_origin()
def authenticate():
    users = {
        "app1": {
            "user_jwt":jwt.encode({'username': 'user1', 'role': 'admin', 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        },
        "app2": {
            "user_jwt":jwt.encode({'username': 'user2', 'role': 'admin', 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        }
    }
    username = request.json['username'] # Simulated validation
    role = request.json['role']
    appNo = request.json['appNo']
    
    # Normally here you would validate the password. We simulate it.
    token = jwt.encode({'username': username, 'role': role, 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
    if users[appNo]['user_jwt'] == token:
        return jsonify({'status': 'success', 'jwt_token': token}), 200
    return jsonify({'status': 'failure','message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
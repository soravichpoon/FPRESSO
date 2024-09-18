from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import jwt
import datetime
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jwt_secret_key1'
CORS(app)

@app.route('/')
@cross_origin()
def hello():
    return 'auth1'

@app.route('/authenticate', methods=['POST'])
@cross_origin()
def authenticate():
    users = {
        "app1": {
            "user_jwt":jwt.encode({'username': 'user1', 'password': 'pass1', 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        },
        "app2": {
            "user_jwt":jwt.encode({'username': 'user2', 'password': 'pass2', 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        }
    }
    username = request.json['username'] # Simulated validation
    password = request.json['password']
    appNo = request.json['appNo']
    
    # Normally here you would validate the password. We simulate it.
    token = jwt.encode({'username': username, 'password': password, 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
    if users[appNo]['user_jwt'] == token:
        return jsonify({'status': 'success', 'jwt_token': token}), 200
    return jsonify({'status': 'failure','message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
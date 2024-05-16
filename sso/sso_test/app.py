from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS, cross_origin
import requests
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'
CORS(app)

token = {'sso-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcxNDQ1ODAyN30.pryvdAJO8pCO2_I-sfVXOb3TW0FOn7KExwKewMacvso'}

@app.route('/')
@cross_origin()
def hello():
    return 'hello'

@app.route('/authenticate', methods=['GET'])
@cross_origin()
def authenticate():
    username = request.headers.get('username')
    role = request.headers.get('role')
    # Create SSO token with user details
    sso_token = jwt.encode({
        'sub': username,
        'role': role,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm=ALGORITHM)
    resp = make_response(jsonify({'sso_token': sso_token}))
    token.update({'sso-token': sso_token})
    return resp

@app.route('/verify', methods=['GET'])
@cross_origin()
def verify():
    sso_token = token['sso-token']
    appNo = request.headers.get('appNo')  # Get role from header
    try:
        decoded = jwt.decode(sso_token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        app_role = requests.get(f'https://{appNo}-test-swlzbjlflq-as.a.run.app/get_role', headers={'username': decoded['sub']})
        if app_role.status_code == 200:
            app_roles = app_role.json()['role']
            return jsonify({'status': 'verified', 'username': decoded['sub'], 'role': app_roles}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'
CORS(app)

users = {
    'app1': {'user1' : {"app1": {"role": "admin"},
                        "app2": {"role": "user"},
                        "app3": {"role": "user"}}
            },
    'app2': {'user2' : {"app1": {"role": "user"},
                        "app2": {"role": "admin"},
                        "app3": {"role": "user"}}
            },
    'app3': {'user3' : {"app1": {"role": "user"},
                        "app2": {"role": "user"},
                        "app3": {"role": "admin"}}
            }
    }

@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return 'Hello'

@app.route('/authenticate', methods=['GET'])
@cross_origin()
def authenticate():
    username = request.headers.get('username')
    app_num = request.headers.get('appNo')
    role = users[app_num][username]
    
    # Create SSO token with user details
    sso_token = jwt.encode({
        'sub': username,
        'role': role,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm=ALGORITHM)
    
    # Set the cookie at the shared parent domain level
    resp = make_response(jsonify({'sso_token': sso_token}))
    resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
    return resp

@app.route('/verify', methods=['GET'])
@cross_origin()
def verify():
    sso_token = request.cookies.get('sso_token')
    app_num = request.headers.get('appNo')  # Get role from the header
    try:
        decoded = jwt.decode(sso_token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        roles = decoded['role']
        app_role = roles[app_num]['role']
        return jsonify({'status': 'verified', 'username': decoded['sub'], 'role': app_role}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
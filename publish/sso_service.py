from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS, cross_origin
import jwt
import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'

privKey = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0gr6/AuK3Z+LSQ7sR4z09b4sdb9roDjgKLTkQoa9yjaFO2oJ
sQ3fpmx7SFbW57qjAL1VH8hFpfb1CGzXONXc4IramDHFZPORLw6bi5PsTuEDuj45
LURkVKIYoKKD7OP/jxNbuPn0l2wc6drveZnYDw0xPk4BGrCse6Tg1zLiizH5b1hK
bjeFrWu4lCHsbHnwyN7YRakpq4bwsACdYyYSh6Qze5hC05pcjKwW7/VNq85G2nmC
jp8Elz5VDybJdgE5IkxG7XDIq8N64ozdFti6wp19pzBQs8rMd45LiheVf/7ubSe+
QxRw/uVmIeYWaYkoo69NjffhTCFdnA/4mwHJyQIDAQABAoIBAFHBTmHuiDWtVQSx
10weVHaWeC24vUaW/ME7b6FpWtQrln5CztTopoXbsby9eFaoMawnBcwiIuHvlv6Z
hsgrjhakVWNp9ABQQdGEKQ0SHaeyM8Y5U/4HodnDYjycJSd+s0lYapo8SHTr8vEf
c5jsRcnOA73RlOJzpB9YVN/OgZlVvNG9zpMt36uyUXmGo6SNpJrmFNXYXYNezHQs
D1bNWrKvtdvayE6Dlvd/Oamr6whDdJu07jLz4ptu4xP8buenFSc0Rt9NF/ALVXRs
do/41ku+Vtyn1g+jXsr0sZw5kUGAi4qri75DSSLQRu9Q7voJwtU1PGTbn6DnQtQa
L+uW+eUCgYEA54AZGxl4a/EEkJD4GsPhyf5UvCvvJzSrBP+a7j5HsNgmXbjaG/dI
HslNQVl+SSDGObq+9W2v+XK+a3yQsV5BxoElY3N4ZHXMmyRIfPwBPJHQot/VO/x1
Vaf90DA+n3mMt/2CwITVeYHzqU52DqHi/9ZrP8hMoLNeakcoWxp3rI8CgYEA6EWM
HXzdVurwQH2tfs/pR0BKi+YNB/n9+TUYAL7WzLSdnM126CzCGqXA1MF99yTF6E0q
Mvgl33Gt1y2xSrjM6ud3se8/XICEQvfnHTFRUsU91IQ67fGOdmBA+8xiA26g41vQ
KRbSDjzpnHmZfq7NqT0aShDGmDukQQtVQ8kRgCcCgYBFjHV+b7t+6kzNxc/T8q9d
yPvaAHT72VXbzZLVKn7NQVLda1CTgEn5fc6o6GMJQ0BqTZFbGJX6oh9VGXo63y9x
nJEH/MPZoo5SuabRbcBNWx1MIWTlfaYekratGiFmNdUx3YavofikZYc3gSv0n2wc
ImXcJqfmy5x8313faOc1PwKBgQDiiKIFSHjfgrfbTjfeDI0qTsvl8fMXqnxHh77n
SzlX4XgvLD0iaDTPpIWTezuNxTG4RTo5B8h4SvkPeqMFi4NgP2yAACU95KIaZonj
8Out3G1XTbfjxcn6Lhpy+n1Fd6o21J8K1BT+ie4WDIrmATrYKp3vSrlGVDT4s0Lv
n7UP1QKBgQCmvFYc6pewoCa9DwhtDsvxIJK6BtU+RIyTUe77YuH0zmOba1261ldG
rSJu42q1FJLCR8v2khBClFkTmLd6s5Qdlnqj3w1BT9aVsbF5LG6c0/if4yIX02p3
hQutUNFFcs3etWKiDRXTSeCMdLBQEbCbAw+xZuU58zypFlfNT3GScA==
-----END RSA PRIVATE KEY-----"""

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
@app.route('/')
@cross_origin()
def hello():
    return 'hello'

# @app.route('/authenticate', methods=['GET'])
# @cross_origin()
# def authenticate():
#     username = request.headers.get('username')
#     app_num = request.headers.get('appNo')
#     role = users[app_num][username]
#     # Create SSO token with user details
#     sso_token = jwt.encode({
#         'sub': username,
#         'role': role,
#         'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
#     }, app.config['SECRET_KEY'], algorithm=ALGORITHM)
#     resp = make_response(jsonify({'sso_token': sso_token}))
#     resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='None')
#     return resp

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
    
    # Sign the token
    try:
        key = RSA.import_key(privKey.strip())
        hasher = SHA256.new(sso_token.encode())
        signature = pkcs1_15.new(key).sign(hasher)

        # Append signature to the token
        signed_token = sso_token + '.' + signature.hex()

        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        # Before importing the key
        logger.debug(f"Importing private key: {privKey}")
        key = RSA.import_key(privKey.strip())

        resp = make_response(jsonify({'sso_token': signed_token}))
        resp.set_cookie('sso_token', signed_token, httponly=True, secure=True, samesite='None')
        return resp
    except ValueError as e:
        print(f"Failed to import key: {e}")

@app.route('/verify', methods=['GET'])
@cross_origin()
def verify():
    sso_token = request.cookies.get('sso_token')
    app_num = request.headers.get('appNo')  # Get role from header
    try:
        decoded = jwt.decode(sso_token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        roles = decoded['role']
        app_role = roles[app_num]['role']
        return jsonify({'status': 'verified', 'username': decoded['sub'], 'role': app_role}), 200
        # return jsonify({'status': 'verified', 'username': decoded['sub'], 'role': 'user'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
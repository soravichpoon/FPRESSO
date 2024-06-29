from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import jwt
import datetime
import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'
CORS(app)

users_data = {
    'app1': {
        'user1': {
            "app1": "admin",
            "app2": "user" ,
            "app3": "user"
        }
    },
    'app2': {
        'user2': {
            "app1": "user",
            "app2": "admin",
            "app3": "user"
        }
    },
    'app3': {
        'user3': {
            "app1": "user",
            "app2": "user",
            "app3": "admin"
        }
    }
}

user_permission = {
    "app1":{
        "admin":{"permissions" : "Read, Write, Execute"},
        "user":{"permissions" : "Read, Write"}
        },
    "app2":{
        "admin":{"permissions" : "Read, Write, Execute"},
        "user":{"permissions" : "Write"}
        },
    "app3":{
        "admin":{"permissions" : "Read, Write, Execute"},
        "user":{"permissions" : "Read"}
        }
    }


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

@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return 'Hello'

def sign_token(token):
    key = RSA.import_key(privKey.strip())
    hasher = SHA256.new(token.encode())
    signature = pkcs1_15.new(key).sign(hasher)
    print(f"sign_token: {token}.{signature.hex()}")
    return f"{token}.{signature.hex()}"

def pad_token(token):
    R1 = os.urandom(128)
    R2 = os.urandom(128)
    padded_token = R1 + token.encode() + R2
    print(f"Padding: R1={R1.hex()}, R2={R2.hex()}")
    return base64.urlsafe_b64encode(padded_token).decode()

@app.route('/authenticate', methods=['GET'])
@cross_origin()
def generate_sso_token():
    username = request.headers.get('username')
    app_num = request.headers.get('appNo')
    
    if app_num not in users_data or username not in users_data[app_num]:
        return make_response(jsonify({'error': 'Invalid app number or username'}), 400)
    
    role = users_data[app_num][username]
    permissions = user_permission
    
    jwt_token = {
        "userID": username,
        "roles": {},
        "permissions": {},
        'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
    }
    
    # hash role permissions
    for apps, user_role in role.items():
        try:
            role_hash = hashlib.sha256(','.join(user_role).encode()).hexdigest()
            jwt_token['roles'][apps] = role_hash
            permission_hash = hashlib.sha256(','.join(permissions[apps][user_role]['permissions']).encode()).hexdigest()
            jwt_token['permissions'][apps] = permission_hash
        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"app_num: {app_num}, username: {username}, role: {role}, app: {apps}, user_role: {user_role}")
            return make_response(jsonify({'error': 'Invalid role or permission data'}), 500)
    
    # Sign the token with HSM
    token = jwt.encode(jwt_token, app.config['SECRET_KEY'], algorithm=ALGORITHM)
    signed_token = sign_token(token)

    # Padding
    padded_token = pad_token(signed_token)
    sso_token = padded_token

    # sso_token = signed_token
    resp = make_response(jsonify({'sso_token': sso_token}))
    resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='None')
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
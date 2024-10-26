from flask import Flask, request, redirect, make_response, render_template_string, jsonify
from flask_cors import CORS, cross_origin
import requests
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'
CORS(app)

# Simulated user data
users = {
    "user2": {"password": "pass2"}
}

user_role = {
    "admin":"35a3716d343040c666a071477427535ada70f74ceee8b9d9058d4412cbe40c52",
    "users":"0b35b922fd1c5853cf65b737f49c49d8ef750946b5939443056d94b3a3510dc6"
}

user_permission = {
    "admin":{"Read, Write, Execute"},
    "users":{"Write"}
}

permission_hash = {
    "admin":"138c4b0b96c01b0715d870c11c0853592aa32137c421e73827821fe14c9aab6e",
    "users":"0d1279c2e372cf1c8dcc4bef0cf2431eabcb61ddd52cd613673c15eb2cb8a958"
}

pKey = """-----BEGIN RSA PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0gr6/AuK3Z+LSQ7sR4z0
9b4sdb9roDjgKLTkQoa9yjaFO2oJsQ3fpmx7SFbW57qjAL1VH8hFpfb1CGzXONXc
4IramDHFZPORLw6bi5PsTuEDuj45LURkVKIYoKKD7OP/jxNbuPn0l2wc6drveZnY
Dw0xPk4BGrCse6Tg1zLiizH5b1hKbjeFrWu4lCHsbHnwyN7YRakpq4bwsACdYyYS
h6Qze5hC05pcjKwW7/VNq85G2nmCjp8Elz5VDybJdgE5IkxG7XDIq8N64ozdFti6
wp19pzBQs8rMd45LiheVf/7ubSe+QxRw/uVmIeYWaYkoo69NjffhTCFdnA/4mwHJ
yQIDAQAB
-----END RSA PUBLIC KEY-----"""

@app.route('/')
@cross_origin()
def home():
    return render_template_string('''
        <h1>Welcome to App2</h1>
        <form action="/login" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
            <a href="/check">SSO</a>
        </form>
    ''')

def unpadded_token(padded_token):
    try:
        padded_bytes = base64.urlsafe_b64decode(padded_token)
        token_bytes = padded_bytes[128:-128]

        # print(f"Unpadding: R1={R1.hex()}, R2={R2.hex()}")
        # print(f"Token Bytes: {token_bytes}")

        # No XOR operation is needed here since we are simply removing R1 and R2
        unperturbed_bytes = token_bytes
        
        # print(f"Unpadded Token Bytes: {unperturbed_bytes}")
        unpadded_token = unperturbed_bytes.decode()
        
        # print(f"Unpadded Token: {unpadded_token}")
        return unpadded_token
    except Exception as e:
        print(f"Error during unpadding: {e}")
        return None

def verify_token(signed_token):
    try:
        token_part, sig_hex = signed_token.rsplit('.', 1)
        signature = bytes.fromhex(sig_hex)
        key = RSA.import_key(pKey.strip())
        hasher = SHA256.new(token_part.encode())
        pkcs1_15.new(key).verify(hasher, signature)
        return True
    except (ValueError, TypeError):
        return False

@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    # Send user data to Authentication Service 1
    auth_response = requests.post('https://auth-service1-hlcp4m5f5q-as.a.run.app/authenticate', json={'username': username, 'password': password, 'appNo' : 'app2'})
    if auth_response.status_code == 200:
        # Authenticate with SSO service
        sso_response = requests.get('https://sso-service-hlcp4m5f5q-as.a.run.app/authenticate', headers={'username':username, 'appNo': 'app2'})
        if sso_response.status_code == 200:
            sso_token = sso_response.json()['sso_token']
            resp = make_response(redirect('/protected'))
            resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
            print('set cookies success')
            return resp
        return 'SSO Service Error', sso_response.status_code
    return 'Authentication Service Error', auth_response.status_code

@app.route('/getCookie', methods=['GET'])
@cross_origin()
def get_cookie():
    return jsonify({'sso_token': sso_token}), 200

@app.route('/check', methods=['GET'])
@cross_origin()
def check():
    tok_resp = requests.get('https://app1-hlcp4m5f5q-as.a.run.app/getCookie', headers={'appNo': 'app2'})
    tok2_resp = requests.get('https://app3-hlcp4m5f5q-as.a.run.app/getCookie', headers={'appNo': 'app2'})
    if tok_resp and tok_resp.json()['sso_token'] != '':
        sso_token = tok_resp.json()['sso_token']
        resp = make_response(redirect('/protected'))
        resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
        return resp
    elif tok2_resp and tok2_resp.json()['sso_token'] != '':
        sso_token = tok2_resp.json()['sso_token']
        resp = make_response(redirect('/protected'))
        resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
        return resp

@app.route('/protected')
@cross_origin()
def protected():
    token = request.cookies.get('sso_token')
    sign_token = unpadded_token(token)
    # print(f"sign Token: {sign_token}")
    if token and verify_token(sign_token):
        # print('ver true')
        sign_token = sign_token.rsplit('.', 1)[0]
        # print(f"sign Token: {sign_token}")
        decoded = jwt.decode(sign_token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        username = decoded["userID"]
        rolehash = decoded['roles']["app2"]
        permissionhash = decoded['permissions']['app2']
        if rolehash == user_role["admin"]:
            role = "admin"
            if permissionhash == permission_hash["admin"]:
                permission = user_permission["admin"]
            else:
                return 'Access denied <a href="/">Login</a>', 403
        elif rolehash == user_role["users"]:
            role = "user"
            if permissionhash == permission_hash["users"]:
                permission = user_permission['users']
            else:
                return 'Access denied <a href="/">Login</a>', 403
        else:
            return 'Access denied <a href="/">Login</a>', 403    

        return render_template_string(f'''
                <h1>Protected Content</h1>
                <p>Username: {username}</p>
                <p>Role: {role}</p>
                <p>Permissions: {permission}</p>
                <a href="/logout">Logout</a>
            ''')
    return 'Access denied <a href="/">Login</a>', 403

@app.route('/logout')
@cross_origin()
def logout():
    global sso_token
    sso_token = ''
    resp = make_response(redirect('/'))
    resp.set_cookie('sso_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
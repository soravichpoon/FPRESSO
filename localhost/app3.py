from flask import Flask, request, jsonify, redirect, make_response, render_template_string
from flask_cors import CORS, cross_origin
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sso_secret_key'
ALGORITHM = 'HS256'
CORS(app)

users = {
    "user3": {"password": "pass3"}
}
user_role = {
    "admin":"35a3716d343040c666a071477427535ada70f74ceee8b9d9058d4412cbe40c52",
    "users":"0b35b922fd1c5853cf65b737f49c49d8ef750946b5939443056d94b3a3510dc6"
}

user_permission = {
    "admin":{"Read, Write, Execute"},
    "users":{"Read"}
}
permission_hash = {
    "admin":"138c4b0b96c01b0715d870c11c0853592aa32137c421e73827821fe14c9aab6e",
    "users":"7e64a756a018887b63776d859285cdc91012e4834d74d1133e2650ff672770d6"
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
def home():
    return render_template_string('''
        <h1>Welcome to App3</h1>
        <form action="/login" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
            <a href="/protected">SSO</a>
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

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    auth_response = requests.post(
        'http://localhost:5002/authenticate', 
        json={'username': username, 'password': password}
    )
    if auth_response.status_code == 200:
        sso_response = requests.get('http://localhost:5000/authenticate', headers={'username':username, 'appNo': 'app3'})
        if sso_response.status_code == 200:
            sso_token = sso_response.json()['sso_token']
            resp = make_response(redirect('/protected'))
            resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
            return resp
        return 'SSO Service Error', sso_response.status_code
    return 'Authentication Service Error', auth_response.status_code

@app.route('/protected')
def protected():
    token = request.cookies.get('sso_token')
    sign_token = unpadded_token(token)
    print(f"sign Token: {sign_token}")
    if token and verify_token(sign_token):
        print('ver true')
        sign_token = sign_token.rsplit('.', 1)[0]
        print(f"sign Token: {sign_token}")
        decoded = jwt.decode(sign_token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        username = decoded["userID"]
        rolehash = decoded['roles']["app3"]
        permissionhash = decoded['permissions']['app3']
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
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('sso_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(port=5103, debug=True)
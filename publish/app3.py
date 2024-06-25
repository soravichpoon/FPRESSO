from flask import Flask, request, jsonify, redirect, make_response, render_template_string
from flask_cors import CORS, cross_origin
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

app = Flask(__name__)
CORS(app)

users = {
    "user3": {"password": "pass3", "role": "admin"}
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

def verify_token(signed_token):
    # Split the token from the signature
    token_part, sig_hex = signed_token.rsplit('.', 1)
    
    # Convert hex signature back to bytes
    signature = bytes.fromhex(sig_hex)
    
    # Load public key
    key = RSA.import_key(pKey.strip())
    
    # Verify the signature
    hasher = SHA256.new(token_part.encode())
    try:
        pkcs1_15.new(key).verify(hasher, signature)
        return True
    except (ValueError, TypeError):
        return False
    
# Use verify_token in the route where you handle the protected endpoint
@app.route('/protected')
@cross_origin()
def protected():
    token = request.cookies.get('sso_token')
    if token and verify_token(token):
        # Decode the JWT part only if the signature is valid
        token_part = token.rsplit('.', 1)[0]
        verify_response = requests.get('http://localhost:5000/verify', headers={'appNo': 'app3'}, cookies={'sso_token': token_part})
        if verify_response.status_code == 200:
            username = verify_response.json()['username']
            role = verify_response.json()['role']  # This will now reflect the role sent by the app
            return render_template_string(f'''
                <h1>Protected Content</h1>
                <p>Username: {username}</p>
                <p>Role: {role}</p>
                <a href="/logout">Logout</a>
            ''')
    return 'Access denied <a href="/">Login</a>', 403

# @app.route('/protected')
# def protected():
#     token = request.cookies.get('sso_token')
#     # Assuming the app knows its role or fetches it from some configuration
#     if token:
#         verify_response = requests.get('http://localhost:5000/verify', headers={'appNo': 'app3'}, cookies={'sso_token': token})
#         if verify_response.status_code == 200:
#             username = verify_response.json()['username']
#             role = verify_response.json()['role']  # This will now reflect the role sent by the app
#             return render_template_string(f'''
#                 <h1>Protected Content</h1>
#                 <p>Username: {username}</p>
#                 <p>Role: {role}</p>
#                 <a href="/logout">Logout</a>
#             ''')
#     return 'Access denied <a href="/">Login</a>', 403

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('sso_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(port=5103, debug=True)
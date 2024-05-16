from flask import Flask, request, redirect, make_response, render_template_string, jsonify
from flask_cors import CORS, cross_origin
import requests
import os

app = Flask(__name__)
CORS(app)

# Simulated user data
users = {
    "user2": {"password": "pass2", "role": "admin"}
}

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

@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    # Send user data to Authentication Service 1
    auth_response = requests.post('https://auth-service1-swlzbjlflq-as.a.run.app/authenticate', json={'username': username, 'password': password, 'role': user['role'], 'appNo' : 'app2'})
    if auth_response.status_code == 200:
        # Authenticate with SSO service
        sso_response = requests.get('https://sso-service-swlzbjlflq-as.a.run.app/authenticate', headers={'username':username, 'appNo': 'app2'})
        if sso_response.status_code == 200:
            global sso_token
            sso_token = sso_response.json()['sso_token']
            resp = make_response(redirect('/protected'))
            resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
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
    tok_resp = requests.get('https://app1-swlzbjlflq-as.a.run.app/getCookie', headers={'appNo': 'app2'})
    tok2_resp = requests.get('https://app3-swlzbjlflq-as.a.run.app/getCookie', headers={'appNo': 'app2'})
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
    # Assuming the app knows its role or fetches it from some configuration
    if token:
        verify_response = requests.get('https://sso-service-swlzbjlflq-as.a.run.app/verify', headers={'appNo': 'app2'}, cookies={'sso_token': token})
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
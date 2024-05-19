from flask import Flask, request, jsonify, redirect, make_response, render_template_string
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app)

users = {
    "user3": {"password": "pass3", "role": "admin"}
}

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
            resp = make_response(redirect('/get_cookie1'))
            resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
            return resp
        return 'SSO Service Error', sso_response.status_code
    return 'Authentication Service Error', auth_response.status_code

@app.route('/protected')
def protected():
    token = request.cookies.get('sso_token')
    # Assuming the app knows its role or fetches it from some configuration
    if token:
        verify_response = requests.get('http://localhost:5000/verify', headers={'appNo': 'app3'}, cookies={'sso_token': token})
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
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('sso_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(port=5103, debug=True)
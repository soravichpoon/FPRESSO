from flask import Flask, request, redirect, make_response, render_template_string, jsonify
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app)

# Simulated user data
users = {
    "user1": {"password": "pass1", "role": "admin"}
}

@app.route('/')
@cross_origin()
def home():
    return render_template_string('''
        <h1>Welcome to App1</h1>
        <form action="/login" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
            <a href="/protected">SSO</a>
        </form>
    ''')

@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    # Send user data to Authentication Service 1
    auth_response = requests.post('http://localhost:5001/authenticate', json={'username': username, 'password': password, 'role': user['role'], 'appNo' : 'app1'})
    if auth_response.status_code == 200:
        # Authenticate with SSO service
        sso_response = requests.get('http://localhost:5000/authenticate', headers={'username':username, 'appNo': 'app1'})
        if sso_response.status_code == 200:
            sso_token = sso_response.json()['sso_token']
            resp = make_response(redirect('/protected'))
            resp.set_cookie('sso_token', sso_token, httponly=True, secure=True, samesite='Lax')
            return resp
        return 'SSO Service Error', sso_response.status_code
    return 'Authentication Service Error', auth_response.status_code

@app.route('/protected')
@cross_origin()
def protected():
    token = request.cookies.get('sso_token')
    # Assuming the app knows its role or fetches it from some configuration
    if token:
        verify_response = requests.get('http://localhost:5000/verify', headers={'appNo': 'app1'}, cookies={'sso_token': token})
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
    resp = make_response(redirect('/'))
    resp.set_cookie('sso_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(port=5101, debug=True)
    
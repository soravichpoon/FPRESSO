from flask import Flask, request, redirect, make_response, render_template_string, jsonify
from flask_cors import CORS, cross_origin
import requests
import os

app = Flask(__name__)
CORS(app)

# Simulated user data
users = {
    "user1": {"password": "pass1", "role": "admin"},
    "user2": {"role": "user"},
    "user3": {"role": "user"}
}

token = {'sso-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcxNDQ1ODAyN30.pryvdAJO8pCO2_I-sfVXOb3TW0FOn7KExwKewMacvso'}

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
    auth_response = requests.post('https://auth-service1-swlzbjlflq-as.a.run.app/authenticate', json={'username': username, 'password': password, 'role': user['role'], 'appNo' : 'app1'})
    if auth_response.status_code == 200:
        # Authenticate with SSO service
        sso_response = requests.get('https://sso-test-swlzbjlflq-as.a.run.app/authenticate', headers={'username':username, 'role': 'admin'})
        if sso_response.status_code == 200:
            sso_token = sso_response.json()['sso_token']
            resp = make_response(redirect('/protected'))
            token.update({'sso-token': sso_token})
            return resp
        return 'SSO Service Error', sso_response.status_code
    return 'Authentication Service Error', auth_response.status_code

@app.route('/protected')
@cross_origin()
def protected():
    sso_token = token['sso-token']
    apps = 'app1'
    # Assuming the app knows its role or fetches it from some configuration
    verify_response = requests.get('https://sso-test-swlzbjlflq-as.a.run.app/verify', headers={'appNo': apps, 'sso_token': sso_token})
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

@app.route('/get_role', methods=['GET'])
def get_role():
    username = request.headers.get('username')
    role = users[username]['role']
    if role:
        return jsonify({'role': role}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/logout')
@cross_origin()
def logout():
    resp = make_response(redirect('/'))
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
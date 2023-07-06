from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load the JSON database
def load_database():
    with open('database.json', 'r') as file:
        return json.load(file)

# Save the JSON database
def save_database(database):
    with open('database.json', 'w') as file:
        json.dump(database, file)

# Home page
@app.route('/')
def home():
    return "Welcome to the home page!"

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check login credentials
        database = load_database()
        if username in database and database[username]['password'] == password:
            return 'Login successful'
        else:
            return 'Login failed'
    return render_template('login.html')

# API endpoint to get user data
@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    database = load_database()
    if username in database:
        return jsonify(database[username])
    else:
        return jsonify({'error': 'User not found'}), 404

# API endpoint to create a new user
@app.route('/api/user', methods=['POST'])
def create_user():
    database = load_database()
    data = request.get_json()
    if data['username'] not in database:
        database[data['username']] = {
            'password': data['password'],
            'email': data['email']
        }
        save_database(database)
        return jsonify({'success': 'User created'})
    else:
        return jsonify({'error': 'User already exists'}), 400

if __name__ == '__main__':
    app.run()

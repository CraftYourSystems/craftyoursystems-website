from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
CORS(app) # Allows your frontend to communicate with this backend

SECRET_KEY = "super_secret_oota_key_change_this_later"

# Database connection settings
db_config = {
    "host": "localhost",
    "database": "testdb",
    "user": "postgres",
    "password": "0000" # UPDATE THIS
}

def get_db_connection():
    return psycopg2.connect(**db_config)


# --- 0. TEST ROUTE ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "OOTA Backend API is running successfully!"}), 200

# --- 1. SIGN UP ROUTE ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return jsonify({"message": "OOTA Account created successfully!"}), 201
    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "Email already exists."}), 400
    finally:
        cursor.close()
        conn.close()

# --- 2. LOGIN ROUTE ---
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Check if user exists and password matches the hash
    if user and check_password_hash(user[0], password):
        # Generate JWT
        token = jwt.encode({
            'userEmail': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({"message": "Login successful", "token": token}), 200
    
    return jsonify({"message": "Invalid email or password"}), 401

# --- 3. MIDDLEWARE TO PROTECT ROUTES ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_email = data['userEmail']
        except:
            return jsonify({"message": "Token is invalid or expired!"}), 401
        
        return f(current_user_email, *args, **kwargs)
    return decorated

# --- 4. SECURE FORM SUBMISSION ROUTE ---
@app.route('/submit-form', methods=['POST'])
@token_required
def submit_form(current_user_email):
    data = request.get_json()
    subject = data.get('subject')
    message = data.get('message')

    # Save the message directly to PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (user_email, subject, message) VALUES (%s, %s, %s)", 
        (current_user_email, subject, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Message securely saved to the database!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
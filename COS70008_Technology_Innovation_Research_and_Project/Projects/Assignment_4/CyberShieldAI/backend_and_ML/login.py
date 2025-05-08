from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal, User

app = Flask(__name__)
# Explicit CORS setup for frontend on localhost:5173
CORS(app, origins=["http://localhost:5173"], methods=["POST", "GET", "OPTIONS"], allow_headers=["Content-Type"])

@app.route('/login', methods=['POST'])
def login():
    db = SessionLocal()
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Input validation
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        # Find the user by email
        user = db.query(User).filter(User.email == email).first()

        if user and user.password == password:
            # Successful login
            return jsonify({
                'message': 'Login successful',
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        print("Login error:", str(e))
        return jsonify({'error': 'Internal server error'}), 500

    finally:
        db.close()


if __name__ == "__main__":
    app.run(port=5000, debug=True)

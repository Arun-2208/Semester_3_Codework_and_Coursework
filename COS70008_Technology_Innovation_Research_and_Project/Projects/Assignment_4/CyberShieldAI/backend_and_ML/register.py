from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal, User

app = Flask(__name__)

# Explicit CORS setup for frontend on localhost:5173
CORS(app, origins=["http://localhost:5173"], methods=["POST", "GET", "OPTIONS"], allow_headers=["Content-Type"])

@app.route('/register', methods=['POST'])
def register():
    db = SessionLocal()
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type', 'regular')

    if not username or not password or not email:
        return jsonify({'error': 'Username, email and password are required'}), 400

    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409

        new_user = User(username=username, email=email, password=password, user_type=user_type)
        db.add(new_user)
        db.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        db.rollback()
        print("Error during registration:", str(e))
        return jsonify({'error': 'Internal server error'}), 500

    finally:
        db.close()

if __name__ == "__main__":
    app.run(port=5000, debug=True)

    

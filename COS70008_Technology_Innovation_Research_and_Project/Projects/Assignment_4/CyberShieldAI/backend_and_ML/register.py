from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import SessionLocal, User

# Define blueprint
register_bp = Blueprint('register_bp', __name__)
CORS(register_bp, origins=["http://localhost:5173"], methods=["POST", "GET", "OPTIONS"], allow_headers=["Content-Type"])

@register_bp.route('/register', methods=['POST'])
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

        created_user = db.query(User).filter_by(email=email).first()

        return jsonify({
            'message': 'Registration successful',
            'user_id': created_user.user_id,
            'username': created_user.username,
            'email': created_user.email,
            'user_type': created_user.user_type
        }), 201
    
    except Exception as e:
        db.rollback()
        print("Error during registration:", str(e))
        return jsonify({'error': 'Internal server error'}), 500

    finally:
        db.close()

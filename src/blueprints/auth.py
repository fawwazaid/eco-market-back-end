from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from db import get_db_connection
import uuid

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    conn = get_db_connection()
    data = request.get_json()
    plain_password = data['password']  # Tidak ada hashing, password disimpan secara langsung

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
            existing_user = cur.fetchone()
            if existing_user:
                return jsonify({'error': 'User with this email already exists.'}), 400

            user_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO users (id, username, email, password, location, role) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, data['username'], data['email'], plain_password, data['location'], data['role'])
            )
            conn.commit()

        return jsonify({'message': 'Registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    data = request.get_json()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
            user = cur.fetchone()
            
            if not user or user['password'] != data['password']:  # Password check
                return jsonify({'error': 'Invalid email or password'}), 401

            # Create tokens
            access_token = create_access_token(identity={'id': str(user['id']), 'username': user['username'], 'role': user['role']})
            refresh_token = create_refresh_token(identity={'id': str(user['id']), 'username': user['username'], 'role': user['role']})
            
            return jsonify({'accessToken': access_token, 'refreshToken': refresh_token, 'id': user['id'], 'username': user['username'], 'role': user['role']}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    
    from flask_jwt_extended import jwt_required, get_jwt_identity

@auth_blueprint.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(accessToken=new_access_token)

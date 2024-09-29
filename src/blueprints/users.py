# blueprints/users.py
from flask import Blueprint, request, jsonify
from db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    conn = get_db_connection()
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET username = %s, email = %s, location = %s WHERE id = %s",
                (data['username'], data['email'], data['location'], str(current_user['id']))
            )
            conn.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

@users_blueprint.route('/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    conn = get_db_connection()
    current_user = get_jwt_identity()

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, email, location, role FROM users WHERE id = %s",
                (str(current_user['id']),)
            )
            user = cur.fetchone()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify({
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'location': user['location'],
                'role': user['role']
            }), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

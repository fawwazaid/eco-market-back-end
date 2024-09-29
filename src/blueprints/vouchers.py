from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection
import uuid
from role_checker import role_required

vouchers_blueprint = Blueprint('vouchers', __name__)

@vouchers_blueprint.route('/vouchers', methods=['POST'])
@jwt_required()
@role_required('seller')
def create_voucher():
    conn = get_db_connection()
    current_user = get_jwt_identity()

    try:
        data = request.get_json()
        voucher_id = str(uuid.uuid4())

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO vouchers (id, code, discount, seller_id) VALUES (%s, %s, %s, %s)",
                (voucher_id, data['code'], data['discount'], str(current_user['id']))
            )
            conn.commit()

        return jsonify({'message': 'Voucher created successfully'}), 201
    except Exception as e:
        print(f"Error occurred during voucher creation: {e}")  # Debug log
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    finally:
        conn.close()

@vouchers_blueprint.route('/vouchers', methods=['GET'])
@jwt_required()
def get_vouchers():
    conn = get_db_connection()
    current_user = get_jwt_identity()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, code, discount, seller_id FROM vouchers WHERE seller_id = %s", (str(current_user['id']),))
            vouchers = cur.fetchall()

            print(f"Vouchers fetched: {vouchers}")  # Debug log

            formatted_vouchers = [
                {
                    "id": str(voucher['id']),
                    "code": voucher['code'],
                    "discount": voucher['discount'],
                    "seller_id": str(voucher['seller_id'])
                }
                for voucher in vouchers
            ]

            return jsonify(formatted_vouchers), 200
    except Exception as e:
        print(f"Error occurred during fetching vouchers: {e}")  # Debug log
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    finally:
        conn.close()


@vouchers_blueprint.route('/vouchers/<uuid:voucher_id>', methods=['DELETE'])
@jwt_required()
@role_required('seller')
def delete_voucher(voucher_id):
    conn = get_db_connection()
    current_user = get_jwt_identity()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM vouchers WHERE id = %s AND seller_id = %s", (str(voucher_id), str(current_user['id'])))
            voucher = cur.fetchone()

            if not voucher:
                return jsonify({'error': 'Voucher not found or you do not have permission to delete this voucher.'}), 404

            cur.execute("DELETE FROM vouchers WHERE id = %s", (str(voucher_id),))
            conn.commit()

        return jsonify({'message': 'Voucher deleted successfully'}), 200
    except Exception as e:
        print(f"Error occurred during deleting voucher: {e}")  # Debug log
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    finally:
        conn.close()

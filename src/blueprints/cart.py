from flask import Blueprint, request, jsonify
from db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

cart_blueprint = Blueprint('cart', __name__)

@cart_blueprint.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    conn = get_db_connection()
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        cart_id = str(uuid.uuid4())
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (str(data['product_id']),))
            product = cur.fetchone()
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            if product['quantity'] < data['quantity']:
                return jsonify({'error': 'Not enough quantity available'}), 400

            cur.execute(
                "INSERT INTO cart (id, customer_id, product_id, quantity) VALUES (%s, %s, %s, %s)",
                (cart_id, str(current_user['id']), str(data['product_id']), data['quantity'])
            )
            conn.commit()
        return jsonify({'message': 'Added to cart successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    finally:
        conn.close()

@cart_blueprint.route('/cart', methods=['GET'])
@jwt_required()
def get_cart_items():
    conn = get_db_connection()
    current_user = get_jwt_identity()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM cart WHERE customer_id = %s", (str(current_user['id']),))
            cart_items = cur.fetchall()

            if not cart_items:
                return jsonify({'message': 'Your cart is empty'}), 200

            formatted_cart_items = [
                {
                    "id": str(item['id']),
                    "product_id": str(item['product_id']),
                    "quantity": item['quantity']
                }
                for item in cart_items
            ]

            return jsonify(formatted_cart_items), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    finally:
        conn.close()

@cart_blueprint.route('/cart/checkout', methods=['POST'])
@jwt_required()
def checkout():
    conn = get_db_connection()
    current_user = get_jwt_identity()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM cart WHERE customer_id = %s", (str(current_user['id']),))
            cart_items = cur.fetchall()
            if not cart_items:
                return jsonify({'error': 'Cart is empty'}), 400

            for item in cart_items:
                cur.execute("SELECT * FROM products WHERE id = %s", (str(item['product_id']),))
                product = cur.fetchone()
                if product['quantity'] < item['quantity']:
                    return jsonify({'error': f'Not enough {product["name"]} in stock'}), 400

                cur.execute(
                    "UPDATE products SET quantity = quantity - %s WHERE id = %s",
                    (item['quantity'], str(item['product_id']))
                )

            cur.execute("DELETE FROM cart WHERE customer_id = %s", (str(current_user['id']),))
            conn.commit()
        return jsonify({'message': 'Checkout successful'}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
    finally:
        conn.close()

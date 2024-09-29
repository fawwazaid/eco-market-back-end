# services/cart_service.py
def add_to_cart(conn, customer_id, product_id, quantity):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)", 
                    (customer_id, product_id, quantity))
        conn.commit()

def get_cart_items(conn, customer_id):
    with conn.cursor() as cur:
        cur.execute("SELECT cart.*, products.name, products.price FROM cart "
                    "JOIN products ON cart.product_id = products.id "
                    "WHERE customer_id = %s", (customer_id,))
        return cur.fetchall()

def delete_cart_items(conn, customer_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM cart WHERE customer_id = %s", (customer_id,))
        conn.commit()

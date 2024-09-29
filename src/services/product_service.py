# services/product_service.py
def get_all_products(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM products")
        return cur.fetchall()

def add_product(conn, product_id, name, description, price, quantity, category, seller_id):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO products (id, name, description, price, quantity, category, seller_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s)", 
                    (product_id, name, description, price, quantity, category, seller_id))
        conn.commit()

def update_product(conn, product_id, name, description, price, quantity, category, seller_id):
    with conn.cursor() as cur:
        cur.execute("UPDATE products SET name = %s, description = %s, price = %s, quantity = %s, "
                    "category = %s WHERE id = %s AND seller_id = %s", 
                    (name, description, price, quantity, category, product_id, seller_id))
        conn.commit()

def delete_product(conn, product_id, seller_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE id = %s AND seller_id = %s", (product_id, seller_id))
        conn.commit()

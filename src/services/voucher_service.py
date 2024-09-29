# services/voucher_service.py
def create_voucher(conn, code, discount, seller_id):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO vouchers (code, discount, seller_id) VALUES (%s, %s, %s)", 
                    (code, discount, seller_id))
        conn.commit()

def get_voucher_by_code(conn, code):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM vouchers WHERE code = %s", (code,))
        return cur.fetchone()

# services/user_service.py
class UserAlreadyExistsError(Exception):
    pass

def create_user(conn, username, email, password, location, role):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {email} already exists.")
        
        cur.execute(
            "INSERT INTO users (username, email, password, location, role) VALUES (%s, %s, %s, %s, %s)",
            (username, email, password, location, role)
        )
        conn.commit()

def get_user_by_email(conn, email):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cur.fetchone()

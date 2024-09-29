# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blueprints.auth import auth_blueprint
from blueprints.products import products_blueprint
from blueprints.vouchers import vouchers_blueprint
from blueprints.cart import cart_blueprint
from blueprints.users import users_blueprint
from config import Config
from db import get_db_connection, close_db_connection

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
jwt = JWTManager(app)

app.teardown_appcontext(close_db_connection)

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(products_blueprint)
app.register_blueprint(vouchers_blueprint)
app.register_blueprint(cart_blueprint)
app.register_blueprint(users_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

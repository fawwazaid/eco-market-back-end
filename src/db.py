# db.py
from flask import g
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    if 'db' not in g:
        g.db = psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
    return g.db

def close_db_connection(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

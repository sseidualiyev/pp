
import psycopg2
from psycopg2 import OperationalError
from config import DB_CONFIG


def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to PostgreSQL")
        return conn

    except OperationalError as e:
        print("❌ Connection error:")
        print(e)
        return None
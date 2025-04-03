import bcrypt
from db_connection import get_connection
import mysql.connector


def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Hash password before storing
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users_data (username, password) VALUES (%s, %s)", 
                       (username, hashed_pw))
        conn.commit()
        return "User registered successfully!"
    except mysql.connector.IntegrityError:
        return "Username already exists!"
    finally:
        cursor.close()
        conn.close()



def validate_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users_data WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return True
    return False


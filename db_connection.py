import mysql.connector
import bcrypt

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mayur@123",
        database="movie_recommendation_system",
        auth_plugin="mysql_native_password"  # Ensure correct authentication method
    )

# Test the connection
try:
    conn = get_connection()
    print("✅ Connection successful!")
    conn.close()  # Close connection after testing
except mysql.connector.Error as err:
    print(f"❌ Connection failed: {err}")

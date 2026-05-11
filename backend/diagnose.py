import sys
import os

print("=" * 60)
print("SV ExamShield - System Diagnostic")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check MySQL connector
try:
    import mysql.connector
    print("✓ mysql-connector-python: Installed")
except:
    print("✗ mysql-connector-python: NOT INSTALLED")

# Check FastAPI
try:
    import fastapi
    print("✓ FastAPI: Installed")
except:
    print("✗ FastAPI: NOT INSTALLED")

# Check .env file
if os.path.exists('.env'):
    print("✓ .env file: Found")
else:
    print("✗ .env file: NOT FOUND")

# Try database connection
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    import mysql.connector
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'proctoring_db')
    )
    
    if conn.is_connected():
        print("✓ Database connection: SUCCESS")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✓ Tables found: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        conn.close()
    else:
        print("✗ Database connection: FAILED")
        
except Exception as e:
    print(f"✗ Database connection: FAILED")
    print(f"  Error: {e}")

print("\n" + "=" * 60)
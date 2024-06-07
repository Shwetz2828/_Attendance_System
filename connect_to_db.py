from sqlalchemy import create_engine  # SQLAlchemy function for creating database engine


# Replace 'username', 'password', 'database_name' with your actual credentials
engine = create_engine('mysql+mysqlconnector://username:password@localhost:3307/database_name')

# Now try to connect to the database
try:
    conn = engine.connect()
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

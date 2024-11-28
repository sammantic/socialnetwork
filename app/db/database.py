from psycopg2 import sql, connect, Error

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

HOST = "db"
USER = "admin"
PASSWORD = "admin"
PORT = "5432"
DATABASE_NAME = "socialnetwork"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"


# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for all models
Base = declarative_base()


def create_database_if_not_exists():
    """
    Create database if not exist
    :return:
    """
    
    try:
        # Connect to the default 'postgres' database
        connection = connect(
            dbname="postgres",
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )

        # Set autocommit to True to allow CREATE DATABASE to execute outside of a transaction
        connection.autocommit = True

        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (DATABASE_NAME,)
        )
        exists = cursor.fetchone()

        if not exists:
            # Create the database if it doesn't exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))
            print(f"Database '{DATABASE_NAME}' created successfully.")
        else:
            print(f"Database '{DATABASE_NAME}' already exists.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
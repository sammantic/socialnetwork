from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://admin:admin@db/socialnetwork"


# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for all models
Base = declarative_base()


def create_database_if_not_exists():
    """
    Create the database socialnetwrok if it does not exist

    :return:
    """

    base_url = DATABASE_URL.rsplit("/", 1)[0] + '/postgres'
    database_name = DATABASE_URL.rsplit("/", 1)[-1]

    # Create a temp engine
    temp_engine = create_engine(base_url)

    with temp_engine.connect() as connection:

        # Check the database if the database exists
        result = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": database_name}
        )

        if not result.fetchone():
            # create the database
            connection.execute(text(f"CREATE DATABASE {database_name}"))
            print("INFO: Database created successfully.")
        else:
            print("INFO: Database already exist")

    temp_engine.dispose()


# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
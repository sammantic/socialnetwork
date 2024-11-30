from psycopg2 import sql, connect, Error


def create_database_if_not_exists(db_name: str, host: str, port: str, user: str, password: str):
    """
    Create database if not exist
    :return:
    """
    try:
        # Connect to the default 'postgres' database
        connection = connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Set autocommit to True to allow CREATE DATABASE to execute outside of a transaction
        connection.autocommit = True

        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (db_name,)
        )
        exists = cursor.fetchone()

        if not exists:
            # Create the database if it doesn't exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
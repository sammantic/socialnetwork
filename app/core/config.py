from app.core.database.config_loader import get_setting

DB_HOST = get_setting("database", "host")
DB_PORT = get_setting("database", "port")
DB_USER = get_setting("database", "user")
DB_PASSWORD = get_setting("database", "password")
DB_NAME = get_setting("database", "name")


def get_database_url(db_name: str = DB_NAME) -> str:
    """
    Build a dynamic database connection URL

    :param db_name: database name
    :return:
    str: a database connection url
    """
    return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
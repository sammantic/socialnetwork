from app.core.database.config_loader import get_config


config = get_config()

DB_HOST = config.host
DB_PORT = config.port
DB_USER = config.user_db
DB_PASSWORD = config.password
DB_NAME = config.name


def get_database_url(db_name: str = DB_NAME) -> str:
    """
    Build a dynamic database connection URL

    :param db_name: database name
    :return:
    str: a database connection url
    """

    return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
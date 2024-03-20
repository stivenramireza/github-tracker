from src.config.database import Database


def manager(func: object) -> object:
    def wrapper(event: dict, ctx: tuple) -> object:
        db = Database()

        try:
            conn, cursor = db.get_connection()
            ctx = (conn, cursor)
            return func(event, ctx)
        finally:
            db.close_connection()

    return wrapper

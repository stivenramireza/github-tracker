from src.config.database import Database


def main() -> None:
    database = Database()
    database.get_connection()
    database.close_connection()


if __name__ == '__main__':
    main()

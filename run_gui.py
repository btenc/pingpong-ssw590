from app.database import create_tables
from app.server.main import app


def main():
    create_tables()
    app.run()


if __name__ == "__main__":
    main()

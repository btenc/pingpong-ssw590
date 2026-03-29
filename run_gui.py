from app.database import create_tables
from app.web import app


def main():
    create_tables()
    app.run()


if __name__ == "__main__":
    main()

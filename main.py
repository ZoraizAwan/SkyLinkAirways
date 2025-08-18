from database.db_setup import create_all
from presentation.cli import menu

if __name__ == "__main__":
    # ensure database/tables exist
    create_all()
    # start CLI
    menu()
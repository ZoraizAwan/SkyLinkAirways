from database.db_setup import create_all
from presentation.cli import main as cli_main
from security.auth import create_admin_if_missing

if __name__ == "__main__":
    # ensure database/tables exist
    create_all()
    # ensure there is at least one admin user
    create_admin_if_missing()
    # start CLI
    cli_main()
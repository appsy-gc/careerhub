from flask import Blueprint
from init import db
from models.cpartners import Partner

# With this line, must use flask db create, or flask db drop...etc in the terminal
db_commands = Blueprint("db", __name__)

# CLI command to create tables
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

# CLI command to drop all tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

# CLI command to seed tables
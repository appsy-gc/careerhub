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
@db_commands.cli.command("seed")
def seed_tables():
    partners = [
        Partner(
            name = "Neva Flynn",
            club = "Fitness First",
            address = "Fitness First Balgowlah Platinum, Condamine Street, Balgowlah NSW, Australia",
            email = "balgowlahplatinumptm@fitnessfirst.com.au"
        ),
        Partner(
            name = "Danielle Walker",
            club = "Goodlife",
            address = "Goodlife Health Clubs Point Cook, Centre, Main Street, Point Cook VIC, Australia",
            email = "ptmpointcook@goodlife.com.au"
        )
    ]

    db.session.add_all(partners)
    db.session.commit()
    print("Tables seeded")
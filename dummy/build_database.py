import os
from dummy.config import db


def create_db():
    # Delete database file if it exists currently
    if os.path.exists("rate.db"):
        os.remove("rate.db")

    # Create the database
    db.create_all()

from flask import make_response, abort
from dummy.config import db
from dummy.models import Rate, RateSchema


def read_rate():
    # Query the database for all the notes
    rate = Rate.query.all()

    # Serialize the list of notes from our data
    rate_schema = RateSchema(many=True)
    data = rate_schema.dump(rate)
    return data
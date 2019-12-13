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


def delete_rate(id):
    delete_rate = Rate.query.filter(Rate.id == id).one_or_none()

    if delete_rate is None:
        abort(
            404,
            "Record not found for Id: {id}".format(id=id),
        )

    else:
        db.session.delete(delete_rate)
        db.session.commit()

        return "Record is deleted"

def check_current_rates(names):
    current_rates = {}
    for name in names:
        current = 0
        record = Rate.query.filter(Rate.name == name).one_or_none()
        if record is None:
            current = 1000
        else:
            current = record.rate
        current_rates[name] = current
    return current_rates

def update_rate(update_rate_dict):
    for record in update_rate_dict:
        current_record = Rate.query.filter(Rate.name == record).one_or_none()
        new_record = Rate(name=record, rate=update_rate_dict[record])
        if current_record is None:
            db.session.add(new_record)
            db.session.commit()
        else:
            new_record.id = current_record.id

            db.session.merge(new_record)
            db.session.commit()

def delete_all_rates():
    rates = Rate.query.filter(Rate.rate!=1000).all()
    for rate in rates: 
        db.session.add(rate)
    db.session.commit()
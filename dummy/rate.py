import csv
from io import StringIO
from dummy.config import db
from dummy.models import Rate, RateSchema
from werkzeug import Response


def read_rate():
    # Query the database for all the notes
    rate = Rate.query.all()

    # Serialize the list of notes from our data
    rate_schema = RateSchema(many=True)
    data = rate_schema.dump(rate)
    return data


def get_rate_file():
    response = Response(generate_file(), mimetype='text/csv')
    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename="rate.csv")
    return response


def check_current_rates(names):
    current_rates = {}
    for name in names:
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
    Rate.__table__.drop(db.engine)
    db.session.commit()
    Rate.__table__.create(db.session.bind)
    db.session.commit()


def generate_file():
    # Query the database for all the notes
    rate = Rate.query.all()

    # Serialize the list of notes from our data
    rate_schema = RateSchema(many=True)
    rate_data = rate_schema.dump(rate)

    data = StringIO()
    w = csv.writer(data)

    # write header
    w.writerow(('Гравець', 'Рейтинг'))
    yield data.getvalue()
    data.seek(0)
    data.truncate(0)

    # write each rate item
    for item in rate_data:
        w.writerow((
            item["name"],
            item["rate"]
        ))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

from flask import make_response, abort
from dummy.config import db
from dummy.models import Result, ResultSchema


def read_results():
    # Query the database for all the notes
    result = Result.query.all()

    # Serialize the list of notes from our data
    result_schema = ResultSchema(many=True)
    data = result_schema.dump(result)
    return data


def add_result(results):
    for result in results:
        match_id = result.get("match_id")
        name = result.get("name")
        points = result.get("points")
        date = result.get("date")
    
        schema = ResultSchema()
        new_result = schema.load(result, session=db.session)

        db.session.add(new_result)
        db.session.commit()
    
    return "Result is added successfully"


def replace_result():
    return {'coming':'soon'}


def delete_result():
    return {'coming':'soon'}
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

def add_result():
    return {'coming':'soon'}

def replace_result():
    return {'coming':'soon'}

def delete_result():
    return {'coming':'soon'}
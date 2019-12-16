from flask import make_response, abort
from dummy.config import db
from dummy.models import Result, ResultSchema
from dummy.rate import delete_all_rates
from dummy.calculator import calculate_rate


def read_results():
    # Query the database for all the notes
    result = Result.query.all()

    # Serialize the list of notes from our data
    result_schema = ResultSchema(many=True)
    data = result_schema.dump(result)
    return data


def add_result(body):
    matches = set()

    for result_array in body:
        for result in result_array:
            match_id = result.get("match_id")
            name = result.get("name")
            points = result.get("points")
            date = result.get("date")

            matches.add(match_id)
    
            schema = ResultSchema()
            new_result = schema.load(result, session=db.session)

            db.session.add(new_result)
            db.session.commit()

    calculate_rate(matches)
        
    
    return "Result is added successfully"


def replace_result(body):
    result_id = body.get("result_id")
    match_id = body.get("match_id")
    name= body.get("name")
    points = body.get("points")
    date = body.get("date")
    
    update_result = Result.query.filter(
        Result.result_id == result_id
    ).one_or_none()

    if update_result is None:
        abort(
            404,
            "Result not found for Id: {result_id}".format(result_id=result_id),
        )

    else:
        schema = ResultSchema()
        update = schema.load(body, session=db.session)

        update.result_id = update_result.result_id
        db.session.merge(update)
        delete_all_rates()

        calculate_rate(select_all_matches())

        db.session.commit()

        return "Record is updated"


def delete_result(result_id):
    delete_result = Result.query.filter(
        Result.result_id == result_id
    ).one_or_none()

    if delete_result is None:
        abort(
            404,
            "Result not found for Id: {result_id}".format(result_id=result_id),
        )

    else:
        db.session.delete(delete_result)
        delete_all_rates()

        calculate_rate(select_all_matches())

        db.session.commit()

        return "Record is deleted"


def select_all_matches():
    matches = set()

    all_matches = Result.query.all()

    for item in all_matches:
        matches.add(item.match_id)
        print(item.match_id)

    return matches

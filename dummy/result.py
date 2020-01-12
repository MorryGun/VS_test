from io import StringIO
import csv
from datetime import datetime
from flask import abort
from dummy.config import db
from dummy.models import Result, ResultSchema
from dummy.rate import delete_all_rates
from dummy.calculator import calculate_rate, calculate_rates


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

            matches.add(match_id)
    
            schema = ResultSchema()
            new_result = schema.load(result, session=db.session)

            db.session.add(new_result)
            db.session.commit()

    calculate_rates(matches)

    return "Result is added successfully"


def replace_result(body):
    result_id = body.get("result_id")
    
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
        db.session.commit()

        delete_all_rates()
        calculate_rates(select_all_matches())

        return "Record is updated"


def delete_result(result_id):
    result_to_delete = Result.query.filter(
        Result.result_id == result_id
    ).one_or_none()

    if result_to_delete is None:
        abort(
            404,
            "Result not found for Id: {result_id}".format(result_id=result_id),
        )

    else:
        db.session.delete(result_to_delete)
        db.session.commit()

        delete_all_rates()
        calculate_rates(select_all_matches())

        return "Record is deleted"


def upload(upfile):
    if ".csv" not in upfile.filename:
        abort(
            404,
            "Incorrect file extension. Expected: .csv",
        )
    add_results_from_file(upfile)
    return "File uploaded successfully"


def select_all_matches():
    matches = set()

    all_matches = Result.query.all()

    for item in all_matches:
        matches.add(item.match_id)

    return matches


def add_results_from_file(file_storage):
    matches = set()

    result_id = check_current_result_id()
    match_id = check_current_match_id()

    file_data = StringIO(file_storage.read().decode("utf-8"))
    reader = csv.reader(file_data, delimiter=',')

    for row in reader:
        if all(not item for item in row):
            #calculate_rate(match_id)
            match_id += 1
        else:
            result = Result()
            result.result_id = result_id
            result.match_id = match_id
            result.name = row[0]
            result.points = int(row[1])
            result.date = datetime.strptime(row[2], '%Y-%m-%d')

            schema = ResultSchema()
            dumped_result = schema.dump(result)
            new_result = schema.load(dumped_result, session=db.session)

            result_id += 1
            matches.add(match_id)

            db.session.add(new_result)
            db.session.commit()
    calculate_rates(matches)


def check_current_match_id():
    all_matches = Result.query.all()
    if len(all_matches) > 0:
        return max(item.match_id for item in all_matches)+1
    else:
        return 1


def check_current_result_id():
    all_matches = Result.query.all()
    if len(all_matches) > 0:
        return max(item.result_id for item in all_matches)+1
    else:
        return 1

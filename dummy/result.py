from flask import make_response, abort
from dummy.config import db
from dummy.models import Result, ResultSchema
from dummy.rate import check_current_rates, update_rate


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
    matches = set()

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

        matches.add(update_result.match_id)
        calculate_rate(matches)

        update.result_id = update_result.result_id

        db.session.merge(update)
        db.session.commit()

        return "Record is updated"


def delete_result(result_id):
    matches = set()

    delete_result = Result.query.filter(
        Result.result_id == result_id
    ).one_or_none()

    if delete_result is None:
        abort(
            404,
            "Result not found for Id: {result_id}".format(result_id=result_id),
        )

    else:
        matches.add(delete_result.match_id)
        calculate_rate(matches)
        db.session.delete(delete_result)
        db.session.commit()

        return "Record is deleted"

def calculate_rate(matches):
    names = []
    for match_id in matches:

        # Create dict current_rates with names and current rates of the players by match_id
        # Create list points with points of the player

        selected_matches = Result.query.filter(Result.match_id == match_id).all()

        points = []
        players_points = {}

        for selected_match in selected_matches:
            names.append(selected_match.name)
            points.append(selected_match.points)
            players_points[selected_match.name] = selected_match.points

        current_rates = check_current_rates(names)

        # Calculate prize fond and sum of points for current match

        fond = 0
        for rate in current_rates:
            fond = fond + current_rates[rate]*0.25


        sum_of_game_points = 0
        min_point = min(points) if min(points) < 0 else 0
        for point in points:
            sum_of_game_points = sum_of_game_points + point - min_point

        # Calculate final rate after the match

        if sum_of_game_points != 0:
            for rate in current_rates:
                prize = fond*(players_points[rate]-min_point)/sum_of_game_points
                current_rates[rate] = round(0.75 * current_rates[rate] + prize)

        # Update rates in rate table

        update_rate(current_rates)


from dummy.models import Result, ResultSchema
from dummy.rate import check_current_rates, update_rate


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

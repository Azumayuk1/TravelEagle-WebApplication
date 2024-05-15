def calculate_approximate_travel_time(distance_to_place):
    average_speed_per_hour = 60000
    if distance_to_place > 0:
        return f"{round(60 * distance_to_place / average_speed_per_hour, 1)} минут"
    else:
        return ''


3

def calculate_nights(check_in_date, check_out_date):
    return (check_out_date - check_in_date).days


def calculate_total_price(room_price, num_rooms, check_in_date, check_out_date):
    return room_price * num_rooms * calculate_nights(check_in_date, check_out_date)


def calculate_points(total_price):
    return int(total_price / 1000)

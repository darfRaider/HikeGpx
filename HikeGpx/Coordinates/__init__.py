def prettify_degree(deg: float) -> str:
    degrees = int(deg)
    minutes_decimal = (deg-degrees)*60
    minutes = int(minutes_decimal)
    seconds = round((minutes_decimal-minutes)*60,2)
    return f"{degrees}° {minutes}' {seconds}\""
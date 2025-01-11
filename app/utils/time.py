from datetime import datetime, timedelta


def uuid1_time_to_datetime(time: int) -> datetime:
    """
    Convert a UUID1 timestamp to a datetime object.
    UUID1 timestamps are based on the number of 100-nanosecond intervals
    since 00:00:00.00, 15 October 1582 (the date of the Gregorian calendar reform). \n
    Args:
        time (int): The UUID1 timestamp.
    Returns:
        datetime: The corresponding datetime object.
    """
    return datetime(1582, 10, 15) + timedelta(microseconds=time // 10)

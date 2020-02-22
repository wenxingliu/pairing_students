import datetime as dt
import pytz


def compute_timezone_utc_offset_dict():
    time_zone_list = [
        "Eastern",
        "Central",
        "Mountain",
        "Pacific"
    ]

    utc_offset_dict = {}

    for time_zone in time_zone_list:
        utc_offset = _compute_utc_offset_for_timezone(time_zone)
        utc_offset_dict[time_zone] = utc_offset

    return utc_offset_dict


def _compute_utc_offset_for_timezone(timezone_name: str) -> int:
    tz_now = dt.datetime.now(pytz.timezone(f'US/{timezone_name}'))
    utc_offset = tz_now.utcoffset().total_seconds() / 60 / 60
    return utc_offset

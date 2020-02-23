from collections import Counter
import datetime as dt
from typing import List

import pandas as pd

from models.requestee import Requestee
from models.time_slot import TimeSlot, TimeSlotList
from services.utils.common import (invalid_wechat,
                                   cleanup_time_slot_day,
                                   compute_time_part_from_str,
                                   assign_scarcity_metrics_to_person_and_time_slot)


def cleanup_utc_time_slots_requestee(time_str: str, day_int: str) -> TimeSlotList:
    day_int = cleanup_time_slot_day(day_int)

    time_slots_str_list = time_str.split(',')
    time_slots_cleaned = [_cleanup_time_slot_str_requestee(time_slot_str, day_int)
                          for time_slot_str in time_slots_str_list]

    return TimeSlotList(time_slots_cleaned)


def _cleanup_time_slot_str_requestee(time_slot_str: str, day_int: int) -> TimeSlot:
    afternoon = False
    if '晚上' in time_slot_str:
        afternoon = True

    time_slot_str_cleaned = time_slot_str.split('早上 ')[-1].split('晚上 ')[-1].split('（仅限周末）')[0].replace(' ', '')

    start_str, end_str = time_slot_str_cleaned.split('-')

    start = compute_time_part_from_str(start_str)
    end = compute_time_part_from_str(end_str)

    if afternoon:
        start = start + dt.timedelta(hours=12)
        end = end + dt.timedelta(hours=12)

    time_slot = TimeSlot(start=start, end=end, weekday=day_int)

    return time_slot


def compute_request_scarcity_index(request_df: pd.DataFrame) -> pd.DataFrame:
    scarcity_dict = _compute_request_scarcity(request_df)
    request_df['scarcity_index'] = request_df.time_slots_china.apply(
        lambda x: assign_scarcity_metrics_to_person_and_time_slot(x, scarcity_dict))
    return request_df


def _compute_request_scarcity(request_df: pd.DataFrame) -> dict:
    scarcity_dict = Counter([time_slot for data_tuple in request_df.itertuples()
                             for time_slot in data_tuple.time_slots_china])
    return scarcity_dict


def compute_requestees(requestee_df: pd.DataFrame) -> List[Requestee]:
    requestees = []

    for data_row in requestee_df.iterrows():
        requestee_info = data_row[1]
        requestee = Requestee(requestee_info)
        requestees.append(requestee)

    sorted_requestees = sorted(requestees, key=lambda s: s.priority)

    return sorted_requestees

from collections import Counter
import datetime as dt
from typing import List, Set

import pandas as pd

from models.requestee import Requestee
from models.paired_info import PairedInfo
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


def _previous_pairing_info(requestee: Requestee,
                           existing_pairs: Set[PairedInfo]) -> PairedInfo:
    previous_paired_info = None
    for paired_info in existing_pairs:
        if paired_info.requestee_wechat == requestee.parent_wechat:
            previous_paired_info = paired_info
    return previous_paired_info


def compute_requestees(requestee_df: pd.DataFrame,
                       existing_pairs: Set[PairedInfo]) -> List[Requestee]:
    requestees = []

    for requestee_info in requestee_df.reset_index().T.to_dict().values():
        requestee = Requestee(requestee_info)

        prev_pairing_info = _previous_pairing_info(requestee, existing_pairs)

        # never paired
        if prev_pairing_info is None:
            requestees.append(requestee)
        # paired and successfull
        elif prev_pairing_info.valid:
            print(f"Request {requestee} already paired, and valid")
        # paired but not successful
        else:
            requestees.append(requestee)
            requestee.existing_pairing_info = prev_pairing_info
            print(f"Request {requestee} paired, but failed to connect")

    sorted_requestees = sorted(requestees, key=lambda s: s.priority)

    return sorted_requestees

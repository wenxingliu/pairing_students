from collections import Counter
import datetime as dt
from typing import List, Set

import pandas as pd

import settings as settings
from models.time_slot import TimeSlot, TimeSlotList
from models.paired_info import PairedInfo
from models.volunteer import Volunteer
from services.utils.common import (cleanup_time_slot_day,
                                   compute_time_part_from_str,
                                   assign_scarcity_metrics_to_person_and_time_slot)


def compute_available_time_slots_volunteer(data_row) -> TimeSlotList:
    volunteer_time_slots = []
    for col in settings.VOLUNTEER_TIME_SLOT_COLS:
        time_slot_str = data_row[col]
        time_slot_day = cleanup_time_slot_day(col)
        if pd.notnull(time_slot_str):
            time_slot_list = _cleanup_time_slot_time_volunteer(time_slot_str, time_slot_day)
            volunteer_time_slots += time_slot_list
    return TimeSlotList(volunteer_time_slots)


def compute_volunteer_scarcity_index(volunteer_df: pd.DataFrame) -> pd.DataFrame:
    scarcity_dict = _compute_volunteer_scarcity(volunteer_df)
    volunteer_df['scarcity_index'] = volunteer_df.time_slots_local.apply(
        lambda x: assign_scarcity_metrics_to_person_and_time_slot(x, scarcity_dict,
                                                                  class_type='volunteer')
    )
    return volunteer_df


def _compute_volunteer_scarcity(request_df: pd.DataFrame) -> dict:
    scarcity_dict = Counter([time_slot for data_tuple in request_df.itertuples()
                             for time_slot in data_tuple.time_slots_local])
    return scarcity_dict


def _cleanup_time_slot_time_volunteer(time_str: str, day_int: int) -> List[TimeSlot]:
    time_slots_str_list = time_str.split(',')
    time_slots_cleaned = [_clean_time_slot_str_volunteer(time_slot_str, day_int)
                          for time_slot_str in time_slots_str_list]
    return time_slots_cleaned


def _clean_time_slot_str_volunteer(time_slot_str: str, day_int: int) -> TimeSlot:
    time_slot_str = time_slot_str.lower()
    afternoon = "pm" in time_slot_str
    time_slot_str = time_slot_str.replace("pm", "").replace("am", "").replace(" ", "")
    start_str, end_str = time_slot_str.split("-")
    start_str = _complete_time_string(start_str)
    end_str = _complete_time_string(end_str)

    start = compute_time_part_from_str(start_str)
    end = compute_time_part_from_str(end_str)

    if afternoon:
        start = start + dt.timedelta(hours=12)
        end = end + dt.timedelta(hours=12)

    day_num = int(day_int)

    time_slot = TimeSlot(start=start, end=end, weekday=day_num)
    return time_slot


def _complete_time_string(time_str):
    if ":" not in time_str:
        time_str = f"{time_str}:00"
    return time_str


def _email_match(paired_info: PairedInfo, volunteer: Volunteer) -> bool:
    paired_emails = set([paired_info.volunteer_parent_email, paired_info.volunteer_email])
    volunteer_emails = set([volunteer.volunteer_email, volunteer.parent_email])
    common_email_address = set(paired_emails).intersection(volunteer_emails)
    return len(common_email_address) > 0


def _not_paired(volunteer: Volunteer,
                existing_pairs: Set[PairedInfo]) -> bool:
    previous_paired_info = None
    for paired_info in existing_pairs:
        if _email_match(paired_info, volunteer):
            previous_paired_info = paired_info
            # if volunteer.name == paired_info.volunteer_name:
            #     previous_paired_info = paired_info
            # else:
            #     print(f'Potential duplicate {volunteer.name} {volunteer.volunteer_email}')

    return previous_paired_info is None


def compute_volunteers(volunteer_df: pd.DataFrame,
                       existing_pairs: Set[PairedInfo]) -> List[Volunteer]:
    volunteers = []

    for volunteer_info in volunteer_df.reset_index().T.to_dict().values():
        volunteer = Volunteer(volunteer_info)

        if _not_paired(volunteer, existing_pairs):
            volunteers.append(volunteer)
        else:
            print(f"Volunteer {volunteer} already paired")

    volunteers = sorted(volunteers, key=lambda v: v.age)
    return volunteers

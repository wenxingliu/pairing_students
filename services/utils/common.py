import datetime as dt
import pandas as pd
from typing import List

import settings as settings


def dedup_dataframe(df: pd.DataFrame, idx_cols: List[str]) -> pd.DataFrame:
    df.sort_values('timestamp', inplace=True)
    for col in idx_cols:
        df[col] = df[col].apply(lambda x: str(x).lower())
    df.drop_duplicates(idx_cols, keep='last', inplace=True)
    return df


def convert_bool_to_int(str_val: str) -> int:
    try:
        if str_val.lower() in ['否', 'no', 'n']:
            return 0
        elif str_val.lower() in ['是', 'yes', 'y']:
            return 1
        else:
            return None
    except AttributeError:
        return None


def cleanup_gender(gender_val: str) -> str:
    try:
        if gender_val.lower() in ['男', 'male', 'm', 'boy', 'b']:
            return 'm'
        elif gender_val.lower() in ['女', 'female', 'f', 'girl', 'g']:
            return 'f'
        else:
            return None
    except AttributeError:
        return None


def get_digits(digit_str: str) -> int:
    cleaned_str = ''.join([i for i in str(digit_str) if i.isdigit()])
    try:
        return int(cleaned_str)
    except ValueError:
        return None


def cleanup_time_slot_day(day_str: str) -> int:
    MAPPER = {
        '周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4, '周六': 5, '周日': 6,
        'Available Weekday and time(Local time) [M (choose one or more)]': 0,
        'Available Weekday and time(Local time) [T (choose one or more)]': 1,
        'Available Weekday and time(Local time) [W (choose one or more)]': 2,
        'Available Weekday and time(Local time) [Th (choose one or more)]': 3,
        'Available Weekday and time(Local time) [F (choose one or more)]': 4,
        'Available Weekend and time(Local time) [Sat (choose one or more)]': 5,
        'Available Weekend and time(Local time) [Sun (choose one or more)]': 6
    }
    return MAPPER.get(day_str)


def compute_time_part_from_str(time_str: str) -> dt.datetime:
    DUMMY_DATETIME = f"{settings.DUMMY_MONDAY_DATE} {time_str}"
    time_part = dt.datetime.strptime(DUMMY_DATETIME, "%Y-%m-%d %H:%M")
    return time_part


# def _concat_time_slots(time_slot_list: List[TimeSlot]) -> List[TimeSlot]:
#     """If gap less than 30 min, concat"""
#     THRESHOLD = 30
#
#     list_len = len(time_slot_list)
#
#     if list_len <= 1:
#         return time_slot_list
#
#     output_list = [time_slot_list[0]]
#
#     for i in range(list_len - 1):
#         prev_time_slot = output_list[-1]
#         latter_time_slot = time_slot_list[i + 1]
#
#         if prev_time_slot.adjacent(latter_time_slot, threshold_min=THRESHOLD):
#             new_time_slot = TimeSlot(start=prev_time_slot.start, end=latter_time_slot.end)
#             output_list[-1] = new_time_slot
#         else:
#             output_list.append(latter_time_slot)
#
#     return output_list
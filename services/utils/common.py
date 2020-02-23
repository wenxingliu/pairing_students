import datetime as dt
import pandas as pd
from typing import List, Union

import settings as settings


def dedup_dataframe(df: pd.DataFrame,
                    first_dedup_cols: List[str],
                    dedup_wechat_cols: List[str] = None) -> pd.DataFrame:
    """
    first dedup by wechat account, take the last one;
    then dedup based on name, take the last one and compile other wechat info
    """
    df = _dedup_based_on_selected_subset(df, first_dedup_cols)

    if dedup_wechat_cols:
        df = _combine_mutliple_wechat_entries(df, dedup_wechat_cols)

    return df


def _combine_mutliple_wechat_entries(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:

    # compile wechat info
    gp_df = df.groupby(cols, as_index=False).agg({'parent_wechat': _backup_wechat_information})

    if gp_df.empty:
        return df

    gp_df.rename(columns={"parent_wechat": "other_wechat_info"}, inplace=True)

    # dedup based on selected column
    dedup_df = _dedup_based_on_selected_subset(df, cols)

    # join back to get all info
    joined_df = dedup_df.merge(gp_df, how='left', on=cols)

    return joined_df


def _dedup_based_on_selected_subset(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    sort by time, and take the latest record
    """
    df = df.sort_values('timestamp')

    for col in cols:
        df[col] = df[col].apply(lambda x: str(x).lower().strip())

    dedup_df = df.drop_duplicates(cols, keep='last')

    return dedup_df


def _backup_wechat_information(wechat_lst) -> Union[None, str]:
    if len(wechat_lst) > 1:
        return ', '.join(wechat_lst)
    else:
        return None


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


def convert_str_to_bool(bool_str: str) -> bool:
    if str(bool_str).lower() == 'true':
        return True
    else:
        return False


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


def assign_scarcity_metrics_to_person_and_time_slot(time_slot_list,
                                                    scarcity_dict,
                                                    class_type='') -> int:
    """Compute how rare the request is, the lower the number is, the rarer the requested slot is"""
    scarcity_index_list = []
    for time_slot in time_slot_list:
        scarcity_index = scarcity_dict[time_slot]
        time_slot.scarcity_index = scarcity_index
        scarcity_index_list.append(scarcity_index)

    if scarcity_index_list:
        if class_type == 'volunteer':
            return min(scarcity_index_list)
        else:
            return max(scarcity_index_list)
    else:
        return 0


def invalid_wechat(wechat_id: str) -> id:
    return str(wechat_id).lower().startswith("wxid")

import datetime as dt
import pandas as pd
from typing import List

import settings as settings
from services.utils.common import (dedup_dataframe,
                                   convert_str_to_bool,
                                   convert_bool_to_int,
                                   cleanup_gender,
                                   get_digits)
from services.utils.requestee import (cleanup_utc_time_slots_requestee,
                                      compute_request_scarcity_index)
from services.utils.volunteer import (compute_available_time_slots_volunteer,
                                      compute_volunteer_scarcity_index)
from services.utils.timezone_conversion import compute_timezone_utc_offset_dict


def read_and_clean_requests(xlsx_file_path_list: List[str],
                            sheet_name: str,
                            data_dir: str = settings.DATA_INPUT_DIR) -> pd.DataFrame:
    request_df = _combine_multiple_xlsx_files(xlsx_file_path_list, sheet_name, data_dir)

    print(f"Number of raw request records: {len(request_df)}")

    request_df.rename(columns=settings.REQUEST_COLUMNS_MAPPER, inplace=True)
    request_df['timestamp'] = pd.to_datetime(request_df.timestamp)

    request_df = dedup_dataframe(df=request_df,
                                 first_dedup_cols=settings.REQUESTEE_UNIQUE_COLS,
                                 dedup_wechat_cols=['requestee'])

    # Exclude requests with invalid wechat accounts
    # invalid_wechat_list = _invalid_wechat_account()
    # request_df = request_df.loc[~request_df.parent_wechat.isin(invalid_wechat_list)]

    if 'doctor_family' in request_df:
        request_df['doctor_family'] = request_df.doctor_family.apply(convert_bool_to_int)
    if 'patient_family' in request_df:
        request_df['patient_family'] = request_df.patient_family.apply(convert_bool_to_int)
    if 'hubei_family' in request_df:
        request_df['hubei_family'] = request_df.hubei_family.apply(convert_bool_to_int)

    request_df['gender'] = request_df.gender.apply(cleanup_gender)
    request_df['volunteer_gender'] = request_df.volunteer_gender.apply(cleanup_gender)

    request_df['age'] = request_df.age_raw.apply(get_digits)
    request_df = request_df.loc[request_df.age < 18]

    request_df['time_slots_china'] = request_df.apply(
        lambda r: cleanup_utc_time_slots_requestee(r['time_slot_time'], r['time_slot_day']),
        axis=1
    )

    request_df = compute_request_scarcity_index(request_df)

    print(f"Number of unique requests: {len(request_df)}")

    return request_df


def read_and_clean_volunteers(xlsx_file_path_list: List[str],
                              sheet_name: str,
                              data_dir: str = settings.DATA_INPUT_DIR) -> pd.DataFrame:
    volunteer_df = _combine_multiple_xlsx_files(xlsx_file_path_list, sheet_name, data_dir)

    print(f"Number of raw volunteer records: {len(volunteer_df)}")

    volunteer_df.columns = [col.replace("'", "") for col in volunteer_df.columns]
    volunteer_df.rename(columns=settings.VOLUNTEER_COLUMNS_MAPPER, inplace=True)

    volunteer_df = volunteer_df.loc[pd.notnull(volunteer_df.name)]

    volunteer_df = dedup_dataframe(df=volunteer_df,
                                   first_dedup_cols=settings.VOLUNTEER_UNIQUE_COLS,
                                   dedup_wechat_cols=None)

    volunteer_df['timestamp'] = pd.to_datetime(volunteer_df.timestamp)

    volunteer_df['volunteer_gender'] = volunteer_df.volunteer_gender.apply(cleanup_gender)
    volunteer_df['age'] = volunteer_df.age.apply(get_digits)

    utc_offset_dict = compute_timezone_utc_offset_dict()
    volunteer_df['utc_offset'] = volunteer_df.timezone.apply(
        lambda x: utc_offset_dict.get(x, 0))
    volunteer_df["time_slots_local"] = volunteer_df.apply(compute_available_time_slots_volunteer, axis=1)

    volunteer_df.num_pairs.fillna(1, inplace=True)
    volunteer_df.fillna("", inplace=True)

    volunteer_df = compute_volunteer_scarcity_index(volunteer_df)

    print(f"Number of unique volunteers: {len(volunteer_df)}")

    return volunteer_df


def read_previous_paired_results(csv_file_path_list: List[str]) -> pd.DataFrame:
    raw_paired_results_df = _combine_multiple_pairing_csv_files(csv_file_path_list)

    raw_paired_results_df["timestamp"] = dt.datetime.utcnow()

    raw_paired_results_df['volunteer_email_sent'] = True

    raw_paired_results_df.rename(columns=settings.CONFIRMATION_COLUMNS_MAPPER, inplace=True)

    if ('accept_pairing' in raw_paired_results_df) and ('connected' in raw_paired_results_df):
        raw_paired_results_df['accept_pairing'] = raw_paired_results_df.accept_pairing.apply(convert_bool_to_int)
        raw_paired_results_df['connected'] = raw_paired_results_df.connected.apply(convert_bool_to_int)
        raw_paired_results_df['paired'] = raw_paired_results_df.apply(lambda r: r['accept_pairing'] and r['connected'], axis=1)
        paired_results_df = raw_paired_results_df.loc[raw_paired_results_df.paired == 1]
    else:
        paired_results_df = raw_paired_results_df
        paired_results_df["timestamp"] = pd.to_datetime(paired_results_df.email_sent_time_utc)
        paired_results_df['volunteer_email_sent'] = paired_results_df.volunteer_email_sent.apply(convert_str_to_bool)

    return paired_results_df


def _combine_multiple_pairing_csv_files(csv_file_path_list: List[str]) -> pd.DataFrame:
    df_list = []

    for csv_file_path in csv_file_path_list:
        sub_df = pd.read_csv(f'{settings.PAIRING_OUTPUT_DIR}/{csv_file_path}.csv')
        sub_df['file_group'] = csv_file_path
        df_list.append(sub_df)

    combined_df = pd.concat(df_list, axis=0, sort=True)

    return combined_df


def _combine_multiple_xlsx_files(xlsx_file_path_list: List[str],
                                 sheet_name: str,
                                 data_dir: str) -> pd.DataFrame:
    df_list = []

    for xlsx_file_path in xlsx_file_path_list:
        sub_df = pd.read_excel(f'{data_dir}/{xlsx_file_path}.xlsx', sheet_name=sheet_name)
        sub_df['file_group'] = xlsx_file_path
        df_list.append(sub_df)

    combined_df = pd.concat(df_list, axis=0, sort=True)

    return combined_df


def _invalid_wechat_account() -> list:
    invalid_wechat_df = pd.read_csv(settings.INVALID_WECHAT_LIST_PATH)
    invalid_wechat_list = invalid_wechat_df.wechat.tolist()
    return invalid_wechat_list

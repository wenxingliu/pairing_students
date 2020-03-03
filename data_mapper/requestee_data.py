from typing import List

import pandas as pd

import settings as settings
from data_mapper.utils import _combine_multiple_xlsx_files
from services.utils.common import dedup_dataframe, convert_bool_to_int, cleanup_gender, get_digits
from services.utils.requestee import cleanup_utc_time_slots_requestee, compute_request_scarcity_index


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

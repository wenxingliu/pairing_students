from typing import List

import pandas as pd

import settings as settings
from data_mapper.utils import _combine_multiple_xlsx_files
from services.utils.common import dedup_dataframe, cleanup_gender, get_digits
from services.utils.timezone_conversion import compute_timezone_utc_offset_dict
from services.utils.volunteer import compute_available_time_slots_volunteer, compute_volunteer_scarcity_index


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

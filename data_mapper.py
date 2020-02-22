import pandas as pd

from config import settings as settings
from services.utils.common import dedup_dataframe, convert_bool_to_int, cleanup_gender, get_digits
from services.utils.requestee import cleanup_utc_time_slots_requestee, compute_scarcity_index
from services.utils.volunteer import compute_available_time_slots_volunteer
from services.utils.timezone_conversion import compute_timezone_utc_offset_dict


def read_and_clean_requests(xlsx_file_path: str, sheet_name: str) -> pd.DataFrame:
    request_df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name)
    request_df.rename(columns=settings.REQUEST_COLUMNS_MAPPER, inplace=True)
    request_df['timestamp'] = pd.to_datetime(request_df.timestamp)

    request_df = dedup_dataframe(request_df, settings.REQUESTEE_UNIQUE_COLS)

    request_df['doctor_family'] = request_df.doctor_family.apply(convert_bool_to_int)
    request_df['patient_family'] = request_df.patient_family.apply(convert_bool_to_int)

    request_df['gender'] = request_df.gender.apply(cleanup_gender)
    request_df['volunteer_gender'] = request_df.volunteer_gender.apply(cleanup_gender)

    request_df['age'] = request_df.age_raw.apply(get_digits)

    request_df['time_slots_china'] = request_df.apply(
        lambda r: cleanup_utc_time_slots_requestee(r['time_slot_time'], r['time_slot_day']),
        axis=1
    )

    request_df = compute_scarcity_index(request_df)

    return request_df


def read_and_clean_volunteers(xlsx_file_path: str, sheet_name: str) -> pd.DataFrame:
    volunteer_df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name)
    volunteer_df.columns = [col.replace("'", "") for col in volunteer_df.columns]
    volunteer_df.rename(columns=settings.VOLUNTEER_COLUMNS_MAPPER, inplace=True)

    volunteer_df = volunteer_df.loc[pd.notnull(volunteer_df.name)]

    volunteer_df = dedup_dataframe(volunteer_df, settings.VOLUNTEER_UNIQUE_COLS)

    volunteer_df['timestamp'] = pd.to_datetime(volunteer_df.timestamp)

    volunteer_df['volunteer_gender'] = volunteer_df.volunteer_gender.apply(cleanup_gender)
    volunteer_df['age'] = volunteer_df.age.apply(get_digits)

    utc_offset_dict = compute_timezone_utc_offset_dict()
    volunteer_df['utc_offset'] = volunteer_df.timezone.apply(
        lambda x: utc_offset_dict.get(x, 0))
    volunteer_df["time_slots_local"] = volunteer_df.apply(compute_available_time_slots_volunteer, axis=1)

    volunteer_df.num_pairs.fillna(1, inplace=True)
    volunteer_df.fillna("", inplace=True)

    required_cols = list(settings.VOLUNTEER_COLUMNS_MAPPER.values()) + ['utc_offset', 'time_slots_local']
    common_cols = list(set(required_cols).intersection(volunteer_df.columns))
    volunteer_df = volunteer_df[common_cols]

    return volunteer_df

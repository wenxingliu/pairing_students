import datetime as dt
from typing import List

import pandas as pd

import settings as settings
from data_mapper.utils import _combine_multiple_pairing_csv_files
from services.utils.common import convert_bool_to_int, convert_str_to_bool


def read_previous_paired_results(csv_file_path_list: List[str]) -> pd.DataFrame:
    raw_paired_results_df = _combine_multiple_pairing_csv_files(csv_file_path_list)

    if 'email_sent_time_utc' in raw_paired_results_df:
        raw_paired_results_df["timestamp"] = pd.to_datetime(raw_paired_results_df.email_sent_time_utc)
        raw_paired_results_df.timestamp.fillna(dt.datetime(2001, 1, 1), inplace=True)
    else:
        raw_paired_results_df["timestamp"] = dt.datetime.utcnow()

    if 'volunteer_email_sent' in raw_paired_results_df:
        raw_paired_results_df.volunteer_email_sent.fillna(True, inplace=True)
    else:
        raw_paired_results_df['volunteer_email_sent'] = True

    raw_paired_results_df.rename(columns=settings.CONFIRMATION_COLUMNS_MAPPER, inplace=True)

    if ('accept_pairing' in raw_paired_results_df) and ('connected' in raw_paired_results_df):
        raw_paired_results_df['accept_pairing'] = raw_paired_results_df.accept_pairing.apply(convert_bool_to_int)
        raw_paired_results_df['connected'] = raw_paired_results_df.connected.apply(convert_bool_to_int)
        raw_paired_results_df['paired'] = raw_paired_results_df.apply(lambda r: r['accept_pairing'] and r['connected'], axis=1)
        paired_results_df = raw_paired_results_df.loc[raw_paired_results_df.paired == 1]
    else:
        paired_results_df = raw_paired_results_df
        paired_results_df['volunteer_email_sent'] = paired_results_df.volunteer_email_sent.apply(convert_str_to_bool)

    paired_results_df.sort_values(['timestamp', 'file_group'])
    paired_results_df = paired_results_df.drop_duplicates(['volunteer', 'volunteer_email',
                                                           'volunteer_parent_email', 'requestee'])

    return paired_results_df

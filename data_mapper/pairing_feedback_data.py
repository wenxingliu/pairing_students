from typing import List

import pandas as pd

import settings as settings
from data_mapper.utils import _combine_multiple_xlsx_files
from services.utils.common import dedup_dataframe


def read_pairing_feedback(xlsx_file_path_list: List[str],
                          sheet_name: str) -> pd.DataFrame:
    feedbacks_df = _combine_multiple_xlsx_files(xlsx_file_path_list=xlsx_file_path_list,
                                                sheet_name=sheet_name,
                                                data_dir=settings.DATA_INPUT_DIR)

    feedbacks_df.rename(columns=settings.PAIRING_FEEDBACK_COLUMNS, inplace=True)

    feedbacks_df = dedup_dataframe(df=feedbacks_df,
                                   first_dedup_cols=["volunteer", "volunteer_email",
                                                     "volunteer_parent_email",
                                                     "requestee", "requestee_wechat",
                                                     "requestee_email"])
    return feedbacks_df

import pandas as pd
from typing import List

import settings as settings


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

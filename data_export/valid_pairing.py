import pandas as pd
from typing import List, Union

from data_mapper.previous_pairing_data import read_previous_paired_results
from data_mapper.pairing_feedback_data import read_pairing_feedback
from services.previous_pairing import compute_previously_assigned_pairs
from services.pairing_feedback import process_paired_info_based_on_feedback

OUTPUT_COLS = [
    "organization",
    "volunteer",
    "volunteer_wechat",
    "volunteer_email",
    "volunteer_parent_email",
    "requestee",
    "requestee_wechat",
    "requestee_email",
    "requestee_phone",
    "email_sent_time_utc",
    "doctor_family",
    "hubei_family",
    "is_valid",
    "file_group"
]


def compute_valid_pairing(previously_paired_file_path_list: List[str],
                          pairing_feedback_file_path_list: Union[None, List[str]] = None) \
        -> pd.DataFrame:
    existing_pairs_df = read_previous_paired_results(previously_paired_file_path_list)
    existing_pairs = compute_previously_assigned_pairs(existing_pairs_df)

    # Step 3: Read feedbacks, and adjust previous pairs
    if pairing_feedback_file_path_list is not None:
        feedback_df = read_pairing_feedback(xlsx_file_path_list=pairing_feedback_file_path_list,
                                            sheet_name='Form Responses 1')
        process_paired_info_based_on_feedback(feedback_df, existing_pairs)

    valid_pair_list = []

    for paired_info in existing_pairs:
        is_valid = paired_info.valid and paired_info.active_volunteer and paired_info.active_requestee
        paired_info_dict = {
            "organization": paired_info.paired_info.get('organization', ''),
            "volunteer": paired_info.volunteer_name,
            "volunteer_wechat": paired_info.volunteer_wechat,
            "volunteer_email": paired_info.volunteer_email,
            "volunteer_parent_email": paired_info.volunteer_parent_email,
            "requestee": paired_info.requestee_name,
            "requestee_wechat": paired_info.requestee_wechat,
            "requestee_email": paired_info.paired_info.get('requestee_email', ''),
            "requestee_phone": paired_info.paired_info.get('requestee_phone', ''),
            "email_sent_time_utc": str(paired_info.email_sent_time_utc),
            "doctor_family": paired_info.paired_info.get('doctor_family', ''),
            "hubei_family": paired_info.paired_info.get('hubei_family', ''),
            "file_group": paired_info.paired_info.get('file_group', ''),
            "is_valid": str(is_valid)
        }

        valid_pair_list.append(paired_info_dict)

    df = pd.DataFrame(valid_pair_list)
    df.sort_values(['organization', 'volunteer', 'email_sent_time_utc'], inplace=True)

    df = df[OUTPUT_COLS]

    return df


if __name__ == '__main__':
    df = compute_valid_pairing(previously_paired_file_path_list=['sent/20200226匹配并联系成功表-核实后',
                                                                 'sent/202002270452_paired_sent',
                                                                 'sent/202002270452_recommendations_sent',
                                                                 'sent/202002272226_paired_sent',
                                                                 'sent/202002272226_recommendations_sent',
                                                                 'sent/202002290417_paired_sent',
                                                                 'sent/202002290417_recommendations_sent',
                                                                 'sent/202002291812_paired_sent',
                                                                 'sent/202002291812_recommendations_sent',
                                                                 'sent/202003020222_paired_sent',
                                                                 'sent/202003020222_recommendations_sent',
                                                                 'sent/202003030603_paired_sent',
                                                                 'sent/202003030603_recommendations_sent'],
                               pairing_feedback_file_path_list=['pairing_feedback_response'])

    df.to_csv('data/all_paired_0302.csv', index=False)
    a = 1

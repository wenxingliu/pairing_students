from collections import namedtuple
import datetime as dt
import pandas as pd
from typing import Set, Union
from models.paired_info import PairedInfo


Backouts = namedtuple("Backouts", ["requestee", "volunteer"])


def process_paired_info_based_on_feedback(feedbacks_df: pd.DataFrame,
                                          existing_pairs: Set[PairedInfo]):
    # volunteer needs to be removed
    backout_unassigned_volunteers = []
    # requestee needs to be removed
    backout_unassigned_requestees = []

    for data_tuple in feedbacks_df.itertuples():

        previous_pairing_info = _retrieve_previous_pairing_info(data_tuple,
                                                                existing_pairs)

        # cannot find paired info
        if previous_pairing_info is None:
            if _not_empty(data_tuple.backout_volunteer):
                backout_unassigned_volunteers.append(data_tuple)
            print(f"cannot find prev info for {data_tuple.volunteer}")
            continue

        # found previously paired info, invalidate
        previous_pairing_info.valid = False

        # volunteer paired, and want to back out
        if _not_empty(data_tuple.backout_volunteer):
            previous_pairing_info.active_volunteer = False

        # volunteer paired, but failed to connect, kick out requestee
        if _is_empty(data_tuple.requestee):
            previous_pairing_info.active_requestee = False

    return Backouts(volunteer=backout_unassigned_volunteers,
                    requestee=backout_unassigned_requestees)


def _retrieve_previous_pairing_info(feedback_info,
                                    existing_pairs: Set[PairedInfo]) -> Union[PairedInfo, None]:
    feedback_datetime = feedback_info.timestamp
    selected_pair = None

    for paired_info in existing_pairs:
        feedback_after_pairing = feedback_datetime > paired_info.email_sent_time_utc

        if not feedback_after_pairing:
            continue

        # found record by request
        no_requestee_info = _is_empty(feedback_info.requestee)
        is_same_requestee = (
                paired_info.requestee_name == feedback_info.requestee
                or paired_info.requestee_wechat == feedback_info.requestee_wechat
        )

        if no_requestee_info or is_same_requestee:
            # found record by volunteer
            same_volunteer_name = _string_fuzzy_match(paired_info.volunteer_name,
                                                      feedback_info.volunteer)
            paired_emails = set([paired_info.volunteer_parent_email, paired_info.volunteer_email])
            volunteer_emails = set([feedback_info.volunteer_parent_email, feedback_info.volunteer_email])
            same_volunteer_email = len(set(paired_emails).intersection(volunteer_emails)) > 0
            is_same_volunteer = (same_volunteer_name and same_volunteer_email)

            if is_same_volunteer:
                if (selected_pair is None
                        or selected_pair.email_sent_time_utc < paired_info.email_sent_time_utc):
                    selected_pair = paired_info

    return selected_pair


def _not_empty(input_val: Union[str, None]) -> bool:
    return not _is_empty(input_val)


def _is_empty(input_val: Union[str, None]) -> bool:
    if pd.isnull(input_val):
        return True
    elif str(input_val).lower() in ['', 'none', 'nan', 'na']:
        return True
    return False


def _string_fuzzy_match(str_1: str, str_2: str) -> bool:
    str_1 = str(str_1).lower().replace(' ', '')
    str_2 = str(str_2).lower().replace(' ', '')

    common = set(str_1).intersection(str_2)
    pct_common = len(common) / (len(set(str_1)) / 2 + len(set(str_2)) / 2)

    return pct_common > 0.8


if __name__ == '__main__':
    from data_mapper import read_pairing_feedback

    pairing_feedback_df = read_pairing_feedback(['pairing_feedback_response'])

    from data_mapper import read_previous_paired_results
    existing_pairs_df = read_previous_paired_results(['20200226匹配并联系成功表-核实后',
                                                      '202002270452_paired_sent',
                                                      '202002270452_recommendations_sent',
                                                      '202002272226_paired_sent',
                                                      '202002272226_recommendations_sent',
                                                      '202002290417_paired_sent',
                                                      '202002290417_recommendations_sent',
                                                      '202002291812_paired_sent',
                                                      '202002291812_recommendations_sent'])

    from services.previous_pairing import compute_previously_assigned_pairs
    existing_pairs = compute_previously_assigned_pairs(existing_pairs_df)

    out = process_paired_info_based_on_feedback(pairing_feedback_df, existing_pairs)

    a = 1

from collections import namedtuple
import pandas as pd
from typing import List, Set, Union
from models.paired_info import PairedInfo


Backouts = namedtuple("Backouts", ["requestee", "volunteer"])


def process_paired_info_based_on_feedback(feedbacks_df: pd.DataFrame,
                                          existing_pairs: Set[PairedInfo]):
    # volunteer needs to be removed
    backout_unassigned_volunteers = []
    # requestee needs to be removed
    backout_unassigned_requestees = []

    for data_tuple in feedbacks_df.itertuples():

        previous_pairing_info = _retrieve_previous_pairing_info(data_tuple, existing_pairs)

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
        if not _not_empty(data_tuple.requestee):
            previous_pairing_info.active_requestee = False

    return Backouts(volunteer=backout_unassigned_volunteers,
                    requestee=backout_unassigned_requestees)


def _retrieve_previous_pairing_info(feedback_info,
                                    existing_pairs: List[PairedInfo]) -> Union[PairedInfo, None]:
    for paired_info in existing_pairs:
        # found record by request
        if (
                paired_info.requestee_name == feedback_info.requestee
                or paired_info.requestee_wechat == feedback_info.requestee_wechat
        ):
            return paired_info

        # found record by volunteer
        same_name = str(paired_info.volunteer_name).lower() == feedback_info.volunteer
        paired_emails = set([paired_info.volunteer_parent_email, paired_info.volunteer_email])
        volunteer_emails = set([feedback_info.volunteer_parent_email, feedback_info.volunteer_email])
        common_email_address = set(paired_emails).intersection(volunteer_emails)
        if len(common_email_address) > 0 and same_name:
            return paired_info


def _not_empty(input_val: Union[str, None]) -> bool:
    if pd.isnull(input_val):
        return False
    elif str(input_val).lower() in ['', 'none', 'nan', 'na']:
        return False
    else:
        return True


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

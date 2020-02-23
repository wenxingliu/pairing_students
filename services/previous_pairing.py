import pandas as pd
from typing import List, Set

from models.volunteer import Volunteer
from models.requestee import Requestee
from models.paired_info import PairedInfo


def reflect_all_previously_paired_results(all_requestees: List[Requestee],
                                          all_volunteers: List[Volunteer],
                                          existing_pairs: Set[PairedInfo]):

    requestee_by_wechat_dict = {requestee.parent_wechat: requestee
                                for requestee in all_requestees}

    for paired_info in existing_pairs:
        previously_paired_request = requestee_by_wechat_dict.get(paired_info.requestee_wechat)

        if previously_paired_request:
            reflect_previously_paired_result_of_requestee(
                previously_paired_requestee=previously_paired_request,
                paired_info=paired_info,
                all_volunteers=all_volunteers
            )


def reflect_previously_paired_result_of_requestee(previously_paired_requestee: Requestee,
                                                  paired_info: PairedInfo,
                                                  all_volunteers: List[Volunteer]):
    paired_volunteer = paired_info.find_paired_volunteer(all_volunteers)

    if paired_info.volunteer_email_sent:
        paired_volunteer.mark_email_sent(paired_info.email_sent_time_utc)
        paired_volunteer.assign(previously_paired_requestee, paired_info.promised_time_slot)
        previously_paired_requestee.assign(paired_volunteer, paired_info.promised_time_slot)
    else:
        paired_volunteer.assign(previously_paired_requestee, paired_info.promised_time_slot)
        previously_paired_requestee.assign(paired_volunteer, paired_info.promised_time_slot)
        print(f"Paired: {paired_info}, but email not sent, will resend this time")


def compute_previously_assigned_pairs(pairing_df: pd.DataFrame) -> Set[PairedInfo]:
    paired_list = set()

    for data_row in pairing_df.iterrows():
        data_dict = data_row[1]
        paired_info = PairedInfo(data_dict)
        paired_list.add(paired_info)

    return paired_list

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

    volunteer_by_email_dict = {volunteer.volunteer_email: volunteer
                               for volunteer in all_volunteers}

    for paired_info in existing_pairs:
        previously_paired_request = requestee_by_wechat_dict.get(paired_info.requestee_wechat)
        previously_paired_volunteer = volunteer_by_email_dict.get(paired_info.volunteer_email)

        if (previously_paired_request is not None
                and previously_paired_volunteer is not None
                and previously_paired_volunteer.has_valid_email):

            reflect_previously_paired_result_of_requestee(
                paired_info=paired_info,
                previously_paired_requestee=previously_paired_request,
                previously_paired_volunteer=previously_paired_volunteer
            )
        elif not previously_paired_volunteer.has_valid_email:
            print(f"Invalid email on pairing: {previously_paired_volunteer}")
        else:
            print(f"Invalid paring: {paired_info}")


def reflect_previously_paired_result_of_requestee(paired_info: PairedInfo,
                                                  previously_paired_requestee: Requestee,
                                                  previously_paired_volunteer: Volunteer):

    if paired_info.volunteer_email_sent:
        previously_paired_volunteer.mark_email_sent(paired_info.email_sent_time_utc)
        previously_paired_volunteer.assign(previously_paired_requestee, paired_info.promised_time_slot)
        previously_paired_requestee.assign(previously_paired_volunteer, paired_info.promised_time_slot)
    else:
        previously_paired_volunteer.assign(previously_paired_requestee, paired_info.promised_time_slot)
        previously_paired_requestee.assign(previously_paired_volunteer, paired_info.promised_time_slot)
        print(f"Paired: {paired_info}, but email not sent, will resend this time")


def compute_previously_assigned_pairs(pairing_df: pd.DataFrame) -> List[PairedInfo]:
    paired_list = set()

    for data_dict in pairing_df.reset_index().T.to_dict().values():
        paired_info = PairedInfo(data_dict)
        paired_list.add(paired_info)

    return paired_list

import pandas as pd
from typing import List, Set

from models.volunteer import Volunteer
from models.requestee import Requestee
from models.paired_info import PairedInfo


def reflect_all_previously_paired_results(all_requestees: List[Requestee],
                                          all_volunteers: List[Volunteer],
                                          existing_pairs: Set[PairedInfo]):
    for previously_paired_request in all_requestees:
        reflect_previously_paired_result_of_requestee(
            previously_paired_requestee=previously_paired_request,
            all_volunteers=all_volunteers,
            existing_pairs=existing_pairs
        )


def reflect_previously_paired_result_of_requestee(previously_paired_requestee: Requestee,
                                                  all_volunteers: List[Volunteer],
                                                  existing_pairs: Set[PairedInfo]):
    paired_volunteer = None
    for paired_info in existing_pairs:
        if paired_info.requestee_wechat == previously_paired_requestee.parent_wechat:

            if paired_info.volunteer_email_sent:
                paired_volunteer = paired_info.find_paired_volunteer(all_volunteers)

                paired_volunteer.mark_email_sent(paired_info.email_sent_time_utc)
                paired_volunteer.assign(previously_paired_requestee, paired_info.promised_time_slot)
                previously_paired_requestee.assign(paired_volunteer, paired_info.promised_time_slot)
            else:
                print(f"Paired: {paired_info}, but email not sent")

            break

    if paired_volunteer is None:
        print(f"cannot find paired volunteer for {previously_paired_requestee}")


def compute_previously_assigned_pairs(pairing_df: pd.DataFrame) -> Set[PairedInfo]:
    paired_list = set()

    for data_row in pairing_df.iterrows():
        paired_info = PairedInfo(data_row[0])
        paired_list.add(paired_info)

    return paired_list

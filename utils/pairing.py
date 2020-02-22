import pandas as pd
from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee

from config import settings as settings


def compute_volunteers(volunteer_df: pd.DataFrame) -> List[Volunteer]:
    volunteers = []

    for volunteer_info in volunteer_df.T.to_dict().values():
        volunteer = Volunteer(volunteer_info)
        volunteers.append(volunteer)

    return volunteers


def compute_requestees(requestee_df: pd.DataFrame) -> List[Requestee]:
    requestees = []

    for requestee_info in requestee_df.T.to_dict().values():
        requestee = Requestee(requestee_info)
        requestees.append(requestee)

    sorted_requestees = sorted(requestees, key=lambda s: s.priority)

    return sorted_requestees


def pair_for_all(all_requestees: List[Requestee], all_volunteers: List[Volunteer]):
    for requestee in all_requestees:
        find_pair(requestee, all_volunteers)


def find_pair(requestee: Requestee, all_volunteers: List[Volunteer]):

    for volunteer in all_volunteers:

        if not volunteer.available:
            continue
        if volunteer.gender != requestee.volunteer_gender:
            continue
        if abs(volunteer.age - requestee.age) > settings.AGE_DIFF_THRESHOLD:
            continue

        overlapped_time = volunteer.overlapping_china_time_slots(requestee.time_slots_china)

        if overlapped_time:
            promised_time = sorted(overlapped_time, key=lambda x: x.scarcity_index)[0]
            volunteer.assign(requestee, promised_time)
            requestee.assign(volunteer, promised_time)
            return

    print(f'no match for {requestee}')

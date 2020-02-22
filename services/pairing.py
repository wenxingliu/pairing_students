from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee

import settings as settings


def pair_for_all(all_requestees: List[Requestee], all_volunteers: List[Volunteer]):
    for request in all_requestees:
        if not request.assigned:
            find_pair(request, all_volunteers)


def find_pair(requestee: Requestee, all_volunteers: List[Volunteer]):

    matched_volunteer = None

    for volunteer in all_volunteers:

        if not volunteer.available:
            continue
        if volunteer.gender != requestee.volunteer_gender:
            continue
        if abs(volunteer.age - requestee.age) > settings.AGE_DIFF_THRESHOLD:
            continue

        overlapped_time = volunteer.overlapping_china_time_slots(requestee.time_slots_china)

        if overlapped_time:
            matched_volunteer = volunteer
            promised_time = sorted(overlapped_time, key=lambda x: x.scarcity_index)[0]
            matched_volunteer.assign(requestee, promised_time)
            requestee.assign(matched_volunteer, promised_time)
            break

    if matched_volunteer is None:
        print(f'no match for {requestee}')

from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee

import settings as settings


def pair_for_all(all_requestees: List[Requestee], all_volunteers: List[Volunteer]):
    for request in all_requestees:
        if not request.assigned:
            find_pair(request, all_volunteers)


def find_pair(requestee: Requestee, all_volunteers: List[Volunteer]):
    for volunteer in all_volunteers:

        if not _legit_pairing(volunteer, requestee):
            continue

        overlapped_time = volunteer.overlapping_china_time_slots(requestee.time_slots_china)

        if overlapped_time:
            matched_volunteer = volunteer
            promised_time = sorted(overlapped_time, key=lambda x: x.scarcity_index)[0]
            matched_volunteer.assign(requestee, promised_time)
            requestee.assign(matched_volunteer, promised_time)
            break


def _legit_pairing(volunteer: Volunteer, requestee: Requestee) -> bool:
    return (volunteer.available
            and volunteer.has_valid_email
            and volunteer.gender == requestee.volunteer_gender
            and _age_match(volunteer, requestee))


def _age_match(volunteer: Volunteer, requestee: Requestee) -> bool:
    return ((volunteer.age >= requestee.age - 1)
            and (volunteer.age <= requestee.age + 3))

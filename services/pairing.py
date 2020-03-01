from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee
from services.utils.common import age_match, is_prev_paring


def pair_for_all(all_requestees: List[Requestee], all_volunteers: List[Volunteer]):
    for request in all_requestees:
        if not request.assigned:
            find_pair(request, all_volunteers)


def find_pair(requestee: Requestee, all_volunteers: List[Volunteer]):
    possible_volunteers = []

    for volunteer in all_volunteers:

        if not volunteer.active:
            continue

        if not _legit_pairing(volunteer, requestee):
            continue

        overlapped_time = volunteer.overlapping_china_time_slots(requestee.time_slots_china)

        if overlapped_time:
            promised_time = sorted(overlapped_time, key=lambda x: x.scarcity_index)[0]

            possible_volunteers.append((volunteer, promised_time))

    if possible_volunteers:
        sorted_possible_volunteers = sorted(possible_volunteers,
                                            key=lambda x: abs(x[0].age - requestee.age))

        matched_volunteer, promised_time = sorted_possible_volunteers[0]

        matched_volunteer.assign(requestee, promised_time)
        requestee.assign(matched_volunteer, promised_time)


def _legit_pairing(volunteer: Volunteer, requestee: Requestee) -> bool:
    return (volunteer.available
            and volunteer.active
            and not is_prev_paring(volunteer, requestee)
            and volunteer.has_valid_email
            and volunteer.gender in [requestee.volunteer_gender, requestee.gender]
            and age_match(volunteer, requestee, [-1, 100]))

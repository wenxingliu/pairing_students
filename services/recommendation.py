from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee

import settings as settings


def make_recommendations_for_all_unassigned_volunteers(all_requestees: List[Requestee],
                                                       all_volunteers: List[Volunteer]):
    for volunteer in all_volunteers:
        if volunteer.recommendation_filled:
            continue

        make_recommondation_for_volunteer(volunteer, all_requestees)


def make_recommondation_for_volunteer(volunteer: Volunteer,
                                      all_requestees: List[Requestee],
                                      recommendation_num: int = 3) -> List[Requestee]:

    recommendation_list = []

    for requestee in all_requestees:

        if requestee.assigned:
            continue
        if volunteer.gender != requestee.volunteer_gender:
            continue
        if abs(volunteer.age - requestee.age) > settings.AGE_DIFF_THRESHOLD:
            continue
        if len(recommendation_list) >= recommendation_num:
            return

        for time_slot_r in requestee.time_slots_china:
            for time_slot_v in volunteer.time_slots_china:
                hours_diff = (time_slot_r.fake_start_datetime - time_slot_v.fake_start_datetime).total_seconds() / 3600
                if abs(hours_diff) < settings.ALLOWED_HOURS_DIFF_IN_RECOMMENDATION:
                    recommendation_list.append(requestee)
                    volunteer.recommend(requestee)
                    break
                break

from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee
from services.utils.common import age_match
import settings as settings


def make_recommendations_for_all_unassigned_volunteers(all_requestees: List[Requestee],
                                                       all_volunteers: List[Volunteer]):
    for volunteer in all_volunteers:
        if volunteer.recommendation_made:
            continue

        make_recommondation_for_volunteer(volunteer, all_requestees)


def make_recommondation_for_volunteer(volunteer: Volunteer,
                                      all_requestees: List[Requestee]) -> List[Requestee]:

    for requestee in all_requestees:

        if requestee.assigned or requestee.recommendation_made:
            continue

        if not _legit_recommendation(volunteer, requestee):
            continue

        requestee.recommendation_made = True
        volunteer.recommend(requestee)

        # time_slot_recommendation = _legit_close_time_slot(volunteer, requestee)
        #
        # if time_slot_recommendation is not None:
        #     requestee.recommendation_made = True
        #     volunteer.recommend(requestee)
        #     return


def _legit_recommendation(volunteer: Volunteer, requestee: Requestee):
    return (age_match(volunteer=volunteer, requestee=requestee, age_diff_limit=[-3, 3])
            and (volunteer.gender in [requestee.volunteer_gender, requestee.gender]))


def _legit_close_time_slot(volunteer: Volunteer, requestee: Requestee):
    for time_slot_r in requestee.time_slots_china:
        for time_slot_v in volunteer.time_slots_china:
            hours_diff = (time_slot_r.fake_start_datetime - time_slot_v.fake_start_datetime).total_seconds() / 3600
            if abs(hours_diff) < settings.ALLOWED_HOURS_DIFF_IN_RECOMMENDATION:
                return time_slot_r

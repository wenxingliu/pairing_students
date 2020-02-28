from typing import List

from models.volunteer import Volunteer
from models.requestee import Requestee
from services.utils.common import age_match


# def make_recommendations_for_all_unassigned_volunteers(all_requestees: List[Requestee],
#                                                        all_volunteers: List[Volunteer]):
#     for volunteer in all_volunteers:
#
#         if volunteer.recommendation_made or volunteer.paired_student:
#             continue
#
#         make_recommondation_for_volunteer(volunteer, all_requestees)


def make_recommendations_for_all_unassigned_volunteers(all_requestees: List[Requestee],
                                                       all_volunteers: List[Volunteer]):
    for requetee in all_requestees:

        if requetee.recommendation_made or requetee.assigned:
            continue

        make_recommondation_for_requestee(requetee, all_volunteers)


def make_recommondation_for_volunteer(volunteer: Volunteer,
                                      all_requestees: List[Requestee]) -> None:

    if volunteer.recommendation_made or volunteer.paired_student:
        return

    for requestee in all_requestees:

        if requestee.assigned or requestee.recommendation_made:
            continue

        if _legit_recommendation(volunteer, requestee):
            time_slot_recommendation = _legit_close_time_slot(volunteer, requestee)

            if time_slot_recommendation is not None:
                requestee.recommendation_made = True
                volunteer.recommend(requestee)
                print(f"Recommend {requestee} and {volunteer}")
                return


def make_recommondation_for_requestee(requestee: Requestee,
                                      all_volunteers: List[Volunteer]) -> None:
    possible_volunteers = []

    for volunteer in all_volunteers:

        if volunteer.recommendation_made or volunteer.paired_student:
            continue

        if not _legit_recommendation(volunteer, requestee):
            continue

        time_slot_recommendation = _legit_close_time_slot(volunteer, requestee)

        if time_slot_recommendation is not None:
            possible_volunteers.append((volunteer, time_slot_recommendation))

    if possible_volunteers:
        sorted_possible_volunteers = sorted(possible_volunteers,
                                            key=lambda x: abs(x[0].age - requestee.age))

        recommended_volunteer, promised_time = sorted_possible_volunteers[0]

        requestee.recommendation_made = True
        recommended_volunteer.recommend(requestee)


def blind_recommendation(all_volunteers: List[Volunteer],
                         all_requestees: List[Requestee]):
    for requestee in all_requestees:

        if requestee.assigned or requestee.recommendation_made:
            continue

        for volunteer in all_volunteers:
            if volunteer.recommendation_made or volunteer.paired_student:
                continue

            requestee.recommendation_made = True
            volunteer.recommend(requestee)
            print(f"Blind match {requestee} and {volunteer}")
            break


def _legit_recommendation(volunteer: Volunteer, requestee: Requestee):
    return (age_match(volunteer=volunteer, requestee=requestee,
                      age_diff_limit=[-1, 100])
            and (volunteer.gender in [requestee.volunteer_gender, requestee.gender]))


def _legit_close_time_slot(volunteer: Volunteer, requestee: Requestee):
    for time_slot_r in requestee.time_slots_china:
        for time_slot_v in volunteer.time_slots_china:
            hours_diff = (time_slot_r.fake_start_datetime - time_slot_v.fake_start_datetime).total_seconds() / 3600
            if abs(hours_diff) < 1000:
                return time_slot_r

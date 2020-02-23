import datetime as dt
import pandas as pd
from typing import List

from models.requestee import Requestee
from models.volunteer import Volunteer
import settings as settings


def compute_paired_data(requestees: List[Requestee], log_file: bool = True):
    paired_list = []

    for requestee in requestees:
        if requestee.assigned:
            volunteer = requestee.volunteer
            promised_time_slot = requestee.promised_time_slot

            if volunteer.email_sent:
                email_sent_time_str = volunteer.email_sent_time_utc.strftime("%Y-%m-%d %H:%M:%S")
            else:
                email_sent_time_str = settings.DUMMY_MONDAY_DATE

            paired_info = {
                "organization": volunteer.organization,
                "volunteer": volunteer.name,
                "volunteer_wechat": volunteer.parent_wechat,
                "requestee": requestee.name,
                "requestee_wechat": requestee.parent_wechat,
                "promised_time_slot": str(promised_time_slot),
                "slot_start_time": promised_time_slot.start.strftime("%H:%M"),
                "slot_end_time": promised_time_slot.end.strftime("%H:%M"),
                "weekday": promised_time_slot.weekday,
                "volunteer_email_sent": str(requestee.volunteer.email_sent),
                "email_sent_time_utc": email_sent_time_str,
                "other_wechat_info": requestee.other_wechat_info,
                "doctor_family": requestee.doctor_family,
                "patient_family": requestee.patient_family
            }

            paired_list.append(paired_info)

    paired_df = pd.DataFrame(paired_list)

    if paired_df.empty:
        print('No paired')
    else:
        paired_df.sort_values(["organization", "volunteer_wechat", "promised_time_slot"], inplace=True)

        if log_file:
            file_path = _compute_export_file_path('paired.csv', settings.PAIRING_OUTPUT_DIR)
            paired_df.to_csv(file_path, index=False)

        doctor_family_count = int(paired_df.doctor_family.sum())
        patient_family_count = int(paired_df.patient_family.sum())

        print(f"""
        Successful pairs: {len(paired_df)} 
        Doctor Family: {doctor_family_count}
        Patient Family: {patient_family_count}
        """)

        return paired_df


def compute_unassigned_volunteers(volunteers: List[Volunteer], log_file: bool = True):
    unassigned_volunteer_list = []

    for volunteer in volunteers:
        if volunteer.available and (not volunteer.recommendation_made):
            available_slots_str = ','.join([str(slot) for slot in volunteer.time_slots_china])
            volunteer_info = {
                "Organization": volunteer.organization,
                "Volunteer": volunteer.name,
                "Volunteer Wechat": volunteer.parent_wechat,
                "Willing To Take": volunteer.num_pairs,
                "Current Availability": volunteer.available_spots,
                "Available Time (China Timezone)": available_slots_str,
                "Recommendation Made": volunteer.recommendation_made
            }
            unassigned_volunteer_list.append(volunteer_info)

    unassigned_volunteer_df = pd.DataFrame(unassigned_volunteer_list)

    if unassigned_volunteer_df.empty:
        print(f'No unassigned volunteers')
    else:
        unassigned_volunteer_df.sort_values(['Organization', 'Volunteer'], inplace=True)

        if log_file:
            file_path = _compute_export_file_path('unassigned_volunteers.csv', settings.DATA_OUTPUT_DIR)
            unassigned_volunteer_df.to_csv(file_path, index=False)

        return unassigned_volunteer_df


def compute_volunteers_recommendations(volunteers: List[Volunteer], log_file: bool = True):
    recommendation_list = []

    for volunteer in volunteers:
        available_slots_str = ','.join([str(slot) for slot in volunteer.time_slots_china])

        for request in volunteer.potential_match:
            request_time_slot = request.time_slots_local

            recommendation_info = {
                "Organization": volunteer.organization,
                "Volunteer": volunteer.name,
                "Volunteer Wechat": volunteer.parent_wechat,
                "Potential Match": request.name,
                "Volunteer Available Time (China Timezone)": available_slots_str,
                "Student Available Time (China Timezone)": request_time_slot
            }

            recommendation_list.append(recommendation_info)

    recommendation_df = pd.DataFrame(recommendation_list)
    recommendation_df.sort_values(['Organization', 'Volunteer',
                                   'Volunteer Available Time (China Timezone)'], inplace=True)

    if log_file:
        file_path = _compute_export_file_path('recommendations.csv', settings.DATA_OUTPUT_DIR)
        recommendation_df.to_csv(file_path, index=False)

    return recommendation_df


def compute_unassgined_requestee(requestees: List[Requestee], log_file: bool = True) -> pd.DataFrame:
    left_requestee_list = []

    for requestee in requestees:

        if requestee.assigned:
            continue

        requestee_info = {
            "timestamp": requestee.timestamp,
            "requestee": requestee.name.title(),
            "requestee_wechat": requestee.parent_wechat,
            "age": requestee.age,
            "gender": requestee.gender,
            "preferred_match_gender": requestee.volunteer_gender,
            "english_learning_in_years": requestee.requestee_info.get('english_learning_in_years'),
            "doctor_family": requestee.doctor_family,
            "patient_family": requestee.patient_family,
            "recommendation_made": "Yes" if requestee.recommendation_made else "No",
            "other_wechat_info": requestee.other_wechat_info
        }

        left_requestee_list.append(requestee_info)

    left_requestee_df = pd.DataFrame(left_requestee_list)

    if left_requestee_df.empty:
        print('No one left!')
    else:
        left_requestee_df.sort_values(["doctor_family", "patient_family", "timestamp"])

        if log_file:
            file_path = _compute_export_file_path('unassigned_requestee.csv', settings.DATA_OUTPUT_DIR)
            left_requestee_df.to_csv(file_path, index=False)

        doctor_family_count = int(left_requestee_df.doctor_family.sum())
        patient_family_count = int(left_requestee_df.patient_family.sum())

        print(f"""
        Unassigned requests: {len(left_requestee_df)} 
        Doctor Family: {doctor_family_count}
        Patient Family: {patient_family_count}
        """)

        return left_requestee_df


def compute_no_organization_volunteers(volunteers: List[Volunteer], log_file: bool = True):
    no_org_list = []

    for volunteer in volunteers:

        if volunteer.no_org:

            volunteer_info = {
                "Volunteer": volunteer.name,
                "Organization": volunteer.organization,
                "Volunteer Wechat": volunteer.parent_wechat,
                "Volunteer Email": volunteer.volunteer_email,
                "Volunteer Parent Email": volunteer.parent_email
            }

            no_org_list.append(volunteer_info)

    no_org_df = pd.DataFrame(no_org_list)
    no_org_df.sort_values(['Organization', 'Volunteer'], inplace=True)

    if log_file:
        file_path = _compute_export_file_path('no_org_volunteers.csv', settings.DATA_OUTPUT_DIR)
        no_org_df.to_csv(file_path, index=False)

    return no_org_df


def _compute_export_file_path(file_name: str, dir_path: str) -> str:
    dt_str = dt.datetime.utcnow().strftime("%Y%m%d%H%M")
    file_path = f"{dir_path}/{dt_str}_{file_name}"
    return file_path

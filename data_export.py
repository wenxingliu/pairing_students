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
                "requestee": requestee.name,
                "requestee_wechat": requestee.parent_wechat,
                "volunteer": volunteer.name,
                "volunteer_wechat": volunteer.parent_wechat,
                "organization": volunteer.organization,
                "promised_time_slot": str(promised_time_slot),
                "slot_start_time": promised_time_slot.start.strftime("%H:%M"),
                "slot_end_time": promised_time_slot.end.strftime("%H:%M"),
                "weekday": promised_time_slot.weekday,
                "volunteer_email_sent": str(requestee.volunteer.email_sent),
                "email_sent_time_utc": email_sent_time_str
            }

            paired_list.append(paired_info)

    paired_df = pd.DataFrame(paired_list)
    paired_df.sort_values(["volunteer_wechat", "promised_time_slot"])

    if log_file:
        file_path = _compute_export_file_path('paired.csv', settings.PAIRING_OUTPUT_DIR)
        paired_df.to_csv(file_path, index=False)

    return paired_df


def compute_volunteers_to_be_paired(volunteers: List[Volunteer], log_file: bool = True):
    to_be_paired_volunteers_list = []

    for volunteer in volunteers:
        if volunteer.available and (not volunteer.recommendation_filled):
            available_slots_str = ','.join([str(slot) for slot in volunteer.time_slots_china])
            volunteer_info = {
                "Volunteer": volunteer.name,
                "Volunteer Wechat": volunteer.parent_wechat,
                "Willing To Take": volunteer.num_pairs,
                "Current Availability": volunteer.available_spots,
                "Available Time (China Timezone)": available_slots_str
            }
            to_be_paired_volunteers_list.append(volunteer_info)

    to_be_paired_volunteers_df = pd.DataFrame(to_be_paired_volunteers_list)

    if log_file:
        file_path = _compute_export_file_path('unassigned_volunteers.csv', settings.DATA_OUTPUT_DIR)
        to_be_paired_volunteers_df.to_csv(file_path, index=False)

    return to_be_paired_volunteers_df


def compute_volunteers_recommendations(volunteers: List[Volunteer], log_file: bool = True):
    recommendation_list = []

    for volunteer in volunteers:
        available_slots_str = ','.join([str(slot) for slot in volunteer.time_slots_china])

        for request in volunteer.potential_match:
            request_time_slot = request.time_slots_local

            recommendation_info = {
                "Volunteer": volunteer.name,
                "Volunteer Wechat": volunteer.parent_wechat,
                "Potential Match": request.name,
                "Volunteer Available Time (China Timezone)": available_slots_str,
                "Student Available Time (China Timezone)": request_time_slot
            }

            recommendation_list.append(recommendation_info)

    recommendation_df = pd.DataFrame(recommendation_list)

    if log_file:
        file_path = _compute_export_file_path('recommendations.csv', settings.DATA_OUTPUT_DIR)
        recommendation_df.to_csv(file_path, index=False)

    return recommendation_df


def _compute_export_file_path(file_name: str, dir_path: str) -> str:
    dt_str = dt.datetime.utcnow().strftime("%Y%m%d%H%M")
    file_path = f"{dir_path}/{dt_str}_{file_name}"
    return file_path

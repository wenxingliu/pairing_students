import pandas as pd
from typing import List

from models.requestee import Requestee
from models.volunteer import Volunteer


def compute_paired_data(requestees: List[Requestee]):
    paired_list = []
    for requestee in requestees:
        if requestee.assigned:
            paired_info = {
                "Requestee": requestee.name,
                "Requestee Wechat": requestee.parent_wechat,
                "Tentative Time (China Timezone)": str(requestee.promised_time_slot),
                "Volunteer": requestee.volunteer.name,
                "Volunteer Wechat": requestee.volunteer.parent_wechat
            }
            paired_list.append(paired_info)
    paired_df = pd.DataFrame(paired_list)
    paired_df.sort_values(["Volunteer Wechat", "Tentative Time (China Timezone)"])
    return paired_df


def compute_volunteers_to_be_paired(volunteers: List[Volunteer]):
    to_be_paired_volunteers_list = []

    for volunteer in volunteers:
        if volunteer.available:
            available_slots_str = ','.join([str(slot) for slot in volunteer.time_slots_china])
            volunteer_info = {
                "Volunteer": volunteer.name,
                "Volunteer Wechat": volunteer.parent_wechat,
                "Availability": volunteer.available_spots,
                "Available Time (China Timezone)": available_slots_str
            }
            to_be_paired_volunteers_list.append(volunteer_info)

    to_be_paired_volunteers_df = pd.DataFrame(to_be_paired_volunteers_list)

    return to_be_paired_volunteers_df

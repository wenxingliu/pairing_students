from typing import List

import pandas as pd

import settings as settings
from data_export.utils import _compute_export_file_path
from models.volunteer import Volunteer


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

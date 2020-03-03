import datetime as dt
import pandas as pd
from typing import List

from models.volunteer import Volunteer
import settings as settings


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

    if no_org_df.empty:
        print("No no_org")
    else:
        no_org_df.sort_values(['Organization', 'Volunteer'], inplace=True)

        if log_file:
            file_path = _compute_export_file_path('no_org_volunteers.csv', settings.DATA_OUTPUT_DIR)
            no_org_df.to_csv(file_path, index=False)

        return no_org_df


def _compute_export_file_path(file_name: str, dir_path: str) -> str:
    dt_str = dt.datetime.utcnow().strftime("%Y%m%d%H%M")
    file_path = f"{dir_path}/{dt_str}_{file_name}"
    return file_path

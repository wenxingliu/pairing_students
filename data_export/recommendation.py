from typing import List

import pandas as pd

import settings as settings
from data_export.utils import _compute_export_file_path
from models.volunteer import Volunteer


def compute_volunteers_recommendations(volunteers: List[Volunteer], log_file: bool = True):
    recommendation_list = []

    for volunteer in volunteers:

        for requestee in volunteer.potential_match:

            if volunteer.email_sent:
                email_sent_time_str = volunteer.email_sent_time_utc.strftime("%Y-%m-%d %H:%M:%S")
            else:
                email_sent_time_str = settings.DUMMY_MONDAY_DATE

            recommendation_info = {
                "organization": volunteer.organization,
                "volunteer": volunteer.name,
                "volunteer_age": volunteer.age,
                "volunteer_wechat": volunteer.parent_wechat,
                "volunteer_email": volunteer.volunteer_email,
                "volunteer_parent_email": volunteer.parent_email,
                "requestee": requestee.name,
                "requestee_age": requestee.age,
                "requestee_wechat": requestee.parent_wechat,
                "requestee_email": requestee.parent_email,
                "requestee_phone": requestee.parent_phone,
                "student_tentative_time": requestee.time_slots_local,
                "other_wechat_info": requestee.other_wechat_info,
                "doctor_family": requestee.doctor_family,
                "patient_family": requestee.patient_family,
                "hubei_family": requestee.hubei_family,
                "request_time_slot": requestee.time_slots_local,
                "volunteer_email_sent": str(volunteer.email_sent),
                "email_sent_time_utc": email_sent_time_str
            }

            recommendation_list.append(recommendation_info)

    recommendation_df = pd.DataFrame(recommendation_list)

    if recommendation_df.empty:
        print(f'No recommendation')
    else:
        recommendation_df.sort_values(['organization', 'volunteer', 'student_tentative_time'], inplace=True)

        if log_file:
            file_path = _compute_export_file_path('recommendations.csv', settings.DATA_OUTPUT_DIR)
            recommendation_df.to_csv(file_path, index=False)

        doctor_family_count = int(recommendation_df.doctor_family.sum())
        patient_family_count = int(recommendation_df.patient_family.sum())

        print(f"""
        Recommendation pairs: {len(recommendation_df)} 
        Doctor Family: {doctor_family_count}
        Patient Family: {patient_family_count}
        """)

        return recommendation_df

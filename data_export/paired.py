from typing import List

import pandas as pd

import settings as settings
from data_export.utils import _compute_export_file_path
from models.requestee import Requestee


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
                "volunteer_age": volunteer.age,
                "volunteer_wechat": volunteer.parent_wechat,
                "volunteer_email": volunteer.volunteer_email,
                "volunteer_parent_email": volunteer.parent_email,
                "requestee": requestee.name,
                "requestee_age": requestee.age,
                "requestee_wechat": requestee.parent_wechat,
                "requestee_email": requestee.parent_email,
                "requestee_phone": requestee.parent_phone,
                "requested_volunteer_gender": requestee.volunteer_gender,
                "promised_time_slot": str(promised_time_slot),
                "slot_start_time": promised_time_slot.start.strftime("%H:%M"),
                "slot_end_time": promised_time_slot.end.strftime("%H:%M"),
                "weekday": promised_time_slot.weekday,
                "volunteer_email_sent": str(requestee.volunteer.email_sent),
                "email_sent_time_utc": email_sent_time_str,
                "other_wechat_info": requestee.other_wechat_info,
                "doctor_family": requestee.doctor_family,
                "patient_family": requestee.patient_family,
                "hubei_family": requestee.hubei_family
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

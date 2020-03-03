from typing import List

import pandas as pd

import settings as settings
from data_export.utils import _compute_export_file_path
from models.requestee import Requestee


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
            "hubei_family": requestee.hubei_family,
            "recommendation_made": "Yes" if requestee.recommendation_made else "No",
            "time_slots_china": requestee.time_slots_local,
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

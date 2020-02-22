from typing import List
from data_export import (compute_paired_data,
                         compute_volunteers_to_be_paired,
                         compute_volunteers_recommendations)
from data_mapper import read_and_clean_requests, read_and_clean_volunteers
from google_client.email_notification import email_to_all_volunteers
from services.pairing import pair_for_all
from services.recommendation import make_recommendations_for_all_unassigned_volunteers
from services.utils.requestee import compute_requestees
from services.utils.volunteer import compute_volunteers

DATA_OUTPUT_DIR = 'data/outputs/'


def main(request_file_path_list: List[str],
         volunteer_file_path_list: List[str],
         send_out_email: bool = False,
         log_results: bool = True):
    requestee_df = read_and_clean_requests(xlsx_file_path_list=request_file_path_list,
                                           sheet_name='学生信息收集表')
    requestee_df = requestee_df.loc[requestee_df.doctor_family == 1]

    volunteer_df = read_and_clean_volunteers(xlsx_file_path_list=volunteer_file_path_list,
                                             sheet_name='Form Responses 1')

    requestees = compute_requestees(requestee_df)
    volunteers = compute_volunteers(volunteer_df)

    pair_for_all(all_requestees=requestees, all_volunteers=volunteers)

    make_recommendations_for_all_unassigned_volunteers(all_requestees=requestees,
                                                       all_volunteers=volunteers)

    if send_out_email:
        email_to_all_volunteers(volunteers)

    if log_results:
        paired_df = compute_paired_data(requestees)
        recommendation_df = compute_volunteers_recommendations(volunteers)
        unassigned_volunteers_df = compute_volunteers_to_be_paired(volunteers)

        paired_df.to_csv(f'{DATA_OUTPUT_DIR}/paired.csv', index=False)
        recommendation_df.to_csv(f'{DATA_OUTPUT_DIR}/recommendation.csv', index=False)
        unassigned_volunteers_df.to_csv(f'{DATA_OUTPUT_DIR}/unassigned_volunteers.csv', index=False)


if __name__ == '__main__':
    main(volunteer_file_path_list=['1 to 1 English teaching_mock.xlsx'],
         request_file_path_list=['request_cov19_02192020.xlsx', 'requests_yan_an.xlsx'],
         send_out_email=False,
         log_results=True)
    print('breakpoint')

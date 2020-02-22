from typing import List
from data_export import (compute_paired_data,
                         compute_unassigned_volunteers,
                         compute_volunteers_recommendations,
                         compute_unassgined_requestee)
from data_mapper import (read_and_clean_requests,
                         read_and_clean_volunteers,
                         read_previous_paired_results)
from google_client.email_notification import email_to_all_volunteers
from services.pairing import pair_for_all
from services.previous_pairing import (reflect_all_previously_paired_results,
                                       compute_previously_assigned_pairs)
from services.recommendation import make_recommendations_for_all_unassigned_volunteers
from services.utils.requestee import compute_requestees
from services.utils.volunteer import compute_volunteers


def main(request_file_path_list: List[str],
         volunteer_file_path_list: List[str],
         previously_paired_file_path_list: List[str] = None,
         send_email: bool = False,
         log_file: bool = True):

    # Step 1: Read volunteer data and request data from files
    requestee_df = read_and_clean_requests(xlsx_file_path_list=request_file_path_list,
                                           sheet_name='学生信息收集表')

    volunteer_df = read_and_clean_volunteers(xlsx_file_path_list=volunteer_file_path_list,
                                             sheet_name='Form Responses 1')

    # Step 2: Compute corresponding class objects
    requestees = compute_requestees(requestee_df)
    volunteers = compute_volunteers(volunteer_df)

    # Step 3: Read existing pairing data, and reflect existing pairing with new data
    if previously_paired_file_path_list is not None:
        existing_pairs_df = read_previous_paired_results(previously_paired_file_path_list)
        existing_pairs = compute_previously_assigned_pairs(existing_pairs_df)

        reflect_all_previously_paired_results(all_volunteers=volunteers,
                                              all_requestees=requestees,
                                              existing_pairs=existing_pairs)

    # Step 4: Find match based on gender, time slot
    pair_for_all(all_requestees=requestees, all_volunteers=volunteers)

    # Step 5: For unassigned volunteers, make recommendations
    make_recommendations_for_all_unassigned_volunteers(all_requestees=requestees,
                                                       all_volunteers=volunteers)

    if send_email:
        try:
            email_to_all_volunteers(volunteers)
        except:
            print("Error when sending emails")

    paired_df = compute_paired_data(requestees, log_file)
    recommendation_df = compute_volunteers_recommendations(volunteers, log_file)
    unassigned_volunteers_df = compute_unassigned_volunteers(volunteers, log_file)
    unassigned_requestee_df = compute_unassgined_requestee(requestees, log_file)

    return [paired_df, recommendation_df, unassigned_volunteers_df, unassigned_requestee_df]


if __name__ == '__main__':
    df_list = main(volunteer_file_path_list=[],
                   request_file_path_list=['request_cov19_02192020', 'requests_yan_an'],
                   previously_paired_file_path_list=None,
                   send_email=False,
                   log_file=True)
    print('breakpoint')

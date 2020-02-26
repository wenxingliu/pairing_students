from typing import List, Set
from data_export import (compute_paired_data,
                         compute_unassigned_volunteers,
                         compute_volunteers_recommendations,
                         compute_unassgined_requestee,
                         compute_no_organization_volunteers)
from data_mapper import (read_and_clean_requests,
                         read_and_clean_volunteers,
                         read_previous_paired_results)
from google_client.email_notification import email_to_all_volunteers, generate_email_text
from services.pairing import pair_for_all
from services.previous_pairing import (reflect_all_previously_paired_results,
                                       compute_previously_assigned_pairs)
from services.recommendation import make_recommendations_for_all_unassigned_volunteers
from services.utils.requestee import compute_requestees
from services.utils.volunteer import compute_volunteers


def main(request_file_path_list: List[str],
         volunteer_file_path_list: List[str],
         previously_paired_file_path_list: List[str] = None,
         keep_previou_pairing_results: bool = True,
         send_email: bool = False,
         include_unassigned: bool = False,
         log_file: bool = True):

    # Step 1: Read volunteer data and request data from files
    requestee_df = read_and_clean_requests(xlsx_file_path_list=request_file_path_list,
                                           sheet_name='学生信息收集表最新版')

    volunteer_df = read_and_clean_volunteers(xlsx_file_path_list=volunteer_file_path_list,
                                             sheet_name='Form Responses 1')

    # Step 2: Read existing pairing data, and reflect existing pairing with new data
    if previously_paired_file_path_list is not None:
        existing_pairs_df = read_previous_paired_results(previously_paired_file_path_list,
                                                         keep_previou_pairing_results)
        existing_pairs = compute_previously_assigned_pairs(existing_pairs_df)

    # Step 3: Compute corresponding class objects
    requestees = compute_requestees(requestee_df, existing_pairs)
    volunteers = compute_volunteers(volunteer_df, existing_pairs)

    # Step 4: Find match based on gender, time slot
    pair_for_all(all_requestees=requestees, all_volunteers=volunteers)

    # Step 5: For unassigned volunteers, make recommendations
    make_recommendations_for_all_unassigned_volunteers(all_requestees=requestees,
                                                       all_volunteers=volunteers)

    # Step 6: Send email
    try:
        if send_email:
            email_to_all_volunteers(volunteers, include_unassigned=include_unassigned)
        else:
            generate_email_text(volunteers, include_unassigned=include_unassigned)
    except:
        print("Error when sending emails")

    try:
        paired_df = compute_paired_data(requestees, log_file)
    except:
        print(f"failed to generate paired_df")

    try:
        recommendation_df = compute_volunteers_recommendations(volunteers, log_file)
    except:
        print(f"failed to generate recommendation_df")

    try:
        unassigned_volunteers_df = compute_unassigned_volunteers(volunteers, log_file)
    except:
        print(f"failed to generate unassigned_volunteers_df")

    try:
        unassigned_requestee_df = compute_unassgined_requestee(requestees, log_file)
    except:
        print(f"failed to generate unassigned_requestee_df")

    try:
        no_org_volunteers = compute_no_organization_volunteers(volunteers, log_file)
    except:
        print(f"failed to generate no_org_volunteers")


if __name__ == '__main__':
    main(volunteer_file_path_list=['volunteer_cleaned_0225'],
         request_file_path_list=['requests_wuhan_20200224'],
         previously_paired_file_path_list=None,
         keep_previou_pairing_results=False,
         include_unassigned=False,
         send_email=False,
         log_file=False)
    print('breakpoint')

import datetime as dt
from typing import List
from data_export import (compute_paired_data,
                         compute_unassigned_volunteers,
                         compute_volunteers_recommendations,
                         compute_unassgined_requestee,
                         compute_no_organization_volunteers)
from data_mapper import (read_and_clean_requests,
                         read_and_clean_volunteers,
                         read_previous_paired_results,
                         read_pairing_feedback)
from google_client.email_notification import email_to_all_volunteers, generate_email_text
from services.pairing import pair_for_all
from services.previous_pairing import compute_previously_assigned_pairs
from services.pairing_feedback import process_paired_info_based_on_feedback
from services.recommendation import make_recommendations_for_all_unassigned_requestees
from services.utils.requestee import compute_requestees
from services.utils.volunteer import compute_volunteers


def main(request_file_path_list: List[str],
         volunteer_file_path_list: List[str],
         previously_paired_file_path_list: List[str] = None,
         pairing_feedback_file_path_list: List[str] = None,
         make_recommendation: bool = False,
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
        existing_pairs_df = read_previous_paired_results(previously_paired_file_path_list)
        existing_pairs = compute_previously_assigned_pairs(existing_pairs_df)
    else:
        existing_pairs = set()

    # Step 3: Read feedbacks, and adjust previous pairs
    if pairing_feedback_file_path_list is not None:
        feedback_df = read_pairing_feedback(xlsx_file_path_list=pairing_feedback_file_path_list,
                                            sheet_name='Form Responses 1')
        backouts = process_paired_info_based_on_feedback(feedback_df,
                                                         existing_pairs)
    else:
        backouts = None

    # Step 4: Compute corresponding class objects
    requestees = compute_requestees(requestee_df, existing_pairs, backouts)
    volunteers = compute_volunteers(volunteer_df, existing_pairs, backouts)

    # Step 5: Find match based on gender, time slot
    pair_for_all(all_requestees=requestees, all_volunteers=volunteers)

    # Step 6: For unassigned volunteers, make recommendations
    if make_recommendation:
        make_recommendations_for_all_unassigned_requestees(all_requestees=requestees,
                                                           all_volunteers=volunteers)

    # Step 7: Send email
    try:
        if send_email:
            email_to_all_volunteers(volunteers, include_unassigned=include_unassigned)
        else:
            generate_email_text(volunteers, include_unassigned=include_unassigned)
    except:
        print("Error when sending emails")

    # Step 8: Log files
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
    main(volunteer_file_path_list=['volunteer_cleaned_0301_SL'],
         request_file_path_list=['requests/20200226最新报名（全国范围）',
                                 'requests/20200226最新报名（武汉扩招）',
                                 'requests/20200227最新报名（全国范围）',
                                 'requests/20200227最新报名（武汉扩招）',
                                 'requests/20200228最新报名（全国范围）',
                                 'requests/20200228最新报名（武汉扩招）',
                                 'requests/20200229最新报名（全国范围）',
                                 'requests/20200229最新报名（武汉扩招）',
                                 'requests/20200301最新报名（全国范围）',
                                 'requests/20200301最新报名（武汉扩招）'],
         previously_paired_file_path_list=['sent/20200226匹配并联系成功表-核实后',
                                           'sent/202002270452_paired_sent',
                                           'sent/202002270452_recommendations_sent',
                                           'sent/202002272226_paired_sent',
                                           'sent/202002272226_recommendations_sent',
                                           'sent/202002290417_paired_sent',
                                           'sent/202002290417_recommendations_sent',
                                           'sent/202002291812_paired_sent',
                                           'sent/202002291812_recommendations_sent',
                                           'sent/202003020222_paired_sent',
                                           'sent/202003020222_recommendations_sent',
                                           'sent/202003030603_paired_sent',
                                           'sent/202003030603_recommendations_sent'],
         pairing_feedback_file_path_list=['pairing_feedback_response'],
         include_unassigned=False,
         make_recommendation=True,
         send_email=False,
         log_file=False)
    print('breakpoint')

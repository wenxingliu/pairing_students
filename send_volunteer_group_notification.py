from typing import List
from data_mapper import read_and_clean_volunteers
from google_client.email_notification import notification_email_to_all_volunteers
from services.utils.volunteer import compute_volunteers


def main(subject: str,
         email_text_file: str,
         volunteer_file_path_list: List[str],
         others_org_only: bool=False,
         send_email: bool = False):
    volunteer_df = read_and_clean_volunteers(xlsx_file_path_list=volunteer_file_path_list,
                                             sheet_name='Form Responses 1')
    volunteers = compute_volunteers(volunteer_df)
    if send_email:
        notification_email_to_all_volunteers(subject=subject,
                                             email_text_file=email_text_file,
                                             volunteers=volunteers,
                                             others_org_only=others_org_only)


if __name__ == '__main__':
    main(subject="[Online Tutoring For Students In Wuhan Project] Attention Needed!",
         email_text_file="after_1st_round_followup_email.txt",
         volunteer_file_path_list=['mock/volunteer_mock_3'],
         others_org_only=False,
         send_email=True)
    print('breakpoint')

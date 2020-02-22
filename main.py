from data_mapper import read_and_clean_requests, read_and_clean_volunteers
from utils.pairing import compute_requestees, compute_volunteers, pair_for_all

from data_export import compute_paired_data, compute_volunteers_to_be_paired

requestee_df = read_and_clean_requests(xlsx_file_path='data/request_02192020.xlsx',
                                       sheet_name='学生信息收集表')
requestee_df = requestee_df.loc[requestee_df.doctor_family == 1]

volunteer_df = read_and_clean_volunteers(xlsx_file_path='data/1 to 1 English teaching.xlsx',
                                         sheet_name='Form Responses 1')

requestees = compute_requestees(requestee_df)
volunteers = compute_volunteers(volunteer_df)

pair_for_all(requestees, volunteers)

paired_df = compute_paired_data(requestees)
to_be_paired_volunteers_df = compute_volunteers_to_be_paired(volunteers)

paired_df.to_csv('data/paired.csv', index=False)
to_be_paired_volunteers_df.to_csv('data/to_be_paired_volunteers.csv', index=False)

print('breakpoint')
